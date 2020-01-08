import argparse
from dockerAPI import *

d = dockerAPI()

# program arguments
parser = argparse.ArgumentParser(description='Initialize user')
parser.add_argument('user', metavar='username', help='The username to initialize.')
args = parser.parse_args()

username = args.user
# d.createTraefikContainer()
try:
	r = d.createNetwork(username)
	print("created network {0}".format(r))
	# net = d.getNetworkObject(username)
	# if net is False:
	# 	print("network doesnt exist")
	# print(net.attrs)
	# connect traefik container to newly created user network
	connect = d.connectNetwork(username, 'traefik')
	print(connect)
except Exception as ex:
	print(ex)
