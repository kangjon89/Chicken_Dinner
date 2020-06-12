# -*- coding: utf-8 -*-
"""
Like a tempory databese.
"""

try:
    import cPickle as pickle
except:
    import pickle
# Redis
import redis

redis_con = redis.StrictRedis(host='localhost', port=6379, db=0)

EXPIRE_TIME = 3 * 60 * 60

KEY_BASE = "TEST"


def set_value(key, value):
    """
    set the value (without overwriting)
    """
    my_key = KEY_BASE + key
    redis_con.set(my_key, pickle.dumps(value))
    redis_con.expire(my_key, EXPIRE_TIME)




def get_value(key):
    """
    get the value
    """
    my_key = KEY_BASE + key
    pickled_value = redis_con.get(my_key)
    if pickled_value is None:
        return None
    
    return pickle.loads(pickled_value)


def delete_value(key):
    """
    remove the value
    """
    my_key = KEY_BASE + key
    return redis_con.delete(my_key)


def exists(key):
    
    my_key = KEY_BASE + key
    return redis_con.exists(my_key)

def set_redis(token ,key, value):
    """
    set_value（）+ token
    """
    new_key = token + '_' + key
    set_value(new_key, value)

def get_redis(token ,key):
    """
    Key of get_value（）+ token
    """     
    new_key = token + '_' + key
    return get_value(new_key)
    
