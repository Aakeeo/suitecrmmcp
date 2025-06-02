from mcp.server.fastmcp import FastMCP
import argparse
import traceback
import json
import logging
from suitecrm import ContactsAPI, AccountsAPI

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

def main():
    parser = argparse.ArgumentParser(description='SuiteCRM API Testing Tool')
    parser.add_argument('action', choices=['search_contacts', 'create_contact', 
                                         'search_accounts', 'create_account'],
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

if __name__ == "__main__":
    # If no arguments provided, run as MCP server
    import sys
    if len(sys.argv) == 1:
        print("No arguments provided. Running as MCP server...")
        mcp.run(transport="stdio")
    else:
        main() 