import os

env = os.getenv('EKRYP_ENV', 'uat')

if env == 'prod':
	REDIS_HOST = "localhost"
	REDIS_PORT = 6379
	REDIS_CHARSET = "utf-8"
elif env == 'uat':
	REDIS_HOST = "localhost"
	REDIS_PORT = 6379
	REDIS_CHARSET = "utf-8"