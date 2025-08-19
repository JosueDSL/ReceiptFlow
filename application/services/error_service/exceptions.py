"""
Exception hierarchy with structured error codes.
All custom exceptions for the ReceiptFlow application.
"""

from typing import Optional, Dict, Any
from .error_codes import ErrorDefinition, ErrorCodes


class ReceiptFlowException(Exception):
    """Base exception for all ReceiptFlow-specific errors"""
    
    def __init__(self, error_def: ErrorDefinition, details: Optional[Dict[str, Any]] = None):
        super().__init__(error_def.message)
        self.error_definition = error_def
        self.details = details or {}
    
    @property
    def message(self) -> str:
        return self.error_definition.message
    
    @property
    def user_message(self) -> str:
        return self.error_definition.user_message
    
    @property
    def code(self) -> str:
        return self.error_definition.code
    
    @property
    def numeric_code(self) -> int:
        return self.error_definition.numeric_code
    
    @property
    def http_status(self) -> int:
        return int(self.error_definition.http_status)
    
    @property
    def category(self) -> str:
        # Return the string value, not the enum
        return self.error_definition.category.value
    
    @property
    def type_uri(self) -> str:
        return self.error_definition.type_uri
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to JSON-serializable dictionary"""
        return {
            "code": self.code,
            "message": self.message,
            "user_message": self.user_message,
            "http_status": self.http_status,
            "category": self.category,  # This will be a string now
            "numeric_code": self.numeric_code,
            "type": self.type_uri,
            "details": self.details
        }


class ValidationError(ReceiptFlowException):
    """Raised when field-specific validation fails"""
    
    def __init__(self, error_def: ErrorDefinition, field: str = None, details: Optional[Dict[str, Any]] = None):
        # Add field information to details
        if details is None:
            details = {}
        if field:
            details['field'] = field
            
        super().__init__(error_def, details)
        self.field = field


class RequestValidationError(ReceiptFlowException):
    """Raised when general request validation fails"""
    
    def __init__(self, error_def: ErrorDefinition, details: Optional[Dict[str, Any]] = None):
        super().__init__(error_def, details)


class PayloadExtractionError(ReceiptFlowException):
    """Raised when payload extraction fails"""
    
    def __init__(self, error_def: ErrorDefinition, details: Optional[Dict[str, Any]] = None):
        super().__init__(error_def, details)


class ImageValidationError(ReceiptFlowException):
    """Raised when image validation fails"""
    
    def __init__(self, error_def: ErrorDefinition, details: Optional[Dict[str, Any]] = None):
        super().__init__(error_def, details)


class AuthenticationError(ReceiptFlowException):
    """Raised when authentication fails"""
    
    def __init__(self, error_def: ErrorDefinition = None, details: Optional[Dict[str, Any]] = None):
        error_def = error_def or ErrorCodes.AUTHENTICATION_REQUIRED
        super().__init__(error_def, details)


class AuthorizationError(ReceiptFlowException):
    """Raised when authorization fails"""
    
    def __init__(self, error_def: ErrorDefinition = None, details: Optional[Dict[str, Any]] = None):
        error_def = error_def or ErrorCodes.ACCESS_DENIED
        super().__init__(error_def, details)


class BusinessLogicError(ReceiptFlowException):
    """Raised when business logic validation fails"""
    
    def __init__(self, error_def: ErrorDefinition, details: Optional[Dict[str, Any]] = None):
        super().__init__(error_def, details)


class ResourceNotFoundError(ReceiptFlowException):
    """Raised when a requested resource is not found"""
    
    def __init__(self, resource: str, identifier: str = None):
        from .error_codes import ErrorDefinition, HttpStatusCodes, ErrorCategories
        
        message = f"{resource} not found"
        if identifier:
            message += f" with identifier: {identifier}"
            
        error_def = ErrorDefinition(
            code="RESOURCE_NOT_FOUND",
            http_status=HttpStatusCodes.NOT_FOUND,
            message=message,
            category=ErrorCategories.BUSINESS_LOGIC,
            numeric_code=4404,
            user_message=f"The requested {resource.lower()} could not be found"
        )
        
        details = {"resource": resource}
        if identifier:
            details["identifier"] = identifier
            
        super().__init__(error_def, details)