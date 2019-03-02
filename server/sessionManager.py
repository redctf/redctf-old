from sessionManagerRedCTF import *

# this wil receive a request from the API and assign the requesting user a cookie value.
# It will also spin up a new container to replace the one in reserve
# containers will be terminated after x amount of time TBD.
import argparse, json

pt = portainerAPI()
tf = traefik()
# program arguments
# parser = argparse.ArgumentParser(description='update stack thing.')
# # parser.add_argument('endpoint', metavar='API Endpoint', help='The API endpoint to communicate with.')
# # parser.add_argument('http', metavar='HTTP request', help='The HTTP request to use (GET, POST, PUT, DELETE, Etc).')
# #
# # args = parser.parse_args()
# # create list to process multiple hosts, replace any spaces in hostname list
# host_list = args.host.replace(" ", "")
# endpoint = args.endpoint

# execute update and report any exceptions
try:
    r = pt.getDockerServices()
    #r = tf.getTraefikCookie()
    print r.text
    #print r.cookies

except Exception as ex:
    print('error: {0}').format(ex)




