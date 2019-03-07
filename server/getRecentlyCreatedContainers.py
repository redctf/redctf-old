from portaineAPI import *
import argparse, itertools

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
    i = 0
    r_list = json.loads(r.text)

    for container in r_list:
        IPv4 = container.get("NetworkSettings", {}).get("Networks", {}).get("ingress", {}).get("IPAMConfig", {}).get("IPv4Address", {})
        name = container.get("Names", {})[0]
        id = container.get("Id")
        print ("container name: \"{0}\", container ID: {1}, IPv4 address: {2} ".format(name, id, IPv4))
        #print ("IPv4 address of container: {0}".format(IPv4))
        i += 1
    print ('total number of containers: ' + str(i))

except Exception as ex:
    print('error: {0}').format(ex)
