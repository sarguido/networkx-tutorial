from sys import argv

from client import tapi, dapi
from client import config

args = argv[1:]

actions = ['get','summary']

if len(args) < 2 or args[0] not in actions or args[1] not in config.RESOURCE:
    print 'action options:', actions
    print 'resource options:', config.RESOURCE.keys()
    exit(1)

action = args[0]
resource = config.RESOURCE[args[1]]

resource_params = args[2:]
params = {}
if resource_params:
    params
    for p in resource_params:
        pair = p.split("=")
        value = pair[1]
        if value == 'None':
            value = None
        params[pair[0]] = value

if not params and 'last' in params:
    params = tapi.get_next_params(resource, params)

# check fields
missing_fields = [field for field in resource['filename_fields']
                  if field not in params
                  and field not in resource['summarize_filename_prefix']]

if missing_fields:
    print "required resource params:", ','.join(missing_fields)
    exit(1)

dapi.adjust_inputs(resource, params)

if action == 'get':
    summary, data = tapi.get_resource(resource=resource, params=params)
elif action == 'summary':
    dapi.summarize_items(resource=resource, params=params)
