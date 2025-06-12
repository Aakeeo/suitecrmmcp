from .modules.contacts import ContactsAPI
from .modules.accounts import AccountsAPI
from .modules.leads import LeadsAPI
from .modules.opportunities import OpportunitiesAPI
from .services.contact_manager import ContactManager

# Export the main classes
__all__ = ['ContactsAPI', 'AccountsAPI', 'LeadsAPI', 'OpportunitiesAPI', 'ContactManager']