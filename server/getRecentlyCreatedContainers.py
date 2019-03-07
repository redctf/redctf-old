from portaineAPI import *
import argparse

# this wil receive a request from the API and assign the requesting user a cookie value.
# It will also spin up a new container to replace the one in reserve
# containers will be terminated after x amount of time TBD.

pt = portainer()

# program arguments
parser = argparse.ArgumentParser(description='Get Docker Service object by ID.')
parser.add_argument('endpointID', metavar='Portainer endpoint ID', help='The Portainer endpoint ID to get from.')
parser.add_argument('--limit', metavar='Limit results', help='Return this number of most recently created containers, including non-running ones.')
parser.add_argument('--label', metavar='Service Name Label', help='Service Name Label exact match')


args = parser.parse_args()

# execute update and report any exceptions
try:
    r = pt.getRecentlyCreatedContainers(args.endpointID, args.limit, args.label)
    r_dict = json.loads(r.text)[0]
    print json.dumps(r_dict, indent=2, sort_keys=True)
    IPv4 = r_dict.get("NetworkSettings", {}).get("Networks", {}).get("ingress", {}).get("IPAMConfig", {}).get("IPv4Address", {})
    print ("IPv4 Address of new Container: " + IPv4)


except Exception as ex:
    print('error: {0}').format(ex)
