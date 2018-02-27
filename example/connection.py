import os
import redis


redis_url = os.getenv('REDIS_URL')
if not redis_url:
    raise RuntimeError('Missing REDIS_URL')

pool = redis.ConnectionPool().from_url(redis_url, db=0)
redis_client = redis.Redis(connection_pool=pool)
