from uuid import uuid4

import redis

from flaskapp.constants import RedisConstants


def generate_random_session_id():
    """
    Generate a random string for unique session id.
    TODO Add check in database

    :return: Returns a unique uuid.
    """
    return str(uuid4())


def update_or_create_session(session_id, data=None):
    r = get_redis()
    r.set(session_id, data)
    r.incr(RedisConstants.REDIS_SESSION_COUNTER)


def get_session_data(session_id):
    r = get_redis()
    return r.get(session_id)


def get_redis():
    return redis.StrictRedis(host=RedisConstants.REDIS_HOST, port=RedisConstants.REDIS_PORT, db=RedisConstants.REDIS_DB)
