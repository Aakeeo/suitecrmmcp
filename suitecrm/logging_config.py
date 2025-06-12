import os
import logging
import logging.handlers
from datetime import datetime

# Create logs directory if it doesn't exist
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

# Generate log filename with timestamp
LOG_FILENAME = os.path.join(LOGS_DIR, f'suitecrm_{datetime.now().strftime("%Y%m%d")}.log')

def setup_logging(name='suitecrm'):
    """
    Set up logging configuration for the application.
    Creates both file and console handlers with different formats.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Prevent logging from propagating to the root logger
    logger.propagate = False

    # Clear any existing handlers
    if logger.handlers:
        logger.handlers.clear()

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%H:%M:%S'
    )

    # File handler - Rotating file handler to manage log file size
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger

# Create a function to log request/response details
def log_api_call(logger, method, endpoint, request_data=None, response_data=None, error=None):
    """
    Log API call details including request and response data.
    
    Args:
        logger: Logger instance
        method: HTTP method or API method name
        endpoint: API endpoint or operation
        request_data: Request payload data
        response_data: Response data
        error: Error details if any
    """
    logger.info(f"API Call Started: {method} {endpoint}")
    
    if request_data:
        logger.debug(f"Request Data: {request_data}")
    
    if response_data:
        logger.debug(f"Response Data: {response_data}")
    
    if error:
        logger.error(f"API Call Error: {error}")
    else:
        logger.info(f"API Call Completed: {method} {endpoint}") 