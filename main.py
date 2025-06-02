from mcp.server.fastmcp import FastMCP
from suitecrm import ContactsAPI, AccountsAPI
import traceback

mcp = FastMCP("suitecrm")

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
            - last_name: Contact's last name
            - email: Contact's email address
            - phone_mobile: Contact's mobile number
            - etc.

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
        list: A list of account records matching the search criteria with fields:
            - id: Account ID
            - name: Account name
            - phone_office: Office phone number
            - website: Account website
            - billing_address_city: City from billing address
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
        account_data (dict): A dictionary containing account information with fields like:
            - name: Account name
            - phone_office: Office phone number
            - website: Account website
            - billing_address_city: City
            - etc.

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

async def test_create_contact():
    """
    Test function to create a new contact with sample data
    """
    sample_contact = {
        "email": "something@gmail.com",
        "last_name": "Chauhan", 
        "first_name": "Shivam",
        "phone_mobile": "7009808"
    }
    
    try:
        result = await create_new_contact(sample_contact)
        if "error" in result:
            print("Error creating contact:", result["error"])
            print("Traceback:", result["traceback"])
        else:
            print("Successfully created contact:", result)
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        print(traceback.format_exc())

def test_create_contact_sync():
    """
    Synchronous test function to create a new contact with sample data
    """
    sample_contact = {
        "email": "something@gmail.com",
        "last_name": "Chauhan", 
        "first_name": "Shivam",
        "phone_mobile": "7009808"
    }
    
    try:
        contacts_api = ContactsAPI()
        result = contacts_api.create_contact(sample_contact)
        if result is None:
            print("Error: API call returned None")
            return
        
        if "error" in result:
            print("Error creating contact:", result["error"])
            print("Traceback:", result["traceback"])
        else:
            print("Successfully created contact:", result)
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        print(traceback.format_exc())

if __name__ == "__main__":
   # Test the contact creation
    test_create_contact_sync()  # Run the synchronous test
    # mcp.run(transport="stdio")  # Continue with normal MCP operation