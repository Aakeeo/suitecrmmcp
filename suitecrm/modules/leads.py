from ..base import SuiteCRMAPI
from typing import Dict, List, Optional, Union
import json
from ..logging_config import setup_logging, log_api_call

# Set up logger for this module
logger = setup_logging('suitecrm.leads')

class LeadsAPI:
    """API class for handling Lead-related operations in SuiteCRM."""
    
    def __init__(self):
        logger.info("Initializing LeadsAPI")
        self.api = SuiteCRMAPI()
        logger.debug(f"Created SuiteCRMAPI instance, initial session_id: {self.api.session_id}")

    def create_lead(self, lead_data: dict) -> Union[Dict, Dict]:
        """
        Create a new lead record in SuiteCRM.

        Args:
            lead_data (dict): A dictionary containing lead information with fields like:
                - first_name: Lead's first name
                - last_name: Lead's last name (required)
                - email1: Lead's email address
                - phone_mobile: Lead's mobile number
                - account_name: Associated account name
                - status: Lead status
                - lead_source: Source of the lead

        Returns:
            Union[Dict, Dict]: The newly created lead record including the generated ID,
                             or error dictionary if the operation fails
        """
        try:
            operation = "Create new lead"
            logger.info(f"{operation} started")
            logger.debug(f"Lead data: {json.dumps(lead_data, indent=2)}")
            
            # Ensure we have a session ID
            self.api.ensure_logged_in()
            
            # Convert the input dictionary to SuiteCRM expected format
            name_value_list = {}
            for key, value in lead_data.items():
                name_value_list[key] = {
                    "name": key,
                    "value": value
                }
            
            create_params = {
                "session": self.api.session_id,
                "module_name": "Leads",
                "name_value_list": name_value_list
            }
            
            # Log the operation details
            log_api_call(
                logger,
                "CREATE",
                operation,
                request_data=create_params
            )
            
            result = self.api.call("set_entry", create_params)
            
            if not result:
                error_msg = "Create lead API call returned None"
                logger.error(error_msg)
                log_api_call(logger, "CREATE", operation, error=error_msg)
                return {"error": "API call failed", "details": "No response from server"}
            
            # Log successful result
            log_api_call(
                logger,
                "CREATE",
                operation,
                response_data=result
            )
            
            return result

        except Exception as e:
            error_msg = f"Failed to create lead: {str(e)}"
            logger.error(error_msg)
            log_api_call(logger, "CREATE", operation, error=error_msg)
            return {
                "error": "Create operation failed",
                "details": str(e)
            }