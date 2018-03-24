import redis

"""
def db_connection(host,port,db):
    r = redis.StrictRedis(host=host, port=port, db=db)
    return r
"""

def put_in_db(full_path, host,port,db):
    print(full_path)
    f = open(full_path, 'rb')
    file = f.read()

    r = redis.StrictRedis(host=host, port=port, db=db)

    start_index = full_path.rfind('\\') + 1
    if start_index == -1:
        start_index = 0

    last_index = full_path.find('osm') - 1
    key = full_path[start_index:last_index]

    r.set(key, file)

    return key


def get_from_db(key, host,port,db):


    r = redis.StrictRedis(host=host, port=port, db=db)
    r.get(key)

    print(r.get(key))



