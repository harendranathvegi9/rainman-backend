"""
Config setup & settings corresponding to different environments
"""
from rainman.app import app
import os

# Base config object: all environments inherit from these settings
class Config(object):
	DEBUG = False
	# Project root, calculated in relation to this file
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')
    LOG_FILENAME = os.path.join(LOG_DIR, 'app.log')
    LOG_MAX_SIZE = 100*1024*1024 # 100MB
    # Number of log files for the rotating handler to keep on disk
    LOG_MAX_NUM = 10

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

# TODO: Config for different environments based on environment vars
app.config.from_object(DevelopmentConfig)