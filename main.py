from mcp.server.fastmcp import FastMCP
from typing import Optional
from suitecrm import ContactsAPI, AccountsAPI, LeadsAPI, OpportunitiesAPI
from suitecrm.services.contact_manager import ContactManager
from suitecrm.modules.opportunities import OpportunitiesAPI
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
async def process_contact(data: dict):
    """
    Process contact information to either create a contact under an existing account
    or create a new account and lead.

    Args:
        data (dict): Dictionary containing contact information including:
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

@mcp.tool()
async def create_new_lead(lead_data: dict):
    """
    Create a new lead record in SuiteCRM.

    Args:
        lead_data (dict): A dictionary containing lead information with fields like:
            - first_name: Lead's first name
            - last_name: Lead's last name
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
        
        if not result:
            return {
                "status": "error",
                "message": "No response received",
                "details": "API call returned None"
            }
            
        return result

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to list opportunities: {str(e)}",
            "details": traceback.format_exc()
        }

@mcp.tool()
async def search_opportunities(query: str):
    """
    Search for opportunities by name.

    Args:
        query (str): Search query string to match against opportunity names

    Returns:
        dict: List of matching opportunities with complete details
    """
    try:
        # First get all opportunities
        result = await list_opportunities()
        
        if result.get("status") == "error":
            return result
            
        opportunities = result.get("opportunities", [])
        
        # Filter opportunities by name
        filtered_opps = [
            opp for opp in opportunities
            if query.lower() in str(opp.get("name", "")).lower()
        ]
        
        return {
            "status": "success",
            "message": f"Found {len(filtered_opps)} matching opportunities",
            "opportunities": filtered_opps,
            "total_count": len(filtered_opps)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to search opportunities: {str(e)}",
            "details": traceback.format_exc()
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