from traefikAPI import *
import argparse

# this wil receive a request from the API and assign the requesting user a cookie value.
# It will also spin up a new container to replace the one in reserve
# containers will be terminated after x amount of time TBD.

tf = traefik()

# program arguments
parser = argparse.ArgumentParser(description='Get Docker Service object by ID.')
parser.add_argument('endpoint', metavar='Traefik endpoint', help='The traefik endpoint to get cookie from.')

args = parser.parse_args()

# execute update and report any exceptions
try:
    r = tf.getTraefikCookie(args.endpoint)
    print r.cookies

except Exception as ex:
    print('error: {0}').format(ex)
