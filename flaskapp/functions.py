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
    """
    Updating or Creating a new key in redis for particular session id

    :param session_id: Key for storing data in redis
    :param data: Data to be stored in redis for given session id
    :return:
    """
    r = _get_redis()
    r.set(session_id, json.dumps(data))
    r.incr(RedisConstants.REDIS_USAGE_COUNTER)
    if data is None:
        r.incr(RedisConstants.REDIS_SESSION_COUNTER)


def is_active_session(session_id):
    r = _get_redis()
    return r.get(session_id) is not None


def remove_session_data(session_id):
    r = _get_redis()
    if is_active_session(session_id=session_id):
        r.delete(session_id)
        return True
    return False


def get_session_data(session_id):
    r = _get_redis()
    data = r.get(session_id)
    if data is None:
        return data
    return data.decode()


def get_level_name(level_id):
    r = _get_redis()
    data = r.get("level_%s" % level_id)
    return json.loads(data.decode()).get('level_name')


def _get_redis():
    return redis.StrictRedis(host=RedisConstants.REDIS_HOST,
                             port=RedisConstants.REDIS_PORT,
                             db=RedisConstants.REDIS_DB)
