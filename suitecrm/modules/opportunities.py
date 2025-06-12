from ..base import SuiteCRMAPI
from typing import Dict, List, Optional, Union
import json
from datetime import datetime
from ..logging_config import setup_logging, log_api_call

# Set up logger for this module
logger = setup_logging('suitecrm.opportunities')

class OpportunitiesAPI:
    """API class for handling Opportunity-related operations in SuiteCRM."""
    
    SALES_STAGES = [
        "Prospecting",
        "Qualification",
        "Needs Analysis",
        "Value Proposition",
        "Identifying Decision Makers",
        "Perception Analysis",
        "Proposal/Price Quote",
        "Negotiation/Review",
        "Closed Won",
        "Closed Lost"
    ]
    
    def __init__(self):
        logger.info("Initializing OpportunitiesAPI")
        self.api = SuiteCRMAPI()
        logger.debug(f"Created SuiteCRMAPI instance, initial session_id: {self.api.session_id}")

    def create_opportunity(self, opportunity_data: dict) -> Union[Dict, Dict]:
        """
        Create a new opportunity record in SuiteCRM.

        Args:
            opportunity_data (dict): A dictionary containing opportunity information with fields:
                - name: Opportunity name (required)
                - account_id: Related account ID (required)
                - sales_stage: Sales stage (required, must be one of SALES_STAGES)
                - amount: Opportunity amount (required)
                - date_closed: Expected close date (required, format: YYYY-MM-DD)
                - lead_id: Related lead ID (optional)
                - description: Additional notes (optional)
                - probability: Success probability (optional)

        Returns:
            Union[Dict, Dict]: The newly created opportunity record including the generated ID,
                             or error dictionary if the operation fails
        """
        try:
            operation = "Create new opportunity"
            logger.info(f"{operation} started")
            logger.debug(f"Opportunity data: {json.dumps(opportunity_data, indent=2)}")
            
            # Validate required fields
            required_fields = ['name', 'account_id', 'sales_stage', 'amount', 'date_closed']
            for field in required_fields:
                if field not in opportunity_data:
                    error_msg = f"Missing required field: {field}"
                    logger.error(error_msg)
                    return {"error": "Validation failed", "details": error_msg}

            # Validate sales stage
            if opportunity_data['sales_stage'] not in self.SALES_STAGES:
                error_msg = f"Invalid sales stage. Must be one of: {', '.join(self.SALES_STAGES)}"
                logger.error(error_msg)
                return {"error": "Validation failed", "details": error_msg}

            # Validate date format
            try:
                datetime.strptime(opportunity_data['date_closed'], '%Y-%m-%d')
            except ValueError:
                error_msg = "Invalid date format. Use YYYY-MM-DD"
                logger.error(error_msg)
                return {"error": "Validation failed", "details": error_msg}

            # Ensure we have a session ID
            self.api.ensure_logged_in()
            
            # Convert the input dictionary to SuiteCRM expected format
            name_value_list = {}
            for key, value in opportunity_data.items():
                name_value_list[key] = {
                    "name": key,
                    "value": value
                }
            
            create_params = {
                "session": self.api.session_id,
                "module_name": "Opportunities",
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
                error_msg = "Create opportunity API call returned None"
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
            error_msg = f"Failed to create opportunity: {str(e)}"
            logger.error(error_msg)
            log_api_call(logger, "CREATE", operation, error=error_msg)
            return {
                "error": "Create operation failed",
                "details": str(e)
            }

    def convert_lead_to_opportunity(self, lead_id: str, opportunity_data: dict) -> Union[Dict, Dict]:
        """
        Convert a lead to an opportunity in SuiteCRM.

        Args:
            lead_id (str): The ID of the lead to convert
            opportunity_data (dict): A dictionary containing opportunity information with fields:
                - name: Opportunity name (required)
                - account_id: Related account ID (required)
                - sales_stage: Sales stage (required)
                - amount: Opportunity amount (required)
                - date_closed: Expected close date (required, format: YYYY-MM-DD)
                - description: Additional notes (optional)
                - probability: Success probability (optional)

        Returns:
            Union[Dict, Dict]: The newly created opportunity record,
                             or error dictionary if the operation fails
        """
        try:
            operation = f"Convert lead {lead_id} to opportunity"
            logger.info(f"{operation} started")
            
            # Create the opportunity
            opportunity_data['lead_id'] = lead_id
            result = self.create_opportunity(opportunity_data)
            
            if 'error' in result:
                return result
            
            # Update lead status to converted
            self.api.ensure_logged_in()
            update_lead_params = {
                "session": self.api.session_id,
                "module_name": "Leads",
                "name_value_list": {
                    "id": {"name": "id", "value": lead_id},
                    "status": {"name": "status", "value": "Converted"}
                }
            }
            
            self.api.call("set_entry", update_lead_params)
            
            return result

        except Exception as e:
            error_msg = f"Failed to convert lead to opportunity: {str(e)}"
            logger.error(error_msg)
            return {
                "error": "Conversion failed",
                "details": str(e)
            }

    def list_opportunities(self) -> Union[Dict, Dict]:
        """
        Get a list of all opportunities with essential details only.

        Returns:
            Union[Dict, Dict]: List of opportunities with basic details or error dictionary
        """
        try:
            operation = "List opportunities"
            logger.info(f"{operation} started")
            
            # Ensure we have a session ID
            self.api.ensure_logged_in()

            # Only fetch essential fields
            select_fields = [
                'name',
                'amount',
                'date_closed',
                'sales_stage'
            ]

            get_params = {
                'session': self.api.session_id,
                'module_name': 'Opportunities',
                'query': '',
                'order_by': 'date_closed ASC',  # Sort by close date
                'offset': 0,
                'select_fields': select_fields,
                'max_results': 100,
                'deleted': 0
            }

            result = self.api.call('get_entry_list', get_params)

            if not result:
                return {
                    "status": "error",
                    "message": "No response from API",
                    "details": "API call returned None"
                }

            # Format the response with essential details
            opportunities = []
            for entry in result.get('entry_list', []):
                name_value_list = entry.get('name_value_list', {})
                opp = {
                    "name": name_value_list.get('name', {}).get('value', 'N/A'),
                    "amount": name_value_list.get('amount', {}).get('value', '0'),
                    "date_closed": name_value_list.get('date_closed', {}).get('value', 'N/A'),
                    "sales_stage": name_value_list.get('sales_stage', {}).get('value', 'N/A')
                }
                opportunities.append(opp)

            return {
                "status": "success",
                "message": f"Found {len(opportunities)} opportunities",
                "opportunities": opportunities,
                "total_count": len(opportunities)
            }

        except Exception as e:
            error_msg = f"Failed to list opportunities: {str(e)}"
            logger.error(error_msg)
            return {
                "status": "error",
                "message": error_msg,
                "details": traceback.format_exc()
            }

    def search_opportunities(self, query: str) -> Union[Dict, Dict]:
        """
        Search through the list of opportunities by name.

        Args:
            query (str): Search query string to match against opportunity names

        Returns:
            Union[Dict, Dict]: List of matching opportunities or error dictionary
        """
        try:
            # First get all opportunities
            result = self.list_opportunities()
            
            if 'error' in result:
                return result
                
            # Filter opportunities based on the query
            opportunities = result['opportunities']
            filtered_opps = [
                opp for opp in opportunities 
                if query.lower() in opp.get('name', '').lower()
            ]

            return {
                'status': 'success',
                'total_count': len(filtered_opps),
                'opportunities': filtered_opps
            }

        except Exception as e:
            error_msg = f"Failed to search opportunities: {str(e)}"
            logger.error(error_msg)
            return {
                "error": "Search operation failed",
                "details": str(e)
            }