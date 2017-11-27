"""ログ用モジュール."""
import logging.config

import settings


def get_my_logger(name):
    logging.config.dictConfig(settings.LOGGING_CONF)
    return logging.getLogger(name)


logger = get_my_logger(__name__)


if __name__ == '__main__':
    """my_loggingを試しに使ってみる."""
    logger.debug('DEBUGレベルです')
    logger.info('INFOレベルです')
    logger.warning('WARNINGレベルです')
    logger.error('ERRORレベルです')
    logger.critical('CRITICALレベルです')
