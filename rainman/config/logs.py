"""
Logging setup for the production environment
"""
from rainman.app import app

# Dev environments send debug info to STDOUT
if not app.debug:
    import logging
    import logging.handlers

    # create log dir if it doesn't exist
    if not os.path.exists(app.config['LOG_DIR']):
        os.makedirs(app.config['LOG_DIR'])

    # Rotate log files after they reach a certain size
    # `LOG_FILENAME` is always most recent
    # `LOG_FILENAME`.n is last
    handler = logging.handlers.RotatingFileHandler(
        app.config['LOG_FILENAME'], maxBytes=app.config['LOG_MAX_SIZE'],
        backupCount=app.config['LOG_MAX_NUM'])

    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)