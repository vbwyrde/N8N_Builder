import os
import logging.config

LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'INFO',
        },
        'file_main': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(LOG_DIR, 'n8n_builder.log'),
            'maxBytes': 5 * 1024 * 1024,  # 5MB
            'backupCount': 5,
            'level': 'INFO',
            'encoding': 'utf8',
        },
        'file_error': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(LOG_DIR, 'errors.log'),
            'maxBytes': 5 * 1024 * 1024,  # 5MB
            'backupCount': 5,
            'level': 'ERROR',
            'encoding': 'utf8',
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file_main', 'file_error'],
            'level': 'INFO',
            'propagate': False,
        },
        'n8n_builder.iteration': {
            'handlers': ['console', 'file_main', 'file_error'],
            'level': 'INFO',
            'propagate': False,
        },
        'n8n_builder.performance': {
            'handlers': ['console', 'file_main', 'file_error'],
            'level': 'INFO',
            'propagate': False,
        },
        'n8n_builder.validation': {
            'handlers': ['console', 'file_main', 'file_error'],
            'level': 'INFO',
            'propagate': False,
        },
        'n8n_builder.llm': {
            'handlers': ['console', 'file_main', 'file_error'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'n8n_builder.project': {
            'handlers': ['console', 'file_main', 'file_error'],
            'level': 'INFO',
            'propagate': False,
        },
        'n8n_builder.filesystem': {
            'handlers': ['console', 'file_main', 'file_error'],
            'level': 'INFO',
            'propagate': False,
        },
        'n8n_builder.diff': {
            'handlers': ['console', 'file_main', 'file_error'],
            'level': 'INFO',
            'propagate': False,
        },
        'n8n_builder.retry': {
            'handlers': ['console', 'file_main', 'file_error'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG) 