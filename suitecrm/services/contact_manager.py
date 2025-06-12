from ..modules.accounts import AccountsAPI
from ..modules.contacts import ContactsAPI
from ..modules.leads import LeadsAPI
from ..logging_config import setup_logging

logger = setup_logging('suitecrm.services.contact_manager')

class ContactManager:
    """Service class to manage contacts, accounts, and leads creation logic."""
    
    def __init__(self):
        self.accounts_api = AccountsAPI()
        self.contacts_api = ContactsAPI()
        self.leads_api = LeadsAPI()

    def handle_contact_creation(self, data: dict) -> dict:
        """
        Handle contact creation based on whether the account exists.
        If account doesn't exist, creates both account and lead.
        If account exists, creates a contact under that account.

        Args:
            data (dict): Dictionary containing contact information including:
                - company_name: Name of the company/account (required)
                - first_name: First name of the contact (required)
                - last_name: Last name of the contact (required)
                - email: Email address
                - phone_mobile: Mobile phone number
                - phone_work: Work phone number (optional)
                - website: Company website (optional)

        Returns:
            dict: Result of the operation including created records
        """
        try:
            # Validate required fields
            required_fields = ['company_name', 'first_name', 'last_name']
            for field in required_fields:
                if not data.get(field):
                    return {
                        'status': 'error',
                        'message': f'Missing required field: {field}'
                    }

            # First, search for the account
            logger.info(f"Searching for account: {data.get('company_name')}")
            account_search_result = self.accounts_api.search_accounts(
                data.get('company_name', ''), 
                field='name'
            )

            if 'error' in account_search_result:
                return account_search_result

            if not account_search_result.get('entry_list', []):
                # Account doesn't exist - create account and lead
                logger.info(f"Account not found: {data.get('company_name')} - Creating new account and lead")
                
                # Create account
                account_data = {
                    'name': data.get('company_name'),
                    'phone_office': data.get('phone_work'),
                    'website': data.get('website', '')
                }
                account_result = self.accounts_api.create_account(account_data)
                
                if 'error' in account_result:
                    return account_result
                
                # Create lead
                lead_data = {
                    'first_name': data.get('first_name'),
                    'last_name': data.get('last_name'),
                    'email1': data.get('email'),
                    'phone_mobile': data.get('phone_mobile'),
                    'account_name': data.get('company_name'),
                    'status': 'New',
                    'lead_source': 'Web'
                }
                lead_result = self.leads_api.create_lead(lead_data)
                
                if 'error' in lead_result:
                    return lead_result
                
                logger.info("Successfully created new account and lead")
                return {
                    'status': 'success',
                    'message': 'Created new account and lead',
                    'account': account_result,
                    'lead': lead_result
                }
            else:
                # Account exists - create contact under this account
                logger.info(f"Account found: {data.get('company_name')} - Creating contact")
                account_id = account_search_result['entry_list'][0]['id']
                
                contact_data = {
                    'first_name': data.get('first_name'),
                    'last_name': data.get('last_name'),
                    'email': data.get('email'),
                    'phone_mobile': data.get('phone_mobile'),
                    'account_id': account_id
                }
                
                contact_result = self.contacts_api.create_contact(contact_data)
                
                if 'error' in contact_result:
                    return contact_result
                
                logger.info("Successfully created contact under existing account")
                return {
                    'status': 'success',
                    'message': 'Contact created under existing account',
                    'contact': contact_result,
                    'account_id': account_id
                }

        except Exception as e:
            error_msg = f"Error in handle_contact_creation: {str(e)}"
            logger.error(error_msg)
            return {
                'status': 'error',
                'message': error_msg
            }