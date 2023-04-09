import redis
from . import db
from apscheduler.schedulers.background import BackgroundScheduler


def init_redis(host: str, port: int, password: str):
    if db.redis_connection is None:
        db.redis_connection = redis.Redis(host=host, port=port, db=0, password=password)
    else:
        raise


def close_redis():
    if db.redis_connection is None:
        return
    else:
        db.redis_connection = None


def init_replica(host: str, port: int, name: str, expire_time: float):

    db.redis_connection.hset(name, "host", host)
    db.redis_connection.hset(name, "port", port)
    db.redis_connection.expire(name, expire_time + 1)


def some_job():
    print("send hash")


def init_scheduler(interval, *args):
    if db.redis_hash_scheduler is None:
        db.redis_hash_scheduler = BackgroundScheduler(job_defaults={'max_instances': 2})
        db.redis_hash_scheduler.add_job(init_replica, args=args, trigger='interval', seconds=interval)
        db.redis_hash_scheduler.start()
    else:
        raise


def shutdown_scheduler():
    if db.redis_hash_scheduler is None:
        raise
    else:
        db.redis_hash_scheduler.shutdown()
