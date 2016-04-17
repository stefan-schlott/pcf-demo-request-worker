import json
import os
# determine environment (e.g. by looking for environment variable PYTHONHOME => /app/.heroku/python)

# local settings for local development (should stay out of GIT)
try:
    from local_config import *
except ImportError as e:
    pass

secondsToSleep=10

threadPoolSize=3

# SQL lines
SQL_INSERT_NEW=("INSERT INTO request_recorder "
               "(timestamp, current_request_count, max_possible_count) "
               "VALUES (%s, %s, %s);")

# production
if 'VCAP_SERVICES' in os.environ.keys():
    memcachedcloud_service = json.loads(os.environ['VCAP_SERVICES'])['memcachedcloud'][0]
    memcached_credentials = memcachedcloud_service['credentials']

    #print "Memcached_Credentials: "+str(memcached_credentials)

    memcachedURL=str(memcached_credentials['servers']).split(',')[0]
    memcachedUsername=str(memcached_credentials['username'])
    memcachedPassword=str(memcached_credentials['password'])

