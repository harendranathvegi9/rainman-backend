from rainman.app import app

if not app.debug:
	import logging
	import logging.handlers

	if not os.path.exists(app.config['LOG_DIR']):
		os.makedirs(app.config['LOG_DIR'])

	handler = logging.handlers.RotatingFileHandler(
		app.config['LOG_FILENAME'], maxBytes=app.config['LOG_MAX_SIZE'], backupCount=app.config['LOG_MAX_NUM'])

	app.logger.setLevel(logging.DEBUG)
	app.logger.addHandler(handler)