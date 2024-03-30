import graphene
import rethinkdb as r
import re
from dockerAPI.dockerAPI import *
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from redctf.settings import RDB_HOST, RDB_PORT, CTF_DB
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from django.utils.dateformat import format
from django.utils import timezone
from users.validators import validate_user_is_admin, validate_user_is_authenticated
from challenges.validators import validate_flag, validate_flag_unique, validate_points, validate_title, validate_description, validate_imageName, validate_ports, validate_pathPrefix, validate_pathPrefix_unique
from categories.validators import validate_category_exists
from categories.models import Category
from challenges.models import Challenge
from ctfs.models import Ctf
from teams.models import SolvedChallenge, Team
from teams.validators import validate_team_id

d = dockerAPI()


def getDjangoTeamsWithSolvedChallengesByID(self, info, chal_id):
    status = graphene.String()

    user = info.context.user
    # Validate user is admin
    validate_user_is_admin(user)

    # get the django team object
    if Team.objects.filter(solved__challenge_id=chal_id).exists():
        teams = Team.objects.filter(solved__challenge_id=chal_id)
        return teams
    else:
        return False

    
def updatePoints(self, info, chal_id, points):
    status = graphene.String()

    user = info.context.user
    # Validate user is admin
    validate_user_is_admin(user)
    
    teams = getDjangoTeamsWithSolvedChallengesByID(self, info, chal_id) 
    
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    rethink_updates = {}
   
    if teams:
        try:
            for team in teams: 
                print('Updating {0}\'s points.'.format(team.name))  
                        
                # calculate the difference in points from old points value to new.
                challenge = Challenge.objects.get(id=chal_id)
                chal_diff_points = abs(challenge.points - points)
                rethink_teams = r.db(CTF_DB).table('teams').filter({'sid':team.id}).run(connection)    

                # use for loop to access the object(s) values and assign to team id variable
                for rethink_team in rethink_teams: 
                    # print(rethink_team['id'])   
                    rethink_team_id = rethink_team['id']
                
                rethink_team_object = r.db('redctf').table(
                'teams').get(rethink_team_id).run(connection)
                
                # get rethink team solved object 
                solved_object = rethink_team_object['solved']
                
                # print(rethink_team_id)
            
                
                # if the updated points value is less than the existing value for the challenge subtract the chal_diff_points to team's total points
                if points < challenge.points:
                    # update total team points
                    team.points -= chal_diff_points
                    
                # if the updated points value is greater than the existing value for the challenge add the chal_diff_points to team's total points
                elif points > challenge.points:
                    # update total team points
                    team.points += chal_diff_points

                else:
                    print('no points change')
                    raise Exception(
                        'updated points value is equal to the existing points value')
                
                # set backend updated team points
                team.save()
                
                # set update for rethinkdb team points
                rethink_updates['points'] = team.points
                
                # update the team's solved challenge points
                solved_challenge = team.solved.get(challenge_id=chal_id)
                solved_challenge.points = points
                
                
                # find challenges to update within rethink solved object
                for index, challenge in enumerate(solved_object):
                    if challenge['id'] == chal_id:
                        solved_object[index]['points'] = points
                
                # update solved object for rethink update
                rethink_updates['solved'] = solved_object
                
                # run updates on rethink
                update = r.db('redctf').table('teams') \
                    .get(rethink_team_id)\
                    .update(rethink_updates).run(connection)
                print('updates: {0}'.format(update))

                    
                
        except Exception as ex:
            raise Exception('error with teams')
            
    else:
        print('no matching teams ')
   
    
    return True
        

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
        runtime = graphene.String(required=False)
        ports = graphene.String(required=False)
        # path_prefix = graphene.String(required=False)
        upload = Upload(required=False)

    def mutate(self, info, category, title, points, description, flag, hosted, ports, image_name=None, runtime=None, upload=None):
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
        if runtime:
            validate_runtime(runtime)
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
                              flag=flag, points=points, hosted=hosted, imageName=image_name, runtime=runtime, ports=ports)
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
                                                     'hosted': hosted, 'imageName': image_name, 'runtime': runtime, 'ports': ports, 'pathPrefix': path_tag, 'created': format(challenge.created, 'U')}).run(connection)
        except RqlRuntimeError as e:
            raise Exception(
                'Error adding challenge to realtime database: %s' % (e))
        finally:
            connection.close()

        return AddChallenge(status='Challenge Created')


class GetFlag(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        challenge = graphene.String(required=False)

    def mutate(self, info):
        user = info.context.user

        if not user.is_anonymous:
            raise Exception('Error: way too authenticated...')

        #no active ctf
        return GetFlag(status='ctf{}')


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

        # Validate active Ctf
        if Ctf.objects.filter(start__lt=timezone.now(), end__gt=timezone.now()):
            
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
        else:
            #no active ctf
            return CheckFlag(status='No currently active CTF')


class DeleteChallenge(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        chal_id = graphene.Int(required=True)

    def mutate(self, info, chal_id):
        user = info.context.user
        # Validate user is admin
        validate_user_is_admin(user)

        # update total team points
        # removePoints = removePoints(self, info, id, 0)
        
        connection = r.connect(host=RDB_HOST, port=RDB_PORT)
        
        # update each team with solved challenges 
        teams = getDjangoTeamsWithSolvedChallengesByID(self, info, chal_id)
        
        rethink_updates = {}
        if teams:
            # print('matching teams')
            try:
                for team in teams: 
                    print('Updating {0}\'s points.'.format(team.name))  
                            
                    # calculate the difference in points from old points value to new.
                    challenge = Challenge.objects.get(id=chal_id)
                    
                    rethink_teams = r.db(CTF_DB).table('teams').filter({'sid':team.id}).run(connection)    
                    
                    # use for loop to access the object(s) values and assign to team id variable
                    for rethink_team in rethink_teams: 
                        print(rethink_team['id'])   
                        rethink_team_id = rethink_team['id']
                    
                    rethink_team_object = r.db('redctf').table(
                    'teams').get(rethink_team_id).run(connection)
                    
                    # get rethink team solved object 
                    solved_object = rethink_team_object['solved']

                    # set django team points
                    team.points -= challenge.points
                    
                    # set django correct_flags
                    team.correct_flags -= 1 
                                    
                    # save backend updated team points
                    team.save()
                    
                    # set update for rethinkdb team points
                    rethink_updates['points'] = team.points
                    
                    # set update for rethinkdb team correct flags
                    rethink_updates['correct_flags'] = team.correct_flags
                    
                    # remove solved challenge object
                    solved_challenge = team.solved.get(challenge_id=chal_id)
                    
                    
                    rethink_updated_solved_object = []
                    # find solved challenges to delete within rethink solved object
                    # this will update the solved challenges to be everything except the one being deleted. 
                    for index, challenge in enumerate(solved_object):
                        if challenge['id'] != chal_id:
                            rethink_updated_solved_object.append(challenge)
                    
                    # update solved object for rethink update (with challenge removedt)
                    rethink_updates['solved'] = rethink_updated_solved_object
                    
                    # run updates on rethink
                    update = r.db('redctf').table('teams') \
                        .get(rethink_team_id)\
                        .update(rethink_updates).run(connection)
                    print('updates: {0}'.format(update))
                    
                    # delete rethink solved challenge
                    solved_challenge.delete()
                    
            except Exception as ex:
                raise Exception('error with teams: {0}'.format(ex))


        
        else:
            print('no matching teams')
            
        try:
            r.db(CTF_DB).table('challenges').filter(
                {'sid': chal_id}).delete().run(connection)
            
        except RqlRuntimeError as e:
            raise Exception(
                'Error deleting challenge from realtime database: %s' % (e))
        finally:
            connection.close()
        # ID is primary key for django, SID is PK in Rethink
        try:
            chal = Challenge.objects.get(id=chal_id)
            chal.delete()

        except Exception as ex:
            # return DeleteChallenge(status='Error deleting challenge from database: %s' % (chal_id))
            raise Exception(
                'Error deleting challenge from database: %s' % (chal_id))

        return DeleteChallenge(status='Challenge Deleted: %s' % (chal_id))
        

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
        runtime = graphene.String(required=False)
        ports = graphene.String(required=False)
        upload = Upload(required=False)

    def mutate(self, info, id, category=None, title=None, points=None, description=None, flag=None, hosted=None, image_name=None, runtime=None, ports=None, upload=None):

        user = info.context.user
        # Validate user is admin
        validate_user_is_admin(user)
        
        

        rethink_updates = {}

        if Challenge.objects.filter(id=id).exists():
            chal = Challenge.objects.get(id =id)
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

            if runtime is not None:
                validate_imageName(runtime)
                chal.runtime = runtime
                rethink_updates['runtime'] = runtime

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
        if len(rethink_updates) != 0:
            

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
    get_flag = GetFlag.Field()
    delete_challenge = DeleteChallenge.Field()
    update_challenge = UpdateChallenge.Field()