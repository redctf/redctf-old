from portaineAPI import *
import argparse

# this wil receive a request from the API and assign the requesting user a cookie value.
# It will also spin up a new container to replace the one in reserve
# containers will be terminated after x amount of time TBD.

pt = portainer()

# program arguments
parser = argparse.ArgumentParser(description='Stop Docker Container by ID.')
parser.add_argument('endpointID', metavar='Portainer endpoint ID', help='The Portainer endpoint ID to get from.')
parser.add_argument('containerID', metavar='Docker Container ID', help='The Docker Container ID to stop.')
parser.add_argument('-d', '--scaleDown', help='Scale the docker service down by 1.', action='store_true')
parser.add_argument('-s', '--serviceID', required='--scaleDown', metavar='Docker Service ID', help='The Docker Service ID to scale down. Required if --scaleDown is selected.')
args = parser.parse_args()

# execute update and report any exceptions
try:
    r = pt.stopContainerByID(args.endpointID, args.containerID, args.scaleDown, args.serviceID)
    print r.request.body


except Exception as ex:
    print('error: {0}').format(ex)
