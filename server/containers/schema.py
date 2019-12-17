import graphene
import rethinkdb as r
from dockerAPI.dockerAPI import *
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from redctf.settings import RDB_HOST, RDB_PORT, CTF_DB
from containers.models import Container
from challenges.models import Challenge
from users.validators import validate_user_is_admin, validate_user_is_authenticated
from containers.validators import validate_name, validate_name_unique

d = dockerAPI()

class AddContainer(graphene.Mutation):
	status = graphene.String()

	class Arguments:
		name = graphene.String(required=True)

	def mutate(self, info, name):
		
		raise Exception('Not implemented yet')
		
		# user = info.context.user
		# image = info.context.image
		# port = info.context.port
		# path = info.context.path
		# # TODO: set this to take network parameter, if they want to do user isolation vs just container isolation
		# # net = info.context.net
		# net = 'false'
		# # Validate user is admin
		# validate_user_is_admin(user)

		# # Sanitize inputs
		# validate_name(name)
		# validate_name_unique(name)

		# # Save the container
		# container = Container(name=name)
		# container.save()

		# # Push the realtime data to rethinkdb
		# # TODO: does this need to be done?? Should it be a call to the systems instead?
		# connection = r.connect(host=RDB_HOST, port=RDB_PORT)
		# try:
		# 	r.db(CTF_DB).table('categories').insert(
		# 		{'sid': container.id, 'name': container.name, 'created': format(container.created, 'U')}).run(connection)
		# except RqlRuntimeError as e:
		# 	raise Exception('Error adding container to realtime database: %s' % (e))
		# finally:
		# 	connection.close()
		# # TODO: does this belong above the DB connection? It should log what the connection details are for the DB.
		# try:
		# 	dockerConnection = d.createContainer(username=user, imageName=image, port=port, pathPrefix=path, netIsolation=net)
		# except:
		# 	print('test error')

		return AddContainer(status='Container Created')

class GetUserContainer(graphene.Mutation):
	status = graphene.String()
	containerName = graphene.String()
	nextHop = graphene.String()

	class Arguments:
		challenge_id = graphene.Int(required=True) #sid from rethinkdb

	def mutate(self, info, challenge_id):
			
		user = info.context.user
		# Validate user is authenticated
		validate_user_is_authenticated(user)


		#does challenge exist with passed in challenge id?
		try:
			chall_obj = Challenge.objects.get(id__exact=challenge_id)
		except:
			raise Exception('Invalid Challenge ID')


		#look up container that belongs to logged in user for the associated challenge
		try:
			cont_obj = Container.objects.get(challenge__id__exact=challenge_id, user__exact=user)
		except:
			print('Container does not exist for user and/or challenge.  Attempt to create.')
			#if none exists create or assign one instead of raising exception

			try:
				new_cont_obj = d.createContainer(username=user, imageName=chall_obj.imageName, port=chall_obj.ports, pathPrefix=chall_obj.pathPrefix, containerType='http')
				print("############")
				print("name: {0}, \nimage: {1}, \nlabels: {2}, \nshort_id: {3}, \nstatus: {4}".format(new_cont_obj.name, new_cont_obj.image, new_cont_obj.labels, new_cont_obj.short_id, new_cont_obj.status))
				print("############")

			except Exception as ex:
				raise Exception('Unable to create container. Exception info: ' + str(ex) )

			# Save the container
			try:
				container = Container(name=new_cont_obj.name, challenge=chall_obj, user=user)
				container.save()
			except Exception as ex:
				raise Exception('Unable to save container. Exception info: ' + str(ex) )

			# Push the realtime data to rethinkdb
			connection = r.connect(host=RDB_HOST, port=RDB_PORT)
			try:
		 		r.db(CTF_DB).table('containers').insert(
		 		{'sid': container.id, 'name': container.name, 'challenge': container.challenge.id, 'user': container.user.id, 'created': format(container.created, 'U')}).run(connection)
			except RqlRuntimeError as e:
				raise Exception('Error adding container to realtime database: %s' % (e))
			finally:
			 	connection.close()
		
			#return CREATED container name (image_header) so header can be parsed out & return path prefix (in challenge model) as a next_hop
			return GetUserContainer(containerName=new_cont_obj.name, nextHop=chall_obj.pathPrefix, status='New Container Created for - challenge_id: ' + str(challenge_id) + ', user: ' + user.username)
		

		#return existing container name (image_header) so header can be parsed out & return path prefix (in challenge model) as a next_hop
		return GetUserContainer(containerName=cont_obj.name, nextHop=chall_obj.pathPrefix, status='Container Retrieved - challenge_id: ' + str(challenge_id) + ', container_id: ' + str(cont_obj.id) + ', user: ' + user.username)

		
class Mutation(graphene.ObjectType):
	add_container = AddContainer.Field()
	get_user_container = GetUserContainer.Field()