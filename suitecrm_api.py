from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import json
import requests
import hashlib

load_dotenv()

mcp = FastMCP("suitecrm-api")

# SuiteCRM configuration
SUITECRM_URL = os.getenv('SUITECRM_URL', 'http://localhost/SuiteCRM-7.14.6/service/v4_1/rest.php')
USERNAME = os.getenv('SUITECRM_USERNAME', 'admin')
PASSWORD = os.getenv('SUITECRM_PASSWORD', 'Admin@123')

def call(method, parameters, url):
    """Helper function to call SuiteCRM API"""
    post_data = {
        "method": method,
        "input_type": "JSON",
        "response_type": "JSON",
        "rest_data": json.dumps(parameters)
    }

    try:
        response = requests.post(url, data=post_data)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": True, "message": str(e)}

def login():
    """Function to login and get session ID"""
    login_parameters = {
        "user_auth": {
            "user_name": USERNAME,
            "password": hashlib.md5(PASSWORD.encode()).hexdigest(),
            "version": "1"
        },
        "application_name": "RestTest",
        "name_value_list": []
    }
    
    login_result = call("login", login_parameters, SUITECRM_URL)
    
    if "error" in login_result:
        raise Exception(f"Error logging in: {login_result['message']}")
    
    return login_result['id']

@mcp.tool()
async def search_contacts(query: str, field: str = "phone_mobile"):
    """
    Search for contacts in SuiteCRM based on a query and field

    Args:
        query (str): The search term
        field (str): The field to search in (default: phone_mobile)

    Returns:
        dict: Contact information
    """
    try:
        session_id = login()
        
        search_params = {
            "session": session_id,
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
        
        result = call("get_entry_list", search_params, SUITECRM_URL)
        return result
    except Exception as e:
        return {"error": True, "message": str(e)}

@mcp.tool()
async def create_new_contact(contact_data: dict):
    """
    Create a new contact in SuiteCRM

    Args:
        contact_data (dict): Dictionary containing contact information
            (first_name, last_name, email, phone_mobile, description)

    Returns:
        dict: Result of contact creation
    """
    try:
        session_id = login()
        
        create_params = {
            "session": session_id,
            "module_name": "Contacts",
            "name_value_list": {
                "first_name": contact_data.get("first_name", ""),
                "last_name": contact_data.get("last_name", ""),
                "email1": contact_data.get("email", ""),
                "phone_mobile": contact_data.get("phone_mobile", ""),
                "description": contact_data.get("description", "")
            }
        }
        
        result = call("set_entry", create_params, SUITECRM_URL)
        return result
    except Exception as e:
        return {"error": True, "message": str(e)}

@mcp.tool()
async def get_user_roles(user_id: str):
    """
    Get roles for a specific user

    Args:
        user_id (str): The ID of the user

    Returns:
        dict: User roles information
    """
    try:
        session_id = login()
        
        get_relationship_params = {
            "session": session_id,
            "module_name": "Users",
            "module_id": user_id,
            "link_field_name": "aclroles",
            "related_module_query": "",
            "related_fields": [],
            "related_module_link_name_to_fields_array": [],
            "deleted": 0,
            "order_by": ''
        }
        
        result = call("get_relationships", get_relationship_params, SUITECRM_URL)
        return result
    except Exception as e:
        return {"error": True, "message": str(e)}

if __name__ == "__main__":
    mcp.run(transport="stdio")