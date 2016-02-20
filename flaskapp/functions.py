import json
from uuid import uuid4

import redis

from flaskapp.constants import RedisConstants


def generate_random_session_id():
    """
    Generate a random string for unique session id.

    :return: Returns a unique uuid.
    """
    session_id = str(uuid4())
    r = _get_redis()
    if r.get(session_id) is None:
        return session_id
    else:
        generate_random_session_id()


def update_or_create_session(session_id, data=None):
    r = _get_redis()
    r.set(session_id, json.dumps(data))
    r.incr(RedisConstants.REDIS_SESSION_COUNTER)


def is_active_session(session_id):
    r = _get_redis()
    return r.get(session_id) is not None


def get_session_data(session_id):
    r = _get_redis()
    data = r.get(session_id)
    if data is None:
        return data
    return data.decode()


def _get_redis():
    return redis.StrictRedis(host=RedisConstants.REDIS_HOST,
                             port=RedisConstants.REDIS_PORT,
                             db=RedisConstants.REDIS_DB)
