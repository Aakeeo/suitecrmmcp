from ..base import SuiteCRMAPI
from typing import Dict, List, Optional, Union
import json
from ..logging_config import setup_logging, log_api_call

# Set up logger for this module
logger = setup_logging('suitecrm.accounts')

class AccountsAPI:
    """API class for handling Account-related operations in SuiteCRM."""
    
    def __init__(self):
        logger.info("Initializing AccountsAPI")
        self.api = SuiteCRMAPI()
        logger.debug(f"Created SuiteCRMAPI instance, initial session_id: {self.api.session_id}")

    def search_accounts(self, query: str, field: str = "name") -> Union[List[Dict], Dict]:
        """
        Search for accounts in SuiteCRM based on a query string and specified field.

        Args:
            query (str): The search query to match against account records
            field (str): The account field to search against. Defaults to "name"

        Returns:
            Union[List[Dict], Dict]: A list of account records matching the search criteria,
                                   or error dictionary if the operation fails
        """
        try:
            operation = f"Search accounts by {field}"
            logger.info(f"{operation} started with query: {query}")
            
            # Ensure we have a session ID before creating search params
            self.api.ensure_logged_in()
            logger.debug(f"Current session_id before search: {self.api.session_id}")
            
            search_params = {
                "session": self.api.session_id,
                "module_name": "Accounts",
                "query": f"accounts.{field} LIKE '%{query}%'",
                "order_by": "",
                "offset": 0,
                "select_fields": [
                    "id",
                    "name",
                    "phone_office",
                    "website",
                    "billing_address_city"
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
                error_msg = "Search accounts API call returned None"
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
            error_msg = f"Failed to search accounts: {str(e)}"
            logger.error(error_msg)
            log_api_call(logger, "SEARCH", operation, error=error_msg)
            return {
                "error": "Search operation failed",
                "details": str(e)
            }

    def create_account(self, account_data: dict) -> Union[Dict, Dict]:
        """
        Create a new account record in SuiteCRM.

        Args:
            account_data (dict): A dictionary containing account information with fields like:
                - name: Account name (required)
                - phone_office: Office phone number
                - website: Account website
                - billing_address_street: Street address
                - billing_address_city: City
                - billing_address_state: State/Province
                - billing_address_postalcode: Postal code
                - billing_address_country: Country
                - description: Additional notes

        Returns:
            Union[Dict, Dict]: The newly created account record including the generated ID,
                             or error dictionary if the operation fails
        """
        try:
            operation = "Create new account"
            logger.info(f"{operation} started")
            logger.debug(f"Account data: {json.dumps(account_data, indent=2)}")
            
            # Ensure we have a session ID
            self.api.ensure_logged_in()
            logger.debug(f"Current session_id before validation: {self.api.session_id}")
            
            # Validate required fields
            if not account_data.get("name"):
                error_msg = "Account creation failed: name is required"
                logger.error(error_msg)
                log_api_call(logger, "CREATE", operation, error=error_msg)
                return {"error": "Validation failed", "details": "name is required"}

            # Convert the input dictionary to SuiteCRM expected format
            name_value_list = {}
            for key, value in account_data.items():
                name_value_list[key] = {
                    "name": key,
                    "value": value
                }
            
            create_params = {
                "session": self.api.session_id,
                "module_name": "Accounts",
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
                error_msg = "Create account API call returned None"
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
            error_msg = f"Failed to create account: {str(e)}"
            logger.error(error_msg)
            log_api_call(logger, "CREATE", operation, error=error_msg)
            return {
                "error": "Create operation failed",
                "details": str(e)
            }