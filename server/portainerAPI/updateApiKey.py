from portaineAPI import *
import argparse

"""
use this to update the API key for portainer 
"""

pt = portainer()

# program arguments
parser = argparse.ArgumentParser(description='update API key.')
parser.add_argument('username', metavar='Username', help='The username to get a key for')
parser.add_argument('password', metavar='Password', help='The password to use for auth')

args = parser.parse_args()

# execute update and report any exceptions
try:
    r = pt.getApiKey(args.username, args.password)
    print r.text

except Exception as ex:
    print('error: {0}').format(ex)