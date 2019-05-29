from portaineAPI import *
import argparse

# this wil receive a request from the API and assign the requesting user a cookie value.
# It will also spin up a new container to replace the one in reserve
# containers will be terminated after x amount of time TBD.

pt = portainer()

# program arguments
parser = argparse.ArgumentParser(description='update stack thing.')
parser.add_argument('endpointID', metavar='Portainer endpoint ID', help='The Portainer endpoint ID to get from.')
parser.add_argument('serviceID', metavar='Docker Service ID', help='The Docker Service ID to get.')

args = parser.parse_args()

# execute update and report any exceptions
try:
    r = pt.getDockerServicesByID(args.endpointID, args.serviceID)
    r_dict = json.loads(r.text)
    print json.dumps(r_dict, indent=2, sort_keys=True)

except Exception as ex:
    print('error: {0}').format(ex)




