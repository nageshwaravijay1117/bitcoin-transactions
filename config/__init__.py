"""
==========================================
Author:Nageshwara Vijay
Created-At:15-09-2019
Last-Modified:17-09-2019
==========================================
"""
import os

env = os.getenv('BITCOIN_ENV', 'uat')

if env == 'prod':
	REDIS_HOST = "localhost"
	REDIS_PORT = 6379
	REDIS_CHARSET = "utf-8"
elif env == 'uat':
	REDIS_HOST = "localhost"
	REDIS_PORT = 6379
	REDIS_CHARSET = "utf-8"