# -*- coding: UTF-8 -*-

import logging
import os


class MyLog(object):

    """
    default setting
    """

    log_file_base_path = './'
    maxBytes = '1024000'
    backupCount = 10
    outputConsole = 1
    outputFile = 1
    outputConsoleLevel = 10
    outputFileLevel = 30
    formatter = "%(asctime)s - %(name)s - %(levelname)s: %(message)s"

    def __init__(self, name='default', **kwargs):

        """
        init config and get value
        """

        self.logger = logging.getLogger(name)

        if 'logFilePath' in kwargs.keys():
            self.log_file_path = kwargs['logFilePath']

        if 'maxBytes' in kwargs.keys():
            self.maxBytes = kwargs['maxBytes']

        if 'backupCount' in kwargs.keys():
            self.backupCount = kwargs['backupCount']

        if 'outputConsoleLevel' in kwargs.keys():
            self.outputConsoleLevel = kwargs['outputConsoleLevel']

        if 'outputFileLevel' in kwargs.keys():
            self.outputFileLevel = kwargs['outputFileLevel']

        if 'outputConsole' in kwargs.keys():
            self.outputConsole = kwargs['outputConsole']

        if 'outputFile' in kwargs.keys():
            self.outputFile = kwargs['outputFile']

        if 'formatter' in kwargs.keys():
            self.formatter = kwargs['formatter']

        if 'logFileBasePath' in kwargs.keys():
            self.log_file_base_path = kwargs['logFileBasePath']

        if 'logFilePathName' in kwargs.keys():
            self.log_file_path = os.path.join(self.log_file_base_path, kwargs['logFilePathName'])
        else:
            self.log_file_path = os.path.join(self.log_file_base_path, name + '.log')

        self.formatter = logging.Formatter(self.formatter)

        # 需要设置默认的级别, 否则会按照 warning 级别
        self.logger.setLevel(logging.DEBUG)

    def getLogger(self):
        """
        output log to console and file
        :return:
        """

        if self.outputConsole == 1:
            # if true, it should output log in console
            ch = logging.StreamHandler()
            ch.setFormatter(self.formatter)
            ch.setLevel(self.outputConsoleLevel)
            self.logger.addHandler(ch)
        else:
            pass

        if self.outputFile == 1:
            fh = logging.FileHandler(self.log_file_path)
            fh.setFormatter(self.formatter)
            fh.setLevel(self.outputFileLevel)
            self.logger.addHandler(fh)
        else:
            pass

        return self.logger

if __name__ == "__main__":

    my_log = MyLog('test9', outputFileLevel=logging.ERROR)
    logger = my_log.getLogger()
    logger.debug('hello')
    logger.info('hello')
    logger.warn('hello')
    logger.error('hello')
    logger.critical('hello')


