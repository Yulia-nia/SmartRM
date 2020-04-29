import logging


logger = logging.getLogger('SmartRM')
logger.setLevel(logging.WARNING)

logger_handler = logging.StreamHandler()
logger_handler.setLevel(logging.DEBUG)

logger_format = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')

logger_handler.setFormatter(logger_format)
logger.addHandler(logger_handler)


def main():
    module_logger = logging.getLogger('SmartRM')
    module_logger.debug(u'This is a debug message')
    module_logger.info(u'This is an info message')
    module_logger.warning(u'This is a warning')
    module_logger.error(u'This is an error message')
    module_logger.critical(u'FATAL!')


if __name__ == '__main__':
    main()
