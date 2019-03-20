import argparse
from dockerAPI import *

d = dockerAPI()

# program arguments
parser = argparse.ArgumentParser(description='Initialize user')
parser.add_argument('user', metavar='username', help='The username to initialize.')
args = parser.parse_args()

username = args.user
d.createTraefikContainer()
try:
	r = d.createNetwork(username)
	print(r)
	net = d.getNetworkObject(username)
	print(net.attrs)
	# connect traefik container to newly create user network
	connect = d.connectNetwork(username, 'traefik')
	print(connect)
except Exception as ex:
	print(ex)
