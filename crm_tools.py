from mcp.server.fastmcp import FastMCP
import argparse
from suitecrm import ContactsAPI, AccountsAPI, LeadsAPI, OpportunitiesAPI
import traceback
import logging
import json
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('crm_tools')

mcp = FastMCP("suitecrm")

# Tool Functions
@mcp.tool()
async def search_contacts(query: str, field: str = "phone_mobile"):
    """
    Search for contacts in SuiteCRM based on a query string and specified field.

    Args:
        query (str): The search query to match against contact records
        field (str, optional): The contact field to search against. Defaults to "phone_mobile"

    Returns:
        list: A list of contact records matching the search criteria
        dict: Error message if API call fails
    """
    try:
        contacts_api = ContactsAPI()
        return contacts_api.search_contacts(query, field)
    except Exception as e:
        return {
            "error": f"Failed to search contacts: {str(e)}",
            "traceback": traceback.format_exc()
        }

@mcp.tool()
async def create_new_contact(contact_data: dict):
    """
    Create a new contact record in SuiteCRM with the provided contact information.

    Args:
        contact_data (dict): A dictionary containing contact information with fields like:
            - first_name: Contact's first name
            - last_name: Contact's last name (required)
            - email: Contact's email address and not email1
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
        dict: The newly created contact record including the generated ID
        dict: Error message if API call fails
    """
    try:
        contacts_api = ContactsAPI()
        return contacts_api.create_contact(contact_data)
    except Exception as e:
        return {
            "error": f"Failed to create contact: {str(e)}",
            "traceback": traceback.format_exc()
        }

@mcp.tool()
async def search_accounts(query: str, field: str = "name"):
    """
    Search for accounts in SuiteCRM based on a query string and specified field.

    Args:
        query (str): The search query to match against account records
        field (str, optional): The account field to search against. Defaults to "name"

    Returns:
        list: A list of account records matching the search criteria
        dict: Error message if API call fails
    """
    try:
        accounts_api = AccountsAPI()
        return accounts_api.search_accounts(query, field)
    except Exception as e:
        return {
            "error": f"Failed to search accounts: {str(e)}",
            "traceback": traceback.format_exc()
        }

@mcp.tool()
async def create_new_account(account_data: dict):
    """
    Create a new account record in SuiteCRM.

    Args:
        account_data (dict): A dictionary containing account information

    Returns:
        dict: The newly created account record including the generated ID
        dict: Error message if API call fails
    """
    try:
        accounts_api = AccountsAPI()
        return accounts_api.create_account(account_data)
    except Exception as e:
        return {
            "error": f"Failed to create account: {str(e)}",
            "traceback": traceback.format_exc()
        }

@mcp.tool()
async def create_new_lead(lead_data: dict):
    """
    Create a new lead record in SuiteCRM.

    Args:
        lead_data (dict): A dictionary containing lead information with fields like:
            - first_name: Lead's first name
            - last_name: Lead's last name (required)
            - email1: Lead's email address
            - phone_mobile: Lead's mobile number
            - account_name: Associated account name
            - status: Lead status (defaults to 'New')
            - lead_source: Source of the lead (defaults to 'Web')

    Returns:
        dict: The newly created lead record including the generated ID
        dict: Error message if API call fails
    """
    try:
        leads_api = LeadsAPI()
        return leads_api.create_lead(lead_data)
    except Exception as e:
        return {
            "error": f"Failed to create lead: {str(e)}",
            "traceback": traceback.format_exc()
        }

@mcp.tool()
async def process_contact_and_lead(data: dict):
    """
    Process contact information to either create a contact under an existing account
    or create a new account and lead.

    Args:
        data (dict): Dictionary containing information including:
            - company_name: Name of the company/account
            - first_name: First name of the contact
            - last_name: Last name of the contact
            - email: Email address
            - phone_mobile: Mobile phone number
            - phone_work: Work phone number (optional)
            - website: Company website (optional)

    Returns:
        dict: Result of the operation including created records or error details
    """
    try:
        contact_manager = ContactManager()
        return contact_manager.handle_contact_creation(data)
    except Exception as e:
        return {
            "error": f"Failed to process contact: {str(e)}",
            "traceback": traceback.format_exc()
        }

@mcp.tool()
async def create_opportunity(opportunity_data: dict):
    """
    Create a new opportunity in SuiteCRM.

    Args:
        opportunity_data (dict): Dictionary containing opportunity information:
            - name: Opportunity name (required)
            - account_id: Related account ID (required)
            - sales_stage: Sales stage (required)
            - amount: Opportunity amount (required)
            - date_closed: Expected close date (required, format: YYYY-MM-DD)
            - description: Additional notes (optional)
            - probability: Success probability (optional)

    Returns:
        dict: The newly created opportunity record or error details
    """
    try:
        opportunities_api = OpportunitiesAPI()
        return opportunities_api.create_opportunity(opportunity_data)
    except Exception as e:
        return {
            "error": f"Failed to create opportunity: {str(e)}",
            "traceback": traceback.format_exc()
        }

@mcp.tool()
async def convert_lead_to_opportunity(lead_id: str, opportunity_data: dict):
    """
    Convert a lead to an opportunity in SuiteCRM.

    Args:
        lead_id (str): ID of the lead to convert
        opportunity_data (dict): Dictionary containing opportunity information:
            - name: Opportunity name (required)
            - account_id: Related account ID (required)
            - sales_stage: Sales stage (required)
            - amount: Opportunity amount (required)
            - date_closed: Expected close date (required, format: YYYY-MM-DD)
            - description: Additional notes (optional)
            - probability: Success probability (optional)

    Returns:
        dict: The created opportunity record or error details
    """
    try:
        opportunities_api = OpportunitiesAPI()
        return opportunities_api.convert_lead_to_opportunity(lead_id, opportunity_data)
    except Exception as e:
        return {
            "error": f"Failed to convert lead to opportunity: {str(e)}",
            "traceback": traceback.format_exc()
        }

@mcp.tool()
async def list_opportunities():
    """
    Get a list of all opportunities in SuiteCRM with essential details only.

    Returns:
        dict: List of all opportunities with basic details:
            - name: Opportunity name
            - amount: Opportunity amount
            - date_closed: Expected close date
            - sales_stage: Current sales stage
    """
    try:
        opportunities_api = OpportunitiesAPI()
        result = opportunities_api.list_opportunities()
        
        # Check if result is None or has error
        if not result or 'error' in result:
            return {
                "status": "error",
                "message": "No opportunities found or error occurred",
                "details": result.get('error', 'Unknown error') if result else 'No response from API'
            }

        # If opportunities list is empty, return empty result
        if not result.get('opportunities', []):
            return {
                "status": "success",
                "message": "No opportunities found",
                "opportunities": []
            }

        # Filter to show only essential details
        simplified_opps = []
        for opp in result.get('opportunities', []):
            simplified_opps.append({
                "name": opp.get('name', 'N/A'),
                "amount": opp.get('amount', '0'),
                "date_closed": opp.get('date_closed', 'N/A'),
                "sales_stage": opp.get('sales_stage', 'N/A')
            })

        # Return successful result with simplified data
        return {
            "status": "success",
            "message": f"Found {len(simplified_opps)} opportunities",
            "opportunities": simplified_opps,
            "total_count": len(simplified_opps)
        }

    except Exception as e:
        logger.error(f"Failed to list opportunities: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            "status": "error",
            "message": "Failed to list opportunities",
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@mcp.tool()
async def search_opportunities(query: str):
    """
    Search for opportunities by name.

    Args:
        query (str): Search query string to match against opportunity names

    Returns:
        dict: List of matching opportunities with basic details:
            - name: Opportunity name
            - amount: Opportunity amount
            - date_closed: Expected close date
            - sales_stage: Current sales stage
    """
    try:
        # First try to get all opportunities
        all_opps = await list_opportunities()
        
        if all_opps.get('status') == 'error':
            return all_opps

        opportunities = all_opps.get('opportunities', [])
        
        # Filter opportunities locally based on query
        filtered_opps = [
            opp for opp in opportunities
            if query.lower() in str(opp.get('name', '')).lower()
        ]

        return {
            "status": "success",
            "message": f"Found {len(filtered_opps)} matching opportunities",
            "opportunities": filtered_opps,
            "total_count": len(filtered_opps)
        }

    except Exception as e:
        logger.error(f"Failed to search opportunities: {str(e)}")
        logger.error(traceback.format_exc())
        return {
            "status": "error",
            "message": "Failed to search opportunities",
            "error": str(e),
            "traceback": traceback.format_exc()
        }

# Test Functions
def test_search_contacts(query: str, field: str = "phone_mobile"):
    """Test function for searching contacts"""
    contacts_api = ContactsAPI()
    try:
        result = contacts_api.search_contacts(query, field)
        print("\nSearch Contacts Result:")
        print(json.dumps(result, indent=2))
        return result
    except Exception as e:
        print(f"\nError searching contacts: {str(e)}")
        print(traceback.format_exc())
        return None

def test_create_contact(contact_data: dict = None):
    """Test function for creating a contact"""
    if contact_data is None:
        contact_data = {
            "email": "test@example.com",
            "last_name": "Test",
            "first_name": "User",
            "phone_mobile": "1234567890"
        }
    
    contacts_api = ContactsAPI()
    try:
        result = contacts_api.create_contact(contact_data)
        print("\nCreate Contact Result:")
        print(json.dumps(result, indent=2))
        return result
    except Exception as e:
        print(f"\nError creating contact: {str(e)}")
        print(traceback.format_exc())
        return None

def test_search_accounts(query: str, field: str = "name"):
    """Test function for searching accounts"""
    accounts_api = AccountsAPI()
    try:
        result = accounts_api.search_accounts(query, field)
        print("\nSearch Accounts Result:")
        print(json.dumps(result, indent=2))
        return result
    except Exception as e:
        print(f"\nError searching accounts: {str(e)}")
        print(traceback.format_exc())
        return None

def test_create_account(account_data: dict = None):
    """Test function for creating an account"""
    if account_data is None:
        account_data = {
            "name": "Test Account",
            "phone_office": "1234567890",
            "website": "www.example.com",
            "description": "Test account created via API"
        }
    
    accounts_api = AccountsAPI()
    try:
        logger.debug(f"Attempting to create account with data: {json.dumps(account_data, indent=2)}")
        
        # Get the API session ID for debugging
        session_id = accounts_api.login() if hasattr(accounts_api, 'login') else None
        if session_id:
            logger.debug(f"Successfully obtained session ID: {session_id}")
        else:
            logger.warning("Could not obtain session ID")
            
        result = accounts_api.create_account(account_data)
        logger.debug(f"Raw API response: {json.dumps(result, indent=2)}")
        
        if result is None:
            logger.error("API returned None response")
        elif isinstance(result, dict) and "error" in result:
            logger.error(f"API returned error: {result['error']}")
        else:
            logger.info("Account creation successful")
            
        print("\nCreate Account Result:")
        print(json.dumps(result, indent=2))
        return result
    except Exception as e:
        logger.error(f"Exception during account creation: {str(e)}")
        logger.error(f"Exception traceback:\n{traceback.format_exc()}")
        print(f"\nError creating account: {str(e)}")
        print(traceback.format_exc())
        return None

def test_create_lead(lead_data: dict = None):
    """Test function for creating a lead"""
    if lead_data is None:
        lead_data = {
            "first_name": "Test",
            "last_name": "Lead",
            "email1": "test.lead@example.com",
            "phone_mobile": "1234567890",
            "account_name": "Test Company",
            "status": "New",
            "lead_source": "Web"
        }
    
    leads_api = LeadsAPI()
    try:
        result = leads_api.create_lead(lead_data)
        print("\nCreate Lead Result:")
        print(json.dumps(result, indent=2))
        return result
    except Exception as e:
        print(f"\nError creating lead: {str(e)}")
        print(traceback.format_exc())
        return None

def test_list_opportunities():
    """Test function for listing opportunities"""
    opportunities_api = OpportunitiesAPI()
    try:
        print("\nAttempting to list opportunities...")
        result = opportunities_api.list_opportunities()
        
        if not result:
            print("No response received from API")
            return None
            
        if 'error' in result:
            print(f"Error: {result['error']}")
            return result
            
        print("\nList Opportunities Result:")
        print(f"Total opportunities found: {result.get('total_count', 0)}")
        print(json.dumps(result.get('opportunities', []), indent=2))
        return result
        
    except Exception as e:
        print(f"\nError listing opportunities: {str(e)}")
        print(traceback.format_exc())
        return None

def main():
    parser = argparse.ArgumentParser(description='SuiteCRM API Testing Tool')
    parser.add_argument('action', choices=['search_contacts', 'create_contact', 
                                         'search_accounts', 'create_account',
                                         'create_lead', 'process_contact_and_lead',
                                         'list_opportunities'],  # Add new choice
                       help='Action to perform')
    parser.add_argument('--query', help='Search query for search operations')
    parser.add_argument('--field', help='Field to search in (default depends on action)')
    parser.add_argument('--data', help='JSON string with data for create operations')
    
    args = parser.parse_args()
    
    if args.action == 'search_contacts':
        if not args.query:
            print("Error: --query is required for search_contacts")
            return
        test_search_contacts(args.query, args.field or "phone_mobile")
    
    elif args.action == 'create_contact':
        contact_data = None
        if args.data:
            try:
                contact_data = json.loads(args.data)
            except json.JSONDecodeError:
                print("Error: Invalid JSON data provided")
                return
        test_create_contact(contact_data)
    
    elif args.action == 'search_accounts':
        if not args.query:
            print("Error: --query is required for search_accounts")
            return
        test_search_accounts(args.query, args.field or "name")
    
    elif args.action == 'create_account':
        account_data = None
        if args.data:
            try:
                account_data = json.loads(args.data)
            except json.JSONDecodeError:
                print("Error: Invalid JSON data provided")
                return
        test_create_account(account_data)

    elif args.action == 'create_lead':
        lead_data = None
        if args.data:
            try:
                lead_data = json.loads(args.data)
            except json.JSONDecodeError:
                print("Error: Invalid JSON data provided")
                return
        test_create_lead(lead_data)
    elif args.action == 'process_contact_and_lead':
        data = None
        if args.data:
            try:
                data = json.loads(args.data)
            except json.JSONDecodeError:
                print("Error: Invalid JSON data provided")
                return
        contact_manager = ContactManager()
        result = contact_manager.handle_contact_creation(data)
        print("\nProcess Result:")
        print(json.dumps(result, indent=2))
    elif args.action == 'list_opportunities':
        test_list_opportunities()

if __name__ == "__main__":
    # If no arguments provided, run as MCP server
    import sys
    if len(sys.argv) == 1:
        print("No arguments provided. Running as MCP server...")
        mcp.run(transport="stdio")
    else:
        main()