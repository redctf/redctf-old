import argparse
from dockerAPI import *

d = dockerAPI()

# program arguments
parser = argparse.ArgumentParser(description='Get Docker Service object by ID.')
parser.add_argument('user', metavar='username', help='The username to add the container to.')
parser.add_argument('imageName', metavar='image name', help='The image and version to use.')
parser.add_argument('ports', metavar='ports', help='Must use port#/protocol:hostport (hostport can be None) - this is a dict')
parser.add_argument('--pathPrefix', metavar='pathPrefix', help='Path prefix for traefik reverse proxy: \'hello\' is an example - don\'t use leading forward slash.')

args = parser.parse_args()
# port format - for static argument.
# ports = "{\"80/tcp\":None, \"9090/tcp\":None}"

try:
	r = d.createContainer(args.user, args.imageName, args.ports, args.pathPrefix)
	print(r.attrs)

except Exception as ex:
	print(ex)

