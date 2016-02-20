from flaskapp import app


class RedisConstants:
    REDIS_HOST = app.config.get('REDIS_HOST')
    REDIS_PORT = app.config.get('REDIS_PORT')
    REDIS_DB = app.config.get('REDIS_DB')
    REDIS_SESSION_COUNTER = "total_sessions"


class UIConstants:
    USERNAME_INVALID = "A name is required."
