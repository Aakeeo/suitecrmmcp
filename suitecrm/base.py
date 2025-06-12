import hashlib
import json
import requests
from .config import SUITECRM_URL, USERNAME, PASSWORD
from .exceptions import SuiteCRMAuthenticationError, SuiteCRMAPIError
from .logging_config import setup_logging, log_api_call

# Set up logger for this module
logger = setup_logging('suitecrm.base')

class SuiteCRMAPI:
    def __init__(self):
        self.session_id = None
        self.base_url = SUITECRM_URL
        logger.info(f"Initialized SuiteCRMAPI with base URL: {self.base_url}")
        logger.debug("Initial session_id is None")

    def _call(self, method, parameters):
        """Helper function to call SuiteCRM API"""
        logger.debug(f"_call method invoked with session_id: {self.session_id}")
        
        post_data = {
            "method": method,
            "input_type": "JSON",
            "response_type": "JSON",
            "rest_data": json.dumps(parameters)
        }

        try:
            # Log the API call start
            log_api_call(
                logger,
                method,
                self.base_url,
                request_data={
                    "method": method,
                    "parameters": parameters,
                    "post_data": post_data
                }
            )
            
            logger.debug(f"Making API call to {self.base_url}")
            response = requests.post(self.base_url, data=post_data)
            
            logger.debug(f"Response status code: {response.status_code}")
            logger.debug(f"Response headers: {dict(response.headers)}")
            
            if response.status_code != 200:
                error_msg = f"API call failed with status code {response.status_code}"
                logger.error(error_msg)
                logger.error(f"Response content: {response.text}")
                log_api_call(logger, method, self.base_url, error=error_msg)
                raise SuiteCRMAPIError(error_msg)
            
            try:
                result = response.json()
                # Log successful API call completion
                log_api_call(
                    logger,
                    method,
                    self.base_url,
                    response_data=result
                )
                return result
            except json.JSONDecodeError as e:
                error_msg = f"Invalid JSON response: {str(e)}"
                logger.error(error_msg)
                logger.error(f"Raw response: {response.text}")
                log_api_call(logger, method, self.base_url, error=error_msg)
                raise SuiteCRMAPIError(error_msg)
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {str(e)}"
            logger.error(error_msg)
            log_api_call(logger, method, self.base_url, error=error_msg)
            raise SuiteCRMAPIError(f"API call failed: {str(e)}")

    def login(self):
        """Function to login and get session ID"""
        logger.info("Attempting to login to SuiteCRM")
        logger.debug(f"Current session_id before login: {self.session_id}")
        
        login_parameters = {
            "user_auth": {
                "user_name": USERNAME,
                "password": hashlib.md5(PASSWORD.encode()).hexdigest(),
                "version": "1"
            },
            "application_name": "RestTest",
            "name_value_list": []
        }
        
        try:
            login_result = self._call("login", login_parameters)
            
            if "error" in login_result:
                error_msg = f"Login failed: {login_result.get('message', 'Unknown error')}"
                logger.error(error_msg)
                raise SuiteCRMAuthenticationError(error_msg)
            
            self.session_id = login_result.get('id')
            if self.session_id:
                logger.info("Successfully logged in to SuiteCRM")
                logger.debug(f"New session ID obtained: {self.session_id}")
            else:
                error_msg = "Login succeeded but no session ID in response"
                logger.error(error_msg)
                logger.debug(f"Full login response: {json.dumps(login_result, indent=2)}")
                raise SuiteCRMAuthenticationError(error_msg)
                
            return self.session_id
            
        except Exception as e:
            error_msg = f"Login failed with exception: {str(e)}"
            logger.error(error_msg)
            raise SuiteCRMAuthenticationError(error_msg)

    def ensure_logged_in(self):
        """Ensure we have a valid session ID"""
        logger.debug(f"ensure_logged_in called, current session_id: {self.session_id}")
        if not self.session_id:
            logger.debug("No session ID found, attempting to login")
            self.login()
        else:
            logger.debug("Using existing session ID")
            
    def call(self, method, parameters):
        """Public method to make API calls with automatic login handling"""
        logger.debug(f"call method invoked for {method}, current session_id: {self.session_id}")
        self.ensure_logged_in()
        logger.debug(f"After ensure_logged_in, session_id is: {self.session_id}")
        return self._call(method, parameters)