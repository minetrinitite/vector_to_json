import redis
import os


# def db_connection(host,port,db):
#     r = redis.StrictRedis(host=host, port=port, db=db)
#     return r

#this is the testing string to check if i can push to my own branchew

def init_redis(host,port,db):
    r = redis.StrictRedis(host=host, port=port, db=db)
    return r

def put_in_db(full_path, redis):
    
    f = open(full_path, 'rb')
    file = f.read()
    f.close()

    start_index = full_path.rfind('\\') + 1
    if start_index == -1:
        start_index = 0

    last_index = full_path.find('osm') - 1
    key = full_path[start_index:last_index]

    redis.set(key, file)

    os.remove(key + '.osm.pbf')
    return key


def get_from_db(key, redis):
    data = redis.get(key)
    f = open(key + '.osm.pbf', 'wb')
    f.write(data)
    f.close()
    return key + ".osm.pbf"

def get_from_db_data(key, redis):
    return redis.get(key)



