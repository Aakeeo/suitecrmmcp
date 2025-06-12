class SuiteCRMError(Exception):
    """Base exception for SuiteCRM related errors"""
    pass

class SuiteCRMAuthenticationError(SuiteCRMError):
    """Raised when authentication fails"""
    pass

class SuiteCRMAPIError(SuiteCRMError):
    """Raised when API calls fail"""
    pass