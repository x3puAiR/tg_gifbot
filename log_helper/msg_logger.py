''''''

import logging


class MsgLogger():
    """Logger utility for bot messages with console and file handlers."""

    def __init__(self,
                 log_name='gifbot',
                 log_file='.app_cache/telegram.log'):
        """Initialize the message logger with specified name and file path."""
        self.log_name = log_name
        self.log_file = log_file
        # self.fmt = '%(asctime)s - %(levelname)s - %(message)s'
        self.fmt = '[%(asctime)s] %(filename)s:%(lineno)d: %(levelname)s: %(message)s'
        self.formatter = logging.Formatter(fmt=self.fmt, datefmt=r'%Y-%m-%d %H:%M:%S')

    def get_logger(self):
        """Get or create a logger instance with console and file handlers."""
        logger = logging.getLogger(self.log_name)
        logger.setLevel(logging.DEBUG)
        # console handler
        console_hdlr = logging.StreamHandler()
        console_hdlr.setLevel(logging.DEBUG)
        console_hdlr.setFormatter(self.formatter)
        # file handler with UTF-8 encoding to handle Unicode characters
        file_hdlr = logging.FileHandler(self.log_file, encoding='utf-8')
        file_hdlr.setLevel(logging.INFO)
        file_hdlr.setFormatter(self.formatter)
        # add handlers
        if not logger.handlers:
            logger.addHandler(console_hdlr)
            logger.addHandler(file_hdlr)
        return logger


if __name__ == '__main__':
    pass
