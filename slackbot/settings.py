import os

DEBUG = True

PLUGINS = [
    'slackbot.plugins',
    
]

API_TOKEN = 'xoxb-20180334097-HwORZoVQ5qgJM24lMzSIkzja'

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

