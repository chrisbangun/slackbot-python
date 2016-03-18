import os

DEBUG = True

PLUGINS = [
    'slackbot.plugins',
    
]

API_TOKEN = 'Your slackbot token from SLACK'

for key in os.environ:
    if key[:9] == 'SLACKBOT_':
        name = key[9:]
        globals()[name] = os.environ[key]

try:
    from slackbot_settings import *
except ImportError:
    try:
        from local_settings import *
    except ImportError:
        pass

