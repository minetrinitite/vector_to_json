import redis
import os


# def db_connection(host,port,db):
#     r = redis.StrictRedis(host=host, port=port, db=db)
#     return r

#this is the testing string to check if i can push to my own branchew

def put_in_db(full_path, host,port,db):
    
    f = open(full_path, 'rb')
    file = f.read()
    f.close()
    r = redis.StrictRedis(host=host, port=port, db=db)

    start_index = full_path.rfind('\\') + 1
    if start_index == -1:
        start_index = 0

    last_index = full_path.find('osm') - 1
    key = full_path[start_index:last_index]

    r.set(key, file)

    os.remove(key + '.osm.pbf')
    return key


def get_from_db(key, host,port,db):
    r = redis.StrictRedis(host=host, port=port, db=db)
    data = r.get(key)
    f = open(key + '.osm.pbf', 'wb')
    f.write(data)
    f.close()




