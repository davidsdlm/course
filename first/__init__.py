import redis
from . import db


def init_redis(host: str, port: int, password: str):
    if db.redis_connection is None:
        db.redis_connection = redis.Redis(host=host, port=port, db=0, password=password)
    else:
        raise


def init_replica(host: str, port: int, name: str):

    db.redis_connection.lpush("web_app", name)
    db.redis_connection.hset(name, "host", host)
    db.redis_connection.hset(name, "port", port)