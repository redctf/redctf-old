from portaineAPI import *
import argparse

# this wil receive a request from the API and assign the requesting user a cookie value.
# It will also spin up a new container to replace the one in reserve
# containers will be terminated after x amount of time TBD.

pt = portainer()

# program arguments
parser = argparse.ArgumentParser(description='Get Docker Service object by ID.')
parser.add_argument('endpointID', metavar='Portainer endpoint ID', help='The Portainer endpoint ID to get from.')
parser.add_argument('serviceID', metavar='Docker Service ID', help='The Docker Service ID to get.')
parser.add_argument('replicas', metavar='Docker Service Replica count', help='The Docker Service number of replicas.')
args = parser.parse_args()

# execute update and report any exceptions
try:
    r = pt.updateDockerServiceByID(args.endpointID, args.serviceID, args.replicas)
    print r.text

except Exception as ex:
    print('error: {0}').format(ex)




