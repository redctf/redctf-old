import graphene
import rethinkdb as r
import re
from dockerAPI.dockerAPI import *
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from redctf.settings import RDB_HOST, RDB_PORT, CTF_DB
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from django.utils.dateformat import format
from users.validators import validate_user_is_admin, validate_user_is_authenticated
from challenges.validators import validate_flag, validate_flag_unique, validate_points, validate_title, validate_description, validate_imageName, validate_ports, validate_pathPrefix, validate_pathPrefix_unique
from categories.validators import validate_category_exists
from categories.models import Category
from challenges.models import Challenge
from teams.models import SolvedChallenge, Team
from teams.validators import validate_team_id

d = dockerAPI()

def updatePoints(self, info, chal_id, points):
    status = graphene.String()

    user = info.context.user
    # Validate user is admin
    validate_user_is_admin(user)

    # for team in teams - get solved challenges = id, remove points, remove correct flags, update rethinkdb.

    # get all points for each team, add them up after the points update is done.

    # rethindb data explorer javascript implementation
    # r.db('redctf').table('teams').filter(
    #     function (solved){
    #         return solved('solved').contains(function(id){
    #         return id('id').eq(68);
    #         })
    #     }
    #     )

    rethink_updates = {}

    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        # r.db(CTF_DB).table('teams').filter({'sid':id}).update(rethink_updates).run(connection)
        # get teams with solved challenges containing chal_id
        request = r.db('redctf').table('teams') \
            .concat_map(
            lambda doc: doc['solved']
            .concat_map(lambda data: [{'id': doc['id'], 'sid': doc['sid'], 'name': doc['name'], 'points': doc['points'], 'solved': data}])) \
            .filter(
            lambda doc:
            doc['solved']['id'] == chal_id
        ).run(connection)
        print('update rethink results: {0}'.format(request))

    except RqlRuntimeError as e:
        raise Exception(
            'Error updating challenge from realtime database: %s' % (e))


    try:
        # get each team object, then update the team's points and the solved challenge points accordingly.
        for team in request:
            print('Updating {0}\'s points.'.format(team['name']))

            # calculate the difference in points from old points value to new.
            chal_diff_points = abs(team['solved']['points'] - points)

            # get the team object to have the full solved array to do a single nested udpate
            team_object = r.db('redctf').table(
                'teams').get(team['id']).run(connection)
            solved_object = team_object['solved']

            # get the django team object
            if Team.objects.filter(id__iexact=team_object['sid']).exists():
                django_team_object = Team.objects.get(id__iexact=team_object['sid'])
            else:
                raise Exception(
                    'unable to find team in backend'
                )
            for index, chal in enumerate(solved_object):
                print('#{0}: {1}'.format(index, chal))
                if chal['id'] == chal_id:
                    if points == 0:
                        del solved_object[index]
                        # print('removed chal from solved: {0}'.format(d))
                    else:
                        solved_object[index]['points'] = points
                        print('updated #{0} points = {1}'.format(
                        index, points))

        # if the updated points value is less than the existing value for the challenge subtract the chal_diff_points to team's total points
        if points < team['solved']['points']:
            # update total team points
            rethink_updates['points'] = team['points'] - \
                chal_diff_points
            

        # if the updated points value is greater than the existing value for the challenge add the chal_diff_points to team's total points
        elif points > team['solved']['points']:
            # update total team points
            rethink_updates['points'] = team['points'] + \
                chal_diff_points

        else:
            print('no points change')
            raise Exception(
                'updated points value is equal to the existing points value')
        # set backend updated team points
        django_team_object.points = rethink_updates['points']
        """
        Trying to delete an SolvedChallenge object when points are 0 (passed in from DeleteChallege). The Team object contains the many to many relationship solved challenge object which contains the challenge ID. 
        """
        if points == 0:
            print('delete django nested object.')
            # django_team_object.solved
        django_team_object.save()
        
        # set updated challenge points
        rethink_updates['solved'] = solved_object

        # run updates
        update = r.db('redctf').table('teams') \
            .get(team['id'])\
            .update(rethink_updates).run(connection)
        print('updates: {0}'.format(update))

    except Exception as ex:
        raise Exception(
            'Error updating points: {0}'.format(ex)
        )
    
    finally:
        connection.close()
        status = 'Points updated'
    return status

class AddChallenge(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        category = graphene.Int(required=True)
        title = graphene.String(required=True)
        points = graphene.Int(required=True)
        description = graphene.String(required=True)
        flag = graphene.String(required=True)
        hosted = graphene.Boolean(required=True)
        image_name = graphene.String(required=False)
        ports = graphene.String(required=False)
        # path_prefix = graphene.String(required=False)
        upload = Upload(required=False)

    def mutate(self, info, category, title, points, description, flag, hosted, ports, image_name=None, upload=None):
        user = info.context.user
        # Validate user is admin
        validate_user_is_admin(user)

        # sanitize all the input fields
        validate_flag(flag)
        validate_flag_unique(flag)
        validate_points(points)
        validate_title(title)
        validate_description(description)
        validate_category_exists(category)
        if image_name:
            validate_imageName(image_name)
        if ports:
            validate_ports(ports)
        # if path_prefix:
        #     validate_pathPrefix(path_prefix)
        #     validate_pathPrefix_unique(path_prefix)

        # parse dockerfile for list of ports
        if upload:
            try:
                ports = list()
                for line in upload:
                    line = line.decode('utf-8')
                    start = 'EXPOSE '

                    if (start in line):
                        possible_port = (line[line.find(start)+len(start):])
                        ports.append(possible_port.split())

                # flatten list
                flattened_ports = list(
                    set([val for sublist in ports for val in sublist]))
                print(flattened_ports)

            except Exception as e:
                raise Exception('Error parsing uploaded Dockerfile: ', e)

        challenge_category = Category.objects.get(id=category)

        # Save the challenge flag to the database
        challenge = Challenge(category=challenge_category, title=title, description=description,
                              flag=flag, points=points, hosted=hosted, imageName=image_name, ports=ports)
        challenge.save()

        # set var for pathPrefix and tag
        path_tag = str(challenge.id)
        challenge.pathPrefix = path_tag

        if upload:
            image_name = path_tag + ':latest'

            # build image
            build = d.buildImage(fileobj=upload.file, tag=path_tag)

            # delete already saved challenge if build fails
            if not build:
                chall_id = challenge.id
                try:
                    challenge.delete()
                except:
                    # raise exception if unable to delete already saved challenge requiring manual intervention
                    raise Exception(
                        'Unable to delete challenge ID: %i. Manual deletion necessary.' % (chall_id))

                raise Exception(
                    'Unable to build image.  Reverted challenge creation.')

            challenge.upload = upload
            challenge.imageName = image_name

        challenge.save()

        # Push the realtime data to rethinkdb
        connection = r.connect(host=RDB_HOST, port=RDB_PORT)
        try:
            r.db(CTF_DB).table('challenges').insert({'sid': challenge.id, 'category': challenge.category.id, 'title': title, 'points': points, 'description': description,
                                                     'hosted': hosted, 'imageName': image_name, 'ports': ports, 'pathPrefix': path_tag, 'created': format(challenge.created, 'U')}).run(connection)
        except RqlRuntimeError as e:
            raise Exception(
                'Error adding challenge to realtime database: %s' % (e))
        finally:
            connection.close()

        return AddChallenge(status='Challenge Created')


class CheckFlag(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        flag = graphene.String(required=True)

    def mutate(self, info, flag):
        user = info.context.user
        # Validate user is authenticated
        validate_user_is_authenticated(user)

        # Sanitize flag input
        validate_flag(flag)

        correct = False
        if Challenge.objects.filter(flag__iexact=flag).exists():
            chal = Challenge.objects.get(flag__iexact=flag)
            if chal.id not in user.team.solved.all().values_list('challenge_id', flat=True):
                user.team.points += chal.points
                user.team.correct_flags += 1
                sc = SolvedChallenge(challenge=chal)
                sc.save()
                user.team.solved.add(sc)
                user.team.save()
            correct = True
        else:
            user.team.wrong_flags += 1
            user.team.save()
            correct = False

        # Create list of solved challenges
        solved = []
        for sc in user.team.solved.all().order_by('timestamp'):
            solved.append({'id': sc.challenge.id, 'points': sc.challenge.points,
                           'timestamp': format(sc.timestamp, 'U')})

        # Push the realtime data to rethinkdb
        connection = r.connect(host=RDB_HOST, port=RDB_PORT)
        try:
            r.db(CTF_DB).table('teams').filter({"sid": user.team.id}).update(
                {'points': user.team.points, 'correct_flags': user.team.correct_flags, 'wrong_flags': user.team.wrong_flags, 'solved': solved}).run(connection)
            if correct:
                r.db(CTF_DB).table('challenges').filter({"sid": chal.id}).update(
                    {'solved_count': SolvedChallenge.objects.filter(challenge=chal).count()}).run(connection)
        except RqlRuntimeError as e:
            raise Exception(
                'Error adding category to realtime database: %s' % (e))
        finally:
            connection.close()

        if correct:
            return CheckFlag(status='Correct Flag')
        else:
            return CheckFlag(status='Wrong Flag')


class DeleteChallenge(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        user = info.context.user
        # Validate user is admin
        validate_user_is_admin(user)

        removePoints = updatePoints(self, info, id, 0)
        
        connection = r.connect(host=RDB_HOST, port=RDB_PORT)
        try:
            r.db(CTF_DB).table('challenges').filter(
                {'sid': id}).delete().run(connection)
        except RqlRuntimeError as e:
            raise Exception(
                'Error deleting challenge from realtime database: %s' % (e))
        finally:
            connection.close()

        # ID is primary key for django, SID is PK in Rethink
        if Challenge.objects.filter(id__iexact=id).exists():
            chal = Challenge.objects.get(id__iexact=id)
            chal.delete()

        else:
            # return DeleteChallenge(status='Error deleting challenge from database: %s' % (id))
            raise Exception(
                'Error deleting challenge from database: %s' % (id))

        return DeleteChallenge(status='Challenge Deleted: %s' % (id))


class UpdateChallenge(graphene.Mutation):
    status = graphene.String()
    class Arguments:
        id = graphene.Int(required=True)
        category = graphene.Int(required=False)
        title = graphene.String(required=False)
        points = graphene.Int(required=False)
        description = graphene.String(required=False)
        flag = graphene.String(required=False)
        hosted = graphene.Boolean(required=False)
        image_name = graphene.String(required=False)
        ports = graphene.String(required=False)
        upload = Upload(required=False)

    def mutate(self, info, id, category=None, title=None, points=None, description=None, flag=None, hosted=None, image_name=None, ports=None, upload=None):

        user = info.context.user
        # Validate user is admin
        validate_user_is_admin(user)
        
        

        rethink_updates = {}

        if Challenge.objects.filter(id__iexact=id).exists():
            chal = Challenge.objects.get(id__iexact=id)
            if title is not None:
                validate_title(title)
                chal.title = title
                rethink_updates['title'] = title

            if category is not None:
                validate_category_exists(category)
                challenge_category = Category.objects.get(id=category)
                chal.category = challenge_category
                rethink_updates['category'] = category

            if points is not None:
                validate_points(points)
                chal.points = points
                # update challenge points in rethink
                rethink_updates['points'] = points
                
                # update team's points and solved challenges' points
                try:
                    u = updatePoints(self, info, id, points)
                    print('update points: {0}'.format(u))
                except Exception as ex:
                    raise Exception('update points exception: {0}'.format(ex))

            if description is not None:
                validate_description(description)
                chal.description = description
                rethink_updates['description'] = description

            if flag is not None:
                validate_flag(flag)
                validate_flag_unique(flag)
                chal.flag = flag
                rethink_updates['flag'] = flag

            if hosted is not None:
                chal.hosted = hosted
                rethink_updates['hosted'] = hosted

            if image_name is not None:
                validate_imageName(image_name)
                chal.imageName = image_name
                rethink_updates['imageName'] = image_name

            if ports is not None:
                validate_ports(ports)
                chal.ports = ports
                rethink_updates['ports'] = ports

            if upload is not None:
                try:
                    ports = list()
                    for line in upload:
                        line = line.decode('utf-8')
                        start = 'EXPOSE '

                        if (start in line):
                            possible_port = (
                                line[line.find(start)+len(start):])
                            ports.append(possible_port.split())

                    # flatten list
                    flattened_ports = list(
                        set([val for sublist in ports for val in sublist]))
                    print(flattened_ports)
                    chal.ports = flattened_ports
                    chal.upload = upload
                    # rethink doesn't need the file object, may add metadata later
                    # rethink_updates['upload'] = upload

                except Exception as e:
                    raise Exception('Error parsing uploaded Dockerfile: ', e)
            chal.save()

        else:
            raise Exception('Error - can\'t find challenge: %s' % (id))

        connection = r.connect(host=RDB_HOST, port=RDB_PORT)
        try:
            r.db(CTF_DB).table('challenges').filter(
                {'sid': id}).update(rethink_updates).run(connection)
        except RqlRuntimeError as e:
            raise Exception(
                'Error updating challenge from realtime database: %s' % (e))
        finally:
            connection.close()

        return UpdateChallenge(status='Challenge Updated: %s' % (id))

class Mutation(graphene.ObjectType):
    add_challenge = AddChallenge.Field()
    check_flag = CheckFlag.Field()
    delete_challenge = DeleteChallenge.Field()
    update_challenge = UpdateChallenge.Field()
