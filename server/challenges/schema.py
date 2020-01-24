import graphene
import rethinkdb as r
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
from teams.models import SolvedChallenge

d = dockerAPI()

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
        path_prefix = graphene.String(required=False)
        upload = Upload(required=False)

    def mutate(self, info, category, title, points, description, flag, hosted, image_name, ports, path_prefix, upload=None):
        user = info.context.user
        # Validate user is admin
        validate_user_is_admin(user)

        # TODO: sanitize all the input fields 
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
        if path_prefix:
            validate_pathPrefix(path_prefix)
            validate_pathPrefix_unique(path_prefix)


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
                flattened_ports = list(set([val for sublist in ports for val in sublist]))
                print (flattened_ports)
            except Exception as e:
                raise Exception('Error parsing uploaded Dockerfile: ', e)


        challenge_category = Category.objects.get(id=category)

        # Save the challenge flag to the database
        challenge = Challenge(category=challenge_category, title=title, description=description, flag=flag, points=points, hosted=hosted, imageName=image_name, ports=ports, pathPrefix=path_prefix)
        challenge.save()

        # Challenge needs to be saved before file can be uploaded so ID (primary key) exists
        challenge.upload = upload
        challenge.save()

        # Push the realtime data to rethinkdb
        connection = r.connect(host=RDB_HOST, port=RDB_PORT)
        try:
            r.db(CTF_DB).table('challenges').insert({ 'sid': challenge.id, 'category': challenge.category.id, 'title': title, 'points': points, 'description': description, 'hosted': hosted, 'imageName': image_name, 'ports': ports, 'pathPrefix':path_prefix, 'created': format(challenge.created, 'U')}).run(connection)
        except RqlRuntimeError as e:
            raise Exception('Error adding challenge to realtime database: %s' % (e))
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
            solved.append({'id': sc.challenge.id, 'points': sc.challenge.points, 'timestamp': format(sc.timestamp, 'U')})
             
        # Push the realtime data to rethinkdb
        connection = r.connect(host=RDB_HOST, port=RDB_PORT)
        try:
            r.db(CTF_DB).table('teams').filter({"sid": user.team.id}).update({'points': user.team.points, 'correct_flags': user.team.correct_flags, 'wrong_flags': user.team.wrong_flags, 'solved': solved}).run(connection)
            if correct:
                r.db(CTF_DB).table('challenges').filter({"sid": chal.id}).update({'solved_count': SolvedChallenge.objects.filter(challenge=chal).count()}).run(connection)
        except RqlRuntimeError as e:
            raise Exception('Error adding category to realtime database: %s' % (e))
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
        

        # ID is primary key for django, SID is PK in Rethink
        if Challenge.objects.filter(id__iexact=id).exists():
            chal = Challenge.objects.get(id__iexact=id)
            chal.delete()

        else:
            return DeleteChallenge(status='Error deleting challenge from database: %s' % (id))
            
        connection = r.connect(host=RDB_HOST, port=RDB_PORT)
        try:
            r.db(CTF_DB).table('challenges').filter({'sid':id}).delete().run(connection)
        except RqlRuntimeError as e:
            raise Exception('Error deleting challenge from realtime database: %s' % (e))
        finally:
            connection.close()

        return DeleteChallenge(status='Challenge Deleted: %s' % (id))
    
class UpdateChallenge(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)
        updatedCategory = graphene.Int(required=False)
        updatedTitle = graphene.String(required=False)
        updatedPoints = graphene.Int(required=False)
        updatedDescription = graphene.String(required=False)
        updatedFlag = graphene.String(required=False)
        updatedHosted = graphene.Boolean(required=False)
        updatedImage_name = graphene.String(required=False)
        updatedPorts = graphene.String(required=False)
        updatedPath_prefix = graphene.String(required=False)
        updatedUpload = Upload(required=False)
        

    def mutate(self, info, id, updatedCategory=None, updatedTitle=None, updatedPoints=None, updatedDescription=None, updatedFlag=None, updatedHosted=None, updatedImage_name=None, updatedPorts=None, updatedPath_prefix=None, updatedUpload=None):
        user = info.context.user
        # Validate user is admin
        validate_user_is_admin(user)
        

        rethink_updates = {}
        
        
        if Challenge.objects.filter(id__iexact=id).exists():
            chal = Challenge.objects.get(id__iexact=id)
            if updatedTitle:
                chal.title = updatedTitle
                rethink_updates['title'] = updatedTitle
                
            if updatedCategory:
                challenge_category = Category.objects.get(id=updatedCategory)
                chal.category = challenge_category
                rethink_updates['category'] = updatedCategory
                        
            if updatedPoints:
                chal.points = updatedPoints
                rethink_updates['points'] = updatedPoints
                
            if updatedDescription:
                chal.description = updatedDescription
                rethink_updates['description'] = updatedDescription
                
            if updatedFlag:
                chal.flag = updatedFlag
                rethink_updates['flag'] = updatedFlag
                
            if updatedHosted:
                chal.hosted = updatedHosted
                rethink_updates['hosted'] = updatedHosted
                
            if updatedImage_name:
                chal.imageName = updatedImage_name
                rethink_updates['imageName'] = updatedImage_name
                
            if updatedPorts:
                chal.ports = updatedPorts
                rethink_updates['ports'] = updatedPorts
            
            if updatedPath_prefix:
                chal.pathPrefix = updatedPath_prefix
                rethink_updates['pathPrefix'] = updatedPath_prefix
            
            # if updatedUpload:
            #     if upload:
            #         try:
            #             ports = list()
            #             for line in upload:
            #                 line = line.decode('utf-8')
            #                 start = 'EXPOSE '

            #                 if (start in line):
            #                     possible_port = (line[line.find(start)+len(start):])
            #                     ports.append(possible_port.split())

            #         # flatten list
            #         flattened_ports = list(set([val for sublist in ports for val in sublist]))
            #         print (flattened_ports)
            #     except Exception as e:
            #         raise Exception('Error parsing uploaded Dockerfile: ', e)
            #     chal.upload = updatedUpload
            #     rethink_updates['upload'] = updatedUpload
            
            chal.save()
            
            
        else:
            # TODO: updates broken. it updates the challenge and adds the new one called title with value title 
            return UpdateChallenge(status='Error updating challenge')
        # updates = {'title':updatedTitle}
        connection = r.connect(host=RDB_HOST, port=RDB_PORT)
        try:
            r.db(CTF_DB).table('challenges').filter({'sid':id}).update(rethink_updates).run(connection)
        except RqlRuntimeError as e:
            raise Exception('Error updating challenge from realtime database: %s' % (e))
        finally:
            connection.close()

        return UpdateChallenge(status='Challenge Updated: %s' % (id))





class Mutation(graphene.ObjectType):
    add_challenge = AddChallenge.Field()
    check_flag = CheckFlag.Field()
    delete_challenge = DeleteChallenge.Field()
    update_challenge = UpdateChallenge.Field()