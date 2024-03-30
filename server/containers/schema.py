import graphene
import math
import threading
import rethinkdb as r
from dockerAPI.dockerAPI import *
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from redctf.settings import RDB_HOST, RDB_PORT, CTF_DB, MINIMUM_CONTAINER_COUNT, DEBUG
from containers.models import Container
from challenges.models import Challenge
from users.validators import validate_user_is_admin, validate_user_is_authenticated
from containers.validators import validate_name, validate_name_unique
from django.utils import timezone
from django.contrib.sessions.models import Session
from users.models import User

d = dockerAPI()


class GetUserContainer(graphene.Mutation):
    status = graphene.String()
    containerName = graphene.String()
    nextHop = graphene.String()

    class Arguments:
        challenge_id = graphene.Int(required=True)  # sid from rethinkdb

    def mutate(self, info, challenge_id):

        user = info.context.user
        # Validate user is authenticated
        validate_user_is_authenticated(user)

        # does challenge exist with passed in challenge id?
        try:
            chall_obj = Challenge.objects.get(id__exact=challenge_id)
        except:
            raise Exception('Invalid Challenge ID')

        # look up container that belongs to logged in user for the associated challenge
        try:
            cont_obj = Container.objects.get(
                challenge__id__exact=challenge_id, user__exact=user)
        except:
            print(
                'Container does not exist for user and/or challenge.  Attempt to create.')
            # if none exists create or assign one instead of raising exception

            try:
                try:
                    assigned_cont_obj = assignContainerToUser(
                        challenge_id, user.id)
                except:
                    assigned_cont_obj = newContainer(
                        challenge_id, user.id)
                    print("############")
                    print("name: {0}, \nimage: {1}, \nlabels: {2}, \nshort_id: {3}, \nstatus: {4}".format(
                        assigned_cont_obj.name, assigned_cont_obj.image, assigned_cont_obj.labels, assigned_cont_obj.short_id, assigned_cont_obj.status))
                    print("############")
            except Exception as ex:
                raise Exception(
                    'Unable to create container. Exception info: ' + str(ex))

            # return CREATED container name (image_header) so header can be parsed out & return path prefix (in challenge model) as a next_hop
            return GetUserContainer(containerName=assigned_cont_obj.name, nextHop=chall_obj.pathPrefix, status='New Container Created for - challenge_id: ' + str(challenge_id) + ', user: ' + user.username)

        # return existing container name (image_header) so header can be parsed out & return path prefix (in challenge model) as a next_hop
        return GetUserContainer(containerName=cont_obj.name, nextHop=chall_obj.pathPrefix, status='Container Retrieved - challenge_id: ' + str(challenge_id) + ', container_id: ' + str(cont_obj.id) + ', user: ' + user.username)


class ScaleAllChallenges(graphene.Mutation):
    status = graphene.String()

    def mutate():
        user = info.context.user
        # Validate user is admin
        validate_user_is_admin(user)

        return ScaleAllChallenges(status='all challenges scaled')


class ScaleChallenge(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        challenge_id = graphene.Int(required=True)

    def mutate(self, info, challenge_id):
        user = info.context.user
        # Validate user is admin
        validate_user_is_admin(user)

        # TODO: validate input

        if Challenge.objects.filter(id=challenge_id):
            print('valid challenge')

            registeredUsers = getRegisteredUserCount()
            active_uid_list = getActiveSessions()

            scaleChallenge(challenge_id,
                           registeredUsers, active_uid_list)

        else:
            print('invalid challenge')

        return ScaleChallenge(status='challenge scaled')


def getActiveSessions():
    try:
        sessions = Session.objects.filter(expire_date__gte=timezone.now())

        uid_list = []
        # I noticed this might return users who refreshed the page but didn't click logout.
        for session in sessions:
            data = session.get_decoded()
            auid = data.get('_auth_user_id', None)
            if auid not in uid_list:
                uid_list.append(auid)

        return uid_list

    except Exception as ex:
        raise(ex)


def assignContainerToUser(challenge_id, userID):

    user = User.objects.get(id=userID)
    nullContainers = getNullContainers(challenge_id)
    registeredUsers = getRegisteredUserCount()
    active_uid_list = getActiveSessions()
    # scaleChallenge(self, challenge_id, registeredUsers, active_uid_list)
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)

    if len(nullContainers) == 0:
        try:
            # TODO: should we scale then assign or should we build one then scale.
            scaleChallenge(challenge_id,
                           registeredUsers, active_uid_list)

        except:
            raise Exception('unknown issue with scaling nullContainers')

    try:
        assigned_cont_obj = Container.objects.get(id=nullContainers[0].id)
        assigned_cont_obj.user = user
        assigned_cont_obj.save()
        try:

            rethinkContainers = r.db(CTF_DB).table('containers').filter(
                {'sid': assigned_cont_obj.id}).run(connection)
            # use for loop to access the object(s) values and assign to team id variable
            for rethink_container in rethinkContainers:
                    # print(rethink_team['id'])
                rethink_container_id = rethink_container['id']
            # update rethinkdb entry
            update = r.db(CTF_DB).table('containers').get(
                rethink_container_id).update({'user': userID}).run(connection)

        except RqlRuntimeError as e:
            raise Exception(
                'Error deleting container from realtime database: %s' % (e))

    except:
        print('error assigning user an existing container - creating new container to be assigned.')
        assigned_cont_obj = newContainer(challenge_id, userID)

    finally:
        connection.close()

    threadedScaleAllChallenges()


    return assigned_cont_obj


def getRegisteredUserCount():
    try:
        registeredUserCount = User.objects.count()
        return registeredUserCount

    except Exception as ex:
        print(ex)


def getAllChallengeIDs():

    try:
        challengeIDs = Challenge.objects.all()
        return challengeIDs
    except Exception as ex:
        print(ex)


def getAssignedContainers(challenge_id):
    activeContainers = Container.objects.filter(
        challenge__id=challenge_id).exclude(user__id=None)

    return activeContainers


def getAllContainersByChallengeID(challenge_id):
    containers = Container.objects.filter(
        challenge__id=challenge_id)

    return containers


def threadedScaleAllChallenges():
    scale = threading.Thread(target=scaleAllChallenges)
    scale.start()
    print('thread started')

    return


def scaleAllChallenges():

    registeredUsers = getRegisteredUserCount()
    active_uid_list = getActiveSessions()

    challengeIDs = Challenge.objects.exclude(hosted=False)
    for challenge in challengeIDs:
        print('scaling challenge # {0}'.format(challenge.id))
        scaleChallenge(challenge.id,
                       registeredUsers, active_uid_list)
    return


def scaleChallenge(challenge_id, registeredUsers, active_uid_list):

    assignedContainers = getAssignedContainers(challenge_id)
    activeSessionCount = len(active_uid_list)
    activeContainerCount = len(assignedContainers)

    buffer = calculateBuffer(registeredUsers, activeSessionCount,
                             MINIMUM_CONTAINER_COUNT, activeContainerCount, challenge_id)
    challengeContainers = getAllContainersByChallengeID(challenge_id)
    challengeContainerCount = len(challengeContainers)
    nullContainers = getNullContainers(challenge_id)
    nullContainerCount = len(nullContainers)

    # buffer is total number of containers required based upon calculateBuffer
    # MINIMUM_CONTAINER_COUNT is the minimum number of spare containers (assigned to null)
    # ensure we have enough total containers per challenge as well as at least the MINIMUM_CONTAINER_COUNT

    if buffer > challengeContainerCount:
        while buffer > challengeContainerCount:
            newContainer(challenge_id)
            challengeContainerCount = len(getAllContainersByChallengeID(
                challenge_id))
            # this is used in the next if statement
            nullContainerCount = len(getNullContainers(challenge_id))

    # ensure we remove extra containers per challenge buffer calculation as well as at least the MINIMUM_CONTAINER_COUNT
    # elif buffer < challengeContainerCount and nullContainerCount > MINIMUM_CONTAINER_COUNT:
    #     while buffer < challengeContainerCount:
        
    #         if nullContainerCount > MINIMUM_CONTAINER_COUNT and nullContainerCount > 0:
    #             removeContainer(nullContainers[nullContainerCount-1])
    #             challengeContainerCount = len(getAllContainersByChallengeID(
    #                 challenge_id))
    #             nullContainers = getNullContainers(challenge_id)
    #         else:
    #             raise Exception('error with removing containers')
            
    elif buffer < challengeContainerCount:
        while buffer < challengeContainerCount:
        
            if nullContainerCount > 0:
                removeContainer(nullContainers[nullContainerCount-1])
                challengeContainerCount = len(getAllContainersByChallengeID(
                    challenge_id))
                nullContainers = getNullContainers(challenge_id)
            else:
                raise Exception('error with removing containers')

    elif buffer == challengeContainerCount:
        print('Correct # of containers according to buffer logic')

    else:
        raise Exception('error scaling container')

    return


def getNullContainers(challenge_id):
    nullContainers = Container.objects.filter(
        challenge__id=challenge_id).filter(user_id=None)
    return nullContainers


def removeAllContainers():
    # TODO: do I need this?

    return


def removeContainer(containerObject):
    print('deleting container')

    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    containerName = containerObject.name
    challenge_id = containerObject.challenge_id
    nullContainers = getNullContainers(challenge_id)
    registeredUsers = getRegisteredUserCount()
    active_uid_list = getActiveSessions()

    try:
        delete = d.removeContainer(containerName)
        if delete is not None:
            raise Exception(' error deleting container in docker')
        else:
            try:
                # delete rethinkdb entry
                rethinkContainers = r.db(CTF_DB).table('containers').filter(
                    {'sid': containerObject.id}).run(connection)
                # use for loop to access the object(s) values and assign to team id variable
                for rethink_container in rethinkContainers:
                    # print(rethink_team['id'])
                    rethink_container_id = rethink_container['id']

                rethinkDelete = r.db('redctf').table(
                    'containers').get(rethink_container_id).delete().run(connection)
            except RqlRuntimeError as e:
                raise Exception(
                    'Error deleting container from realtime database: %s' % (e))
            containerObject.delete()

    finally:
        connection.close()
    # try:
    #     scaleChallenge(self, challenge_id, registeredUsers, active_uid_list)
    # except:
    #     raise Exception('unknown issue with scaling nullContainers')

    status = 'deleted container: {0}'.format(containerName)
    return status


def calculateBuffer(registeredUsers, activeSessions, minimumContainers, activeContainers, challenge_id):

    # buf = registeredUsers, activeSessions, minimumContainers, activeContainers, challenge

    buffer = activeContainers + \
        ((0.2 * (activeSessions - activeContainers)) +
         (0.05 * (registeredUsers - activeSessions)))

    # if math.ceil(buffer) < minimumContainers:
    #     roundedBuffer = minimumContainers
    #     print("buffer = {0} < minimimumContainers = {1} - using minimum amount of containers instead".format(
    #         buffer, roundedBuffer))
    # else:
    #     roundedBuffer = math.ceil(buffer)

    #     print("buffer = {0}, rounded up to nearest int = {1}".format(
    #         buffer, roundedBuffer))
    #
    roundedBuffer = math.ceil(buffer)
    nullContainerCount = len(getNullContainers(challenge_id))

    # if buffer is lower than # of minimum containers then increase
    # if roundedBuffer < minimumContainers:
    #     while roundedBuffer < minimumContainers:
    #         roundedBuffer += 1

    # if nullContainerCount < minimumContainers:
    #     roundedBuffer += abs(nullContainerCount - minimumContainers)

    print("buffer = {0}, rounded up to nearest int = {1}".format(
        buffer, roundedBuffer))

    return roundedBuffer


def newContainer(challenge_id, userID=None):

    if DEBUG:
        setContainerType = 'http'
    else:
        setContainerType = 'https'

    chall_obj = Challenge.objects.get(id=challenge_id)
    if userID is not None:
        user = User.objects.get(id=userID)
        try:
            new_cont_obj = d.createContainer(
                imageName=chall_obj.imageName,
                runtime=chall_obj.runtime,
                port=chall_obj.ports, pathPrefix=chall_obj.pathPrefix, containerType=setContainerType,
                username=user.username)
            print("############")
            print("name: {0}, \nimage: {1}, \nlabels: {2}, \nshort_id: {3}, \nstatus: {4}".format(
                new_cont_obj.name, new_cont_obj.image, new_cont_obj.labels, new_cont_obj.short_id, new_cont_obj.status))
            print("############")
            rethinkUsername = user.id

        except Exception as ex:
            raise Exception(
                'Unable to create container. Exception info: ' + str(ex))
    else:

        try:
            new_cont_obj = d.createContainer(
                imageName=chall_obj.imageName,
                runtime=chall_obj.runtime,
                port=chall_obj.ports, pathPrefix=chall_obj.pathPrefix, containerType=setContainerType)
            print("############")
            print("name: {0}, \nimage: {1}, \nlabels: {2}, \nshort_id: {3}, \nstatus: {4}".format(
                new_cont_obj.name, new_cont_obj.image, new_cont_obj.labels, new_cont_obj.short_id, new_cont_obj.status))
            print("############")
            user = None
            rethinkUsername = None

        except Exception as ex:
            raise Exception(
                'Unable to create container. Exception info: ' + str(ex))

    # Save the container
    try:
        container = Container(
            name=new_cont_obj.name, challenge=chall_obj, user=user)
        container.save()
    except Exception as ex:
        raise Exception(
            'Unable to save container. Exception info: ' + str(ex))

    # Push the realtime data to rethinkdb
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db(CTF_DB).table('containers').insert(
            {'sid': container.id, 'name': container.name, 'challenge': container.challenge.id, 'user': rethinkUsername, 'created': format(container.created, 'U')}).run(connection)
    except RqlRuntimeError as e:
        raise Exception(
            'Error adding container to realtime database: %s' % (e))
    finally:
        connection.close()

    return new_cont_obj


class Mutation(graphene.ObjectType):
    get_user_container = GetUserContainer.Field()
    scale_challenge = ScaleChallenge.Field()
    scale_all_challenges = ScaleAllChallenges.Field()
