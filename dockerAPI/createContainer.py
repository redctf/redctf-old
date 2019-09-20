import argparse
from dockerAPI import *

d = dockerAPI()

# program arguments
parser = argparse.ArgumentParser(description='Get Docker Service object by ID.')
parser.add_argument('--containerName', metavar='container name', help='Optional - container name if not using network isolation')
parser.add_argument('user', metavar='username', help='The username to add the container to.')
parser.add_argument('imageName', metavar='image name', help='The image and version to use.')
parser.add_argument('ports', metavar='ports', help='Must use port#/protocol:hostport (hostport can be None) - this is a dict')
parser.add_argument('--pathPrefix', metavar='pathPrefix', help='Path prefix for traefik reverse proxy: \'hello\' is an example - don\'t use leading forward slash.')
parser.add_argument('--netIsolation', help='include flag if using network isolation per user', action='store_true')

args = parser.parse_args()
# port format - for static argument.
# ports = "{\"80/tcp\":None, \"9090/tcp\":None}"

try:
	r = d.createContainer(args.user, args.imageName, args.ports, args.containerName, args.pathPrefix, args.netIsolation)
	#print(r.attrs)
	print("############")
	print("name: {0}, \nimage: {1}, \nlabels: {2}, \nshort_id: {3}, \nstatus: {4}".format(r.name, r.image, r.labels, r.short_id, r.status))
	print("############")


except Exception as ex:
	print(ex)

# python C:\Users\Nate\git-repos\redctf\dockerAPI\createContainer.py nate tutum/hello-world:latest 80 --containerName testName --pathPrefix hello