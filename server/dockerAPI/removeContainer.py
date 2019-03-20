import argparse
from dockerAPI import *

d = dockerAPI()

# program arguments
parser = argparse.ArgumentParser(description='Delete a docker container by name')
parser.add_argument('containerName', metavar='container name', help='The container name to delete.')

args = parser.parse_args()

try:
	r = d.removeContainer(args.containerName)
	print(r)

except Exception as ex:
	print(ex)
