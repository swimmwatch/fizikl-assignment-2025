import logging

import structlog
from django.conf import settings


def setup_logger():
    logging.config.dictConfig(settings.LOGGING)

    structlog.configure(
        processors=settings.PROCESSORS,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
