from rainman.app import app
import os

class Config(object):
	PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),'..', '..'))
	DEBUG = False
	LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')
	LOG_FILENAME = os.path.join(LOG_DIR, 'app.log')
	LOG_MAX_SIZE = 100*1024*1024 # 100MB
	LOG_MAX_NUM = 10

class ProductionConfig(Config):
	DEBUG = False

class DevelopmentConfig(Config):
	DEBUG = True

app.config.from_object(DevelopmentConfig)