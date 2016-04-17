import json
import os
# determine environment (e.g. by looking for environment variable PYTHONHOME => /app/.heroku/python)

# local settings for local development (should stay out of GIT)
try:
    from local_config import *
except ImportError as e:
    pass

secondsToSleep=10

threadPoolSize=12

# SQL lines
SQL_INSERT_NEW=("INSERT INTO request_recorder "
               "(timestamp, current_request_count, max_possible_count) "
               "VALUES (%s, %s, %s);")

# production
if 'VCAP_SERVICES' in os.environ.keys():
    # Memcached
    memcachedcloud_service = json.loads(os.environ['VCAP_SERVICES'])['memcachedcloud'][0]
    memcached_credentials = memcachedcloud_service['credentials']

    memcachedURL = str(memcached_credentials['servers']).split(',')[0]
    memcachedUsername = str(memcached_credentials['username'])
    memcachedPassword = str(memcached_credentials['password'])

    # MySQL database (ClearDB)
    cleardb_service = json.loads(os.environ['VCAP_SERVICES'])['cleardb'][0]
    cleardb_credentials = cleardb_service['credentials']

    database_host = str(cleardb_credentials['hostname'])
    database_name = str(cleardb_credentials['name'])
    database_username = str(cleardb_credentials['username'])
    database_password = str(cleardb_credentials['password'])

