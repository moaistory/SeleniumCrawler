import logging
import logging.handlers
import os
import inspect

from . import config

log_dir = os.path.join(os.path.normpath(os.getcwd()), config.LOG_DIR)
log_path = os.path.join(log_dir, config.LOG_FILE_NAME)

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger = logging.getLogger(config.NAME)
logger.setLevel(logging.DEBUG)

#set log file
fileFomatter = logging.Formatter('[%(levelname)s][%(asctime)s]%(message)s')
fileHandler = logging.handlers.TimedRotatingFileHandler(log_path, when='midnight', interval=1, encoding='utf-8', backupCount=config.DF_BACKUP_CNT)
fileHandler.setFormatter(fileFomatter)
fileHandler.setLevel(logging.DEBUG)
logger.addHandler(fileHandler)

#set log stream
streamFomatter = logging.Formatter('[%(levelname)s]%(message)s')
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(streamFomatter)
streamHandler.setLevel(logging.INFO)
logger.addHandler(streamHandler)

logger.findCaller()

def getCallInfo():
	prev_frame = inspect.currentframe().f_back.f_back
	func = prev_frame.f_code
	lineno = prev_frame.f_lineno
	info = '[' + str(func.co_filename) + ':' + str(lineno) + '] ' 
	return info

def info(msg) :  
    callInfo = getCallInfo()
    logger.info(callInfo + str(msg))

def debug(msg) :  
    logger.debug(msg)

def warning(msg) :  
    logger.warning(msg)

def error(msg) :  
    logger.error(msg)

def critical(msg) :  
    logger.critical(msg)