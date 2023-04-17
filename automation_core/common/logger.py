import os
from logging.config import dictConfig

LEVEL_CONSOLE = os.environ.get("LOG_LEVEL_CONSOLE", 'INFO').upper()
LEVEL_FILE = os.environ.get("LOG_LEVEL_FILE", 'DEBUG').upper()


def setup_logging() -> None:
    package_name = __name__.split('.')[0]
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': (
                    '[%(asctime)s] [%(levelname)s] '
                    '[%(name)s.%(funcName)s:%(lineno)s] %(message)s'
                )
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': LEVEL_CONSOLE,
                # Redirect all console prints to stdout (especially from Agent.py),
                # since we tail that channel by ate.utils.ssh.execute():
                'stream': 'ext://sys.stdout',
            },
            'file': {
                'level': LEVEL_FILE,
                'formatter': 'standard',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': package_name + '.log',
                'mode': 'a',
                'maxBytes': 10 * 1024 * 1024,
                'backupCount': 5,
            },
        },
        'loggers': {
            '': {
                # Called external libs to log only to files, not on console, to avoid flooding it:
                'handlers': ['file'],
                'level': LEVEL_FILE,
                'propagate': True
            },
            package_name: {
                'handlers': ['console', 'file'],
                'level': LEVEL_CONSOLE,
                'propagate': False,
            },
        },
    }
    dictConfig(logging_config)
