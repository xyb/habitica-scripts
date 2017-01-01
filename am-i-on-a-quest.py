#!/usr/bin/env python

import argparse, os, requests, sys
parser = argparse.ArgumentParser(description="Are you on a quest with your party? Returns \"Yes\" or \"No\"")


class Debug(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        import pdb; pdb.set_trace()


# MAIN
parser.add_argument('-e','--error-code', \
                    action='store_true', \
                    help='Returns 0 or 1 rather than "Yes" of "No"')
# Set the environment variable HAB_API_USER to your User ID
# or set it via the '-u' argument
parser.add_argument('-u','--user-id', \
                    help='From https://habitica.com/#/options/settings/api')
# Set the environment variable HAB_API_TOKEN to your API token
# or set it via the '-k' argument
parser.add_argument('-k','--api-token', \
                    help='From https://habitica.com/#/options/settings/api')
# Set the Habitica URL (useful for testing local install)
parser.add_argument('--baseurl', \
                    help=argparse.SUPPRESS)
parser.add_argument('--debug', \
                    action=Debug, nargs=0, \
                    help=argparse.SUPPRESS)
args = parser.parse_args()

try:
    if args.user_id is not None:
        USR = args.user_id
    else:
        USR = os.environ['HAB_API_USER']
except KeyError:
    print "Environment variable 'HAB_API_USER' is not set"
    sys.exit(1)

try:
    if args.api_token is not None:
        KEY = args.api_token
    else:
        KEY = os.environ['HAB_API_TOKEN']
except KeyError:
    print "Environment variable 'HAB_API_TOKEN' is not set"
    sys.exit(1)

if args.baseurl is not None:
    URL = args.baseurl + "/api/v3/user"
else:
    URL = "https://habitica.com/api/v3/user"


headers = {"x-api-key":KEY,"x-api-user":USR,"Content-Type":"application/json"}

req = requests.get(URL, headers=headers)
if req.json()['data']['party']['quest']['key']:
    if args.error_code:
        sys.exit(0)
    else:
        print "Yes"
else:
    if args.error_code:
        sys.exit(1)
    else:
        print "No"