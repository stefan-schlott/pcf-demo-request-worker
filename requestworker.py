import bmemcached
import config
import time
from multiprocessing.dummy import Pool as ThreadPool
import mysql.connector
import urllib2

if __name__ == '__main__':
    #print config.memcachedURL + ' ' + config.memcachedUsername + ' ' + config.memcachedPassword

    mc = bmemcached.Client(config.memcachedURL, config.memcachedUsername, config.memcachedPassword)

    #print mc.stats()


    while True:
        mc = bmemcached.Client(config.memcachedURL, config.memcachedUsername, config.memcachedPassword)

        workInProgress = mc.get('workInProgress')

        if workInProgress and workInProgress == 'True':
            destinationURL = mc.get('destinationURL')
            amountOfCalls = mc.get('amountOfCalls')
            timestamp = int(time.time())

            # database connection
            cnx = mysql.connector.connect(user=config.database_username, password=config.database_password,
                                          host=config.database_host, database=config.database_name)

            # initialize database line
            add_new_line = (timestamp,0,amountOfCalls)

            cursor = cnx.cursor()
            cursor.execute(config.SQL_INSERT_NEW, add_new_line)

            # commit and close database connection
            cnx.commit()
            cursor.close()
            cnx.close()

            # create the URL list
            finalURL = destinationURL+'?timestamp='+str(timestamp)
            urls = [finalURL] * int(amountOfCalls)
            #print urls

            # clean up memcached
            mc.delete('workInProgress')
            mc.delete('destinationURL')
            mc.delete('amountOfCalls')

            pool = ThreadPool(config.threadPoolSize)

            # launch the call threads
            results = pool.map(urllib2.urlopen, urls)

            # aggregate the results
            pool.close()
            pool.join()

            #print results
        else:
            # sleep until next round
            time.sleep(config.secondsToSleep)
