import os
import logging
from logging.handlers import TimedRotatingFileHandler

class Logger:

    def __init__(self, logger_name, streaming_log_level="DEBUG") -> None:

        # set params
        self._logger_name = logger_name
        self._streaming_log_level = streaming_log_level

        # enable physical logging
        self._physival_logging_level = None
        self._log_folder_path = None
        self._rotate_days = 30

        # set logger
        self._logger = self.init_logger()

    def init_logger(self):

        # get logger
        try:
            logger=logging.getLogger(self._logger_name)
        except Exception as e:
            raise Exception(f"get logger failed: {str(e)}")

        # set logging level
        logging_level_value = None
        try:
            if self._streaming_log_level.lower() == "debug":
                logging_level_value = logging.DEBUG
            elif self._streaming_log_level.lower() == "info":
                logging_level_value = logging.INFO
            elif self._streaming_log_level.lower() == "warning":
                logging_level_value = logging.WARNING
            elif self._streaming_log_level.lower() == "critical":
                logging_level_value = logging.CRITICAL
            else:
                raise ValueError(f"streaming logging level {self._streaming_log_level} is not supported")
        except Exception as e:
            raise Exception(f"set streaming logging level failed: {str(e)}")

        try:
            # set formatters of log
            formatter = logging.Formatter('[%(asctime)s.%(msecs)03d][%(levelname)s][%(name)s] %(message)s', datefmt='%Y-%m-%d,%H:%M:%S')
        except Exception as e:
            raise Exception(f"set streaming logging formatter failed: {str(e)}")

        # set handlers
        try:           
            # log stream handler & set formatter and level to store
            stream_handler = logging.StreamHandler() # printing to cmd
            stream_handler.setFormatter(formatter)
            stream_handler.setLevel(logging_level_value) # It means DEBUG, INFO, WARNING, CRITICAL will be print
        except Exception as e:
            raise Exception(f"set streaming logging handler failed: {str(e)}")
        
        try:
            # set logger level to memo logs
            logger.setLevel(logging_level_value)

            # add handler
            logger.addHandler(stream_handler)
        except Exception as e:
            raise Exception(f"init logger failed: {str(e)}")

        return logger
    
    def enable_physical_logging(self, log_folder_path, log_level, rotate_days):

        # set params
        self._physival_logging_level = log_level
        self._log_folder_path = log_folder_path
        self._rotate_days = rotate_days

        # check/create log folder
        try:
            if not os.path.exists(self._log_folder_path):
                os.makedirs(self._log_folder_path)
        except Exception as e:
            raise Exception(f"create phtsical log folder failed: {str(e)}")
        
        # set log path
        log_path = os.path.join(self._log_folder_path, f"{self._logger_name}.log")

        # set logging level
        logging_level_value = None
        try:
            if self._physival_logging_level.lower() == "debug":
                logging_level_value = logging.DEBUG
            elif self._physival_logging_level.lower() == "info":
                logging_level_value = logging.INFO
            elif self._physival_logging_level.lower() == "warning":
                logging_level_value = logging.WARNING
            elif self._physival_logging_level.lower() == "critical":
                logging_level_value = logging.CRITICAL
            else:
                raise ValueError(f"phtsical logging level {self._physival_logging_level} is not supported")
        except Exception as e:
            raise Exception(f"set phtsical logging level failed: {str(e)}")

        try:
            # set formatters of log
            formatter = logging.Formatter('[%(asctime)s.%(msecs)03d][%(levelname)s][%(name)s] %(message)s', datefmt='%Y-%m-%d,%H:%M:%S')
        except Exception as e:
            raise Exception(f"set phtsical logging formatter failed: {str(e)}")

        # set handlers
        try:
            # set rotating file handler
            # store filename, when='D', interval=1, backupCount=30 means 1 day 1 file & reserve at most 30 files
            file_handler = TimedRotatingFileHandler(filename=log_path, when='D', interval=1, backupCount=self._rotate_days) 
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging_level_value) # It means DEBUG, INFO, WARNING, CRITICAL will be stored

        except Exception as e:
            raise Exception(f"set phtsical logging handler failed: {str(e)}")
        
        try:
            # set logger level to memo logs
            self._logger.setLevel(logging_level_value)

            # add handler
            self._logger.addHandler(file_handler) 
        except Exception as e:
            raise Exception(f"enable phtsical logger failed: {str(e)}")
        
    
    def info(self, message):
        try:
            self._logger.info(self._postprocess(message))
        except Exception as msg:
            raise Exception(f"store info log failed: {str(msg)}")
        
    def debug(self, message):
        try:
            self._logger.debug(self._postprocess(message))
        except Exception as msg:
            raise Exception(f"store debug log failed: {str(msg)}")
        
    def warning(self, message):
        try:
            self._logger.warning(self._postprocess(message))
        except Exception as msg:
            raise Exception(f"store warning log failed: {str(msg)}")
        
    def critical(self, message):
        try:
            self._logger.critical(self._postprocess(message))
        except Exception as msg:
            raise Exception(f"store critical log failed: {str(msg)}")
        
    def _postprocess(self, message):
        return str(message).replace("\n", ";").replace("\r", " ").replace("\t", " ")
