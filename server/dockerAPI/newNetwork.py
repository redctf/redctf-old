from network import *
import docker

client = docker.client.from_env()
name = 'nate-test1'

create_network(client,name)


