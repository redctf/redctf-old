import argparse
from dockerAPI import *

d = dockerAPI()

# program arguments
parser = argparse.ArgumentParser(description='Get Docker Service object by ID.')
parser.add_argument('user', metavar='username', help='The username to add the container to.')
parser.add_argument('imageName', metavar='image name', help='The username to add the container to.')
parser.add_argument('imageVersion', metavar='version', help='The username to add the container to.')
parser.add_argument('containerPorts', metavar='containerPorts', help='Must use port#/protocol:hostport (hostport can be None) - this is a dict')
parser.add_argument('protocol', metavar='protocol', help='Must use port#/protocol:hostport (hostport can be None) - this is a dict')
parser.add_argument('hostPort', metavar='hostPort', help='Must use port#/protocol:hostport (hostport can be None) - this is a dict')

l = d.listContainers()
print("running containers {}".format(l))


args = parser.parse_args()

containerPorts = args.containerPorts.split(",")
containerPortsProtocols = args.protocol.split(",")
hostPorts = args.containerPorts.split(",")
ports = []

# for i in range(len(containerPorts)):
# 	for protocol in containerPortsProtocols:
# 		for hostport in hostPorts:
# 			print(containerPorts[i])
# 			print(protocol)
# 			print(hostport)
# 			# ports[i] = "{0}/{1}:{2}".format(containerPorts[i], protocol, hostport)
# 			# print(ports[i])
# 			i += 1
print(d.version())
ports = "{\"80/tcp\":None, \"9090/tcp\":None}"
try:
	r = d.createContainer(args.containerName, "80", "natePathPrefix", args.user)
	print(r)
except Exception as ex:
	print(ex)

# d.removeContainer("traefik_{0}".format(args.containerName))
