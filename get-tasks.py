#!/usr/bin/env python

import argparse, json, os, requests, sys
parser = argparse.ArgumentParser(description="Dumps your tasks to a file hab_tasks.json in the current directory")


class Debug(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        import pdb; pdb.set_trace()


# MAIN
# Set the environment variable HAB_API_USER to your User ID
# or set it via the '-u' argument
parser.add_argument('-u','--user-id', \
                    help='From https://habitica.com/#/options/settings/api')
# Set the environment variable HAB_API_TOKEN to your API token
# or set it via the '-k' argument
parser.add_argument('-k','--api-token', \
                    help='From https://habitica.com/#/options/settings/api')
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


headers = {"x-api-key":KEY,"x-api-user":USR,"Content-Type":"application/json"}

req = requests.get("https://habitica.com/api/v3/tasks/user", headers=headers)
with open('hab_tasks.json', 'w') as f:
    json.dump(req.json(),f,separators=(',',':'),sort_keys=True)
