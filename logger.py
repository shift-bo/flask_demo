# coding=utf-8

import logging


class LogHandler(object):
    """日志"""
    @classmethod
    def get_fmt(cls):
        fmt = '[%(levelname)s] [%(asctime)s] [File: %(filename)s] [Line: %(lineno)d] Message: %(message)s'
        formatter = logging.Formatter(fmt)
        formatter.datefmt = '%Y%m%d %H:%M:%S'
        return formatter

    @classmethod
    def _get_handler(cls, log_name, level='INFO'):
        log_file_name = '{}.log' if level == 'INFO' else '{}-error.log'
        log_file_name = log_file_name.format(log_name)
        return logging.FileHandler(log_file_name)

    @classmethod
    def get_handler(cls, log_name):
        handler = cls._get_handler(log_name)
        handler.setLevel(logging.INFO)
        handler.setFormatter(cls.get_fmt())
        return handler

    @classmethod
    def get_error_handler(cls, log_name):
        handler = cls._get_handler(log_name, level='ERROR')
        handler.setLevel(logging.ERROR)
        handler.setFormatter(cls.get_fmt())
        return handler

    @classmethod
    def get_logger(cls, log_name):
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.INFO)
        logger.addHandler(cls.get_handler(log_name))
        logger.addHandler(cls.get_error_handler(log_name))
        return logger


logger = LogHandler.get_logger('Administration')
