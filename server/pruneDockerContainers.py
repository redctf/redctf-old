from portaineAPI import *
import argparse

# this wil receive a request from the API and assign the requesting user a cookie value.
# It will also spin up a new container to replace the one in reserve
# containers will be terminated after x amount of time TBD.

pt = portainer()

# program arguments
parser = argparse.ArgumentParser(description='Prune stopped Docker Containers.')
parser.add_argument('endpointID', metavar='Portainer endpoint ID', help='The Portainer endpoint ID to get from.')
args = parser.parse_args()

# execute update and report any exceptions
try:
    r = pt.pruneStoppedContainers(args.endpointID)
    print r.request.body


except Exception as ex:
    print('error: {0}').format(ex)
