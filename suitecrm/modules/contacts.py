from ..base import SuiteCRMAPI
from typing import Dict, List, Optional, Union
import json
import os
from ..logging_config import setup_logging, log_api_call
import logging

# Debug print for logging setup
print(f"Setting up logging for contacts module. Current directory: {os.getcwd()}")
print(f"Logs directory should be at: {os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')}")

# Set up logger for this module
logger = setup_logging('suitecrm.contacts')

# Debug print for logger setup verification
print(f"Logger handlers: {[type(h).__name__ for h in logger.handlers]}")
print(f"Logger level: {logging.getLevelName(logger.level)}")

class ContactsAPI:
    """API class for handling Contact-related operations in SuiteCRM."""
    
    def __init__(self):
        print("ContactsAPI.__init__ called")  # Debug print
        logger.info("Initializing ContactsAPI")
        self.api = SuiteCRMAPI()
        logger.debug(f"Created SuiteCRMAPI instance, initial session_id: {self.api.session_id}")

    def search_contacts(self, query: str, field: str = "phone_mobile") -> Union[List[Dict], Dict]:
        """
        Search for contacts in SuiteCRM based on a query string and specified field.

        Args:
            query (str): The search query to match against contact records
            field (str): The contact field to search against. Defaults to "phone_mobile"

        Returns:
            Union[List[Dict], Dict]: A list of contact records matching the search criteria,
                                   or error dictionary if the operation fails
        """
        try:
            operation = f"Search contacts by {field}"
            logger.info(f"{operation} started with query: {query}")
            
            # Ensure we have a session ID
            self.api.ensure_logged_in()
            logger.debug(f"Current session_id before search: {self.api.session_id}")
            
            search_params = {
                "session": self.api.session_id,
                "module_name": "Contacts",
                "query": f"contacts.{field} LIKE '%{query}%'",
                "order_by": "",
                "offset": 0,
                "select_fields": [
                    "id",
                    "first_name",
                    "last_name",
                    "email1",
                    "phone_mobile",
                    "phone_work",
                    "phone_home"
                ],
                "max_results": 10,
                "deleted": 0
            }
            
            # Log the operation details
            log_api_call(
                logger,
                "SEARCH",
                operation,
                request_data=search_params
            )
            
            result = self.api.call("get_entry_list", search_params)
            
            if not result:
                error_msg = "Search contacts API call returned None"
                logger.error(error_msg)
                log_api_call(logger, "SEARCH", operation, error=error_msg)
                return {"error": "API call failed", "details": "No response from server"}
            
            # Log successful result
            log_api_call(
                logger,
                "SEARCH",
                operation,
                response_data={
                    "result_count": result.get("result_count", 0),
                    "total_count": result.get("total_count", 0)
                }
            )
            
            return result

        except Exception as e:
            error_msg = f"Failed to search contacts: {str(e)}"
            logger.error(error_msg)
            log_api_call(logger, "SEARCH", operation, error=error_msg)
            return {
                "error": "Search operation failed",
                "details": str(e)
            }

    def create_contact(self, contact_data: dict) -> Union[Dict, Dict]:
        """
        Create a new contact record in SuiteCRM with the provided contact information.

        Args:
            contact_data (dict): A dictionary containing contact information with fields like:
                - first_name: Contact's first name
                - last_name: Contact's last name (required)
                - email: Contact's email address
                - phone_mobile: Contact's mobile number
                - phone_work: Contact's work phone
                - phone_home: Contact's home phone
                - description: Additional notes
                - title: Job title
                - department: Department
                - address_street: Street address
                - address_city: City
                - address_state: State/Province
                - address_postalcode: Postal code
                - address_country: Country

        Returns:
            Union[Dict, Dict]: The newly created contact record including the generated ID,
                             or error dictionary if the operation fails
        """
        try:
            operation = "Create new contact"
            logger.info(f"{operation} started")
            logger.debug(f"Contact data: {json.dumps(contact_data, indent=2)}")


            logger.debug(f"Checking for email fields in contact data: {json.dumps(contact_data, indent=2)}")
            email_value = None
            email_source = None
            if "email" in contact_data and contact_data["email"]:
                email_value = contact_data["email"]
                email_source = "email"
                logger.debug(f"Found email in 'email' field: {email_value}")
            elif "email1" in contact_data and contact_data["email1"]:
                email_value = contact_data["email1"]
                email_source = "email1"
                logger.debug(f"Found email in 'email1' field: {email_value}")
            else:
                logger.debug("No email field found in contact data")

            # Log email validation details
            if email_source:
                logger.info(f"Email validation passed: Using {email_source} field")
                logger.debug(f"Email validation details - Field: {email_source}, Value: {email_value}")
                log_api_call(
                    logger,
                    "EMAIL_VALIDATION",
                    operation,
                    request_data={
                        "status": "success",
                        "used_field": email_source,
                        "value": email_value
                    }
                )
            else:
                logger.info("Email validation skipped: No email provided")
                log_api_call(
                    logger, 
                    "EMAIL_VALIDATION",
                    operation,
                    request_data={
                        "status": "skipped",
                        "reason": "no_email_provided"
                    }
                )
            
            # Ensure we have a session ID
            self.api.ensure_logged_in()
            logger.debug(f"Current session_id before validation: {self.api.session_id}")
            
            # Validate required fields
            # if not contact_data.get("last_name"):
            #     error_msg = "Contact creation failed: last_name is required"
            #     logger.error(error_msg)
            #     log_api_call(logger, "CREATE", operation, error=error_msg)
            #     return {"error": "Validation failed", "details": "last_name is required"}

            # Determine which email field is present
            # Check for email fields
            

            # Convert the input dictionary to SuiteCRM expected format
            field_mapping = {
                "first_name": "first_name",
                "last_name": "last_name",
                "phone_mobile": "phone_mobile",
                "phone_work": "phone_work",
                "phone_home": "phone_home",
                "description": "description",
                "title": "title",
                "department": "department",
                "address_street": "primary_address_street",
                "address_city": "primary_address_city",
                "address_state": "primary_address_state",
                "address_postalcode": "primary_address_postalcode",
                "address_country": "primary_address_country"
            }

            # Create name-value list in SuiteCRM format
            name_value_list = {}
            for input_key, crm_field in field_mapping.items():
                if input_key in contact_data:
                    name_value_list[crm_field] = {
                        "name": crm_field,
                        "value": contact_data[input_key]
                    }
            # Always set email1 if we found an email
            if email_value:
                name_value_list["email1"] = {
                    "name": "email1",
                    "value": email_value
                }
            
            create_params = {
                "session": self.api.session_id,
                "module_name": "Contacts",
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
                error_msg = "Create contact API call returned None"
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
            error_msg = f"Failed to create contact: {str(e)}"
            logger.error(error_msg)
            log_api_call(logger, "CREATE", operation, error=error_msg)
            return {
                "error": "Create operation failed",
                "details": str(e)
            }