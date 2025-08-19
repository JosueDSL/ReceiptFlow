"""
Error codes and definitions for the ReceiptFlow application.
Centralized error code management using enums and dataclasses.
"""

from enum import Enum, IntEnum
from dataclasses import dataclass
from typing import Dict, Any, Optional


class HttpStatusCodes(IntEnum):
    """HTTP status codes enum"""
    # Success codes
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    
    # Client error codes
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    TOO_MANY_REQUESTS = 429
    
    # Server error codes
    INTERNAL_SERVER_ERROR = 500
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503


class ErrorCategories(Enum):
    """Error category classification"""
    VALIDATION = "validation"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    BUSINESS_LOGIC = "business_logic"
    SYSTEM = "system"
    EXTERNAL_SERVICE = "external_service"


@dataclass(frozen=True)
class ErrorDefinition:
    """Immutable error definition with all necessary information"""
    code: str
    http_status: HttpStatusCodes
    message: str
    category: ErrorCategories
    numeric_code: int
    user_message: Optional[str] = None
    
    @property
    def type_uri(self) -> str:
        """Generate RFC 7807 type URI"""
        return f"https://api.receiptflow.com/errors/{self.code.lower()}" # URL for reference
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "code": self.code,
            "http_status": int(self.http_status),
            "message": self.message,
            "category": self.category.value,
            "numeric_code": self.numeric_code,
            "type": self.type_uri,
            "user_message": self.user_message or self.message
        }


class PayloadErrorCodes:
    """Payload extraction and validation error codes"""
    
    # JSON Payload Errors (4000-4099)
    JSON_PAYLOAD_MISSING = ErrorDefinition(
        code="JSON_PAYLOAD_MISSING",
        http_status=HttpStatusCodes.BAD_REQUEST,
        message="No JSON payload found in request",
        category=ErrorCategories.VALIDATION,
        numeric_code=4000,
        user_message="Request must include valid JSON data"
    )
    
    JSON_PAYLOAD_INVALID = ErrorDefinition(
        code="JSON_PAYLOAD_INVALID", 
        http_status=HttpStatusCodes.BAD_REQUEST,
        message="Invalid JSON payload structure",
        category=ErrorCategories.VALIDATION,
        numeric_code=4001,
        user_message="Request contains invalid JSON format"
    )
    
    JSON_PARSE_ERROR = ErrorDefinition(
        code="JSON_PARSE_ERROR",
        http_status=HttpStatusCodes.BAD_REQUEST,
        message="Failed to parse JSON request",
        category=ErrorCategories.VALIDATION,
        numeric_code=4002,
        user_message="Request contains malformed JSON data"
    )
    
    # Image Payload Errors (4100-4199)
    IMAGE_PAYLOAD_MISSING = ErrorDefinition(
        code="IMAGE_PAYLOAD_MISSING",
        http_status=HttpStatusCodes.BAD_REQUEST,
        message="No image payload found in any supported format",
        category=ErrorCategories.VALIDATION,
        numeric_code=4100,
        user_message="Please provide a valid image file"
    )
    
    IMAGE_TOO_LARGE = ErrorDefinition(
        code="IMAGE_TOO_LARGE",
        http_status=HttpStatusCodes.BAD_REQUEST,
        message="Image too large for processing",
        category=ErrorCategories.VALIDATION,
        numeric_code=4101,
        user_message="Image file is too large. Please use a smaller image."
    )
    
    IMAGE_TOO_SMALL = ErrorDefinition(
        code="IMAGE_TOO_SMALL",
        http_status=HttpStatusCodes.BAD_REQUEST,
        message="Image too small or corrupted",
        category=ErrorCategories.VALIDATION,
        numeric_code=4102,
        user_message="Image file is too small or corrupted"
    )
    
    IMAGE_FORMAT_UNSUPPORTED = ErrorDefinition(
        code="IMAGE_FORMAT_UNSUPPORTED",
        http_status=HttpStatusCodes.BAD_REQUEST,
        message="Unsupported image format",
        category=ErrorCategories.VALIDATION,
        numeric_code=4103,
        user_message="Please use JPEG, PNG, GIF, or BMP image format"
    )
    
    BINARY_IMAGE_INVALID = ErrorDefinition(
        code="BINARY_IMAGE_INVALID",
        http_status=HttpStatusCodes.BAD_REQUEST,
        message="Invalid binary image data",
        category=ErrorCategories.VALIDATION,
        numeric_code=4104,
        user_message="Image data is corrupted or invalid"
    )
    
    # Multipart Errors (4200-4299)
    MULTIPART_FILE_EMPTY = ErrorDefinition(
        code="MULTIPART_FILE_EMPTY",
        http_status=HttpStatusCodes.BAD_REQUEST,
        message="No file selected in multipart upload",
        category=ErrorCategories.VALIDATION,
        numeric_code=4200,
        user_message="Please select a file to upload"
    )
    
    MULTIPART_FILE_INVALID = ErrorDefinition(
        code="MULTIPART_FILE_INVALID",
        http_status=HttpStatusCodes.BAD_REQUEST,
        message="Invalid image file format or size",
        category=ErrorCategories.VALIDATION,
        numeric_code=4201,
        user_message="Uploaded file is not a valid image"
    )


class AuthErrorCodes:
    """Authentication and authorization error codes"""
    
    # Authentication Errors (4300-4399)
    AUTHENTICATION_REQUIRED = ErrorDefinition(
        code="AUTHENTICATION_REQUIRED",
        http_status=HttpStatusCodes.UNAUTHORIZED,
        message="Authentication required",
        category=ErrorCategories.AUTHENTICATION,
        numeric_code=4300,
        user_message="Please log in to access this resource"
    )
    
    INVALID_CREDENTIALS = ErrorDefinition(
        code="INVALID_CREDENTIALS",
        http_status=HttpStatusCodes.UNAUTHORIZED,
        message="Invalid username or password",
        category=ErrorCategories.AUTHENTICATION,
        numeric_code=4301,
        user_message="Invalid username or password"
    )
    
    JWT_REQUIRED = ErrorDefinition(
        code="JWT_REQUIRED",
        http_status=HttpStatusCodes.UNAUTHORIZED,
        message="Valid JWT token required",
        category=ErrorCategories.AUTHENTICATION,
        numeric_code=4302,
        user_message="Please provide a valid authorization token"
    )
    
    # Authorization Errors (4400-4499)
    ACCESS_DENIED = ErrorDefinition(
        code="ACCESS_DENIED",
        http_status=HttpStatusCodes.FORBIDDEN,
        message="Access denied",
        category=ErrorCategories.AUTHORIZATION,
        numeric_code=4400,
        user_message="You don't have permission to access this resource"
    )


class BusinessLogicErrorCodes:
    """Business logic error codes"""
    
    # Receipt Processing Errors (4500-4599)
    RECEIPT_PROCESSING_FAILED = ErrorDefinition(
        code="RECEIPT_PROCESSING_FAILED",
        http_status=HttpStatusCodes.UNPROCESSABLE_ENTITY,
        message="Receipt processing failed",
        category=ErrorCategories.BUSINESS_LOGIC,
        numeric_code=4500,
        user_message="Unable to process receipt. Please try again."
    )
    
    DUPLICATE_RECEIPT = ErrorDefinition(
        code="DUPLICATE_RECEIPT",
        http_status=HttpStatusCodes.CONFLICT,
        message="Duplicate receipt detected",
        category=ErrorCategories.BUSINESS_LOGIC,
        numeric_code=4501,
        user_message="This receipt has already been uploaded"
    )

class ValidationErrorCodes:
    """General validation error codes"""
    
    # Field Validation Errors (4300-4399)
    REQUIRED_FIELDS_MISSING = ErrorDefinition(
        code="REQUIRED_FIELDS_MISSING",
        http_status=HttpStatusCodes.BAD_REQUEST,
        message="Missing required fields",
        category=ErrorCategories.VALIDATION,
        numeric_code=4300,
        user_message="Please provide all required fields"
    )
    
    INVALID_FIELD_TYPES = ErrorDefinition(
        code="INVALID_FIELD_TYPES",
        http_status=HttpStatusCodes.BAD_REQUEST,
        message="Invalid field types",
        category=ErrorCategories.VALIDATION,
        numeric_code=4301,
        user_message="One or more fields have invalid data types"
    )
    
    STRING_LENGTH_INVALID = ErrorDefinition(
        code="STRING_LENGTH_INVALID",
        http_status=HttpStatusCodes.BAD_REQUEST,
        message="String length validation failed",
        category=ErrorCategories.VALIDATION,
        numeric_code=4302,
        user_message="One or more text fields are too long or too short"
    )
    
    INVALID_EMAIL_FORMAT = ErrorDefinition(
        code="INVALID_EMAIL_FORMAT",
        http_status=HttpStatusCodes.BAD_REQUEST,
        message="Invalid email format",
        category=ErrorCategories.VALIDATION,
        numeric_code=4303,
        user_message="Please provide a valid email address"
    )
    
    INVALID_UUID_FORMAT = ErrorDefinition(
        code="INVALID_UUID_FORMAT",
        http_status=HttpStatusCodes.BAD_REQUEST,
        message="Invalid UUID format",
        category=ErrorCategories.VALIDATION,
        numeric_code=4304,
        user_message="Invalid identifier format"
    )
    
    INVALID_DATE_FORMAT = ErrorDefinition(
        code="INVALID_DATE_FORMAT",
        http_status=HttpStatusCodes.BAD_REQUEST,
        message="Invalid date format",
        category=ErrorCategories.VALIDATION,
        numeric_code=4305,
        user_message="Please provide date in the correct format"
    )
    
    NUMERIC_RANGE_INVALID = ErrorDefinition(
        code="NUMERIC_RANGE_INVALID",
        http_status=HttpStatusCodes.BAD_REQUEST,
        message="Numeric value out of range",
        category=ErrorCategories.VALIDATION,
        numeric_code=4306,
        user_message="One or more numeric values are outside the allowed range"
    )
    
    INVALID_FIELD_VALUES = ErrorDefinition(
        code="INVALID_FIELD_VALUES",
        http_status=HttpStatusCodes.BAD_REQUEST,
        message="Invalid field values",
        category=ErrorCategories.VALIDATION,
        numeric_code=4307,
        user_message="One or more fields contain invalid values"
    )
    
    INVALID_CONTENT_TYPE = ErrorDefinition(
        code="INVALID_CONTENT_TYPE",
        http_status=HttpStatusCodes.BAD_REQUEST,
        message="Invalid content type",
        category=ErrorCategories.VALIDATION,
        numeric_code=4308,
        user_message="Request content type is not supported"
    )
    
    FILE_TOO_LARGE = ErrorDefinition(
        code="FILE_TOO_LARGE",
        http_status=HttpStatusCodes.BAD_REQUEST,
        message="File too large",
        category=ErrorCategories.VALIDATION,
        numeric_code=4309,
        user_message="File size exceeds maximum allowed limit"
    )
    
    FILE_TOO_SMALL = ErrorDefinition(
        code="FILE_TOO_SMALL",
        http_status=HttpStatusCodes.BAD_REQUEST,
        message="File too small",
        category=ErrorCategories.VALIDATION,
        numeric_code=4310,
        user_message="File size is below minimum requirement"
    )
    
    MULTIPART_FILES_MISSING = ErrorDefinition(
        code="MULTIPART_FILES_MISSING",
        http_status=HttpStatusCodes.BAD_REQUEST,
        message="No files found in multipart request",
        category=ErrorCategories.VALIDATION,
        numeric_code=4311,
        user_message="Please select files to upload"
    )


class SystemErrorCodes:
    """System and infrastructure error codes"""
    
    # Generic System Errors (5000-5099)
    INTERNAL_SERVER_ERROR = ErrorDefinition(
        code="INTERNAL_SERVER_ERROR",
        http_status=HttpStatusCodes.INTERNAL_SERVER_ERROR,
        message="An unexpected error occurred",
        category=ErrorCategories.SYSTEM,
        numeric_code=5000,
        user_message="An unexpected error occurred. Please try again or contact support."
    )
    
    SERVICE_UNAVAILABLE = ErrorDefinition(
        code="SERVICE_UNAVAILABLE",
        http_status=HttpStatusCodes.SERVICE_UNAVAILABLE,
        message="Service temporarily unavailable",
        category=ErrorCategories.SYSTEM,
        numeric_code=5001,
        user_message="Service is temporarily unavailable. Please try again later."
    )


# Central error registry for easy access
class ErrorCodes:
    """Central registry of all error codes"""
    
    # Payload errors
    JSON_PAYLOAD_MISSING = PayloadErrorCodes.JSON_PAYLOAD_MISSING
    JSON_PAYLOAD_INVALID = PayloadErrorCodes.JSON_PAYLOAD_INVALID
    JSON_PARSE_ERROR = PayloadErrorCodes.JSON_PARSE_ERROR
    IMAGE_PAYLOAD_MISSING = PayloadErrorCodes.IMAGE_PAYLOAD_MISSING
    IMAGE_TOO_LARGE = PayloadErrorCodes.IMAGE_TOO_LARGE
    IMAGE_TOO_SMALL = PayloadErrorCodes.IMAGE_TOO_SMALL
    IMAGE_FORMAT_UNSUPPORTED = PayloadErrorCodes.IMAGE_FORMAT_UNSUPPORTED
    BINARY_IMAGE_INVALID = PayloadErrorCodes.BINARY_IMAGE_INVALID
    MULTIPART_FILE_EMPTY = PayloadErrorCodes.MULTIPART_FILE_EMPTY
    MULTIPART_FILE_INVALID = PayloadErrorCodes.MULTIPART_FILE_INVALID
    
    # Auth errors
    AUTHENTICATION_REQUIRED = AuthErrorCodes.AUTHENTICATION_REQUIRED
    INVALID_CREDENTIALS = AuthErrorCodes.INVALID_CREDENTIALS
    JWT_REQUIRED = AuthErrorCodes.JWT_REQUIRED
    ACCESS_DENIED = AuthErrorCodes.ACCESS_DENIED
    
    # Business logic errors
    RECEIPT_PROCESSING_FAILED = BusinessLogicErrorCodes.RECEIPT_PROCESSING_FAILED
    DUPLICATE_RECEIPT = BusinessLogicErrorCodes.DUPLICATE_RECEIPT

    # Validation errors
    REQUIRED_FIELDS_MISSING = ValidationErrorCodes.REQUIRED_FIELDS_MISSING
    INVALID_FIELD_TYPES = ValidationErrorCodes.INVALID_FIELD_TYPES
    STRING_LENGTH_INVALID = ValidationErrorCodes.STRING_LENGTH_INVALID
    INVALID_EMAIL_FORMAT = ValidationErrorCodes.INVALID_EMAIL_FORMAT
    INVALID_UUID_FORMAT = ValidationErrorCodes.INVALID_UUID_FORMAT
    INVALID_DATE_FORMAT = ValidationErrorCodes.INVALID_DATE_FORMAT
    NUMERIC_RANGE_INVALID = ValidationErrorCodes.NUMERIC_RANGE_INVALID
    INVALID_FIELD_VALUES = ValidationErrorCodes.INVALID_FIELD_VALUES
    INVALID_CONTENT_TYPE = ValidationErrorCodes.INVALID_CONTENT_TYPE
    FILE_TOO_LARGE = ValidationErrorCodes.FILE_TOO_LARGE
    FILE_TOO_SMALL = ValidationErrorCodes.FILE_TOO_SMALL
    MULTIPART_FILES_MISSING = ValidationErrorCodes.MULTIPART_FILES_MISSING
    
    # System errors
    INTERNAL_SERVER_ERROR = SystemErrorCodes.INTERNAL_SERVER_ERROR
    SERVICE_UNAVAILABLE = SystemErrorCodes.SERVICE_UNAVAILABLE
    
    @classmethod
    def get_by_code(cls, code: str) -> Optional[ErrorDefinition]:
        """Get error definition by code string"""
        for attr_name in dir(cls):
            if not attr_name.startswith('_') and attr_name != 'get_by_code':
                attr = getattr(cls, attr_name)
                if isinstance(attr, ErrorDefinition) and attr.code == code:
                    return attr
        return None
    
    @classmethod
    def get_by_numeric_code(cls, numeric_code: int) -> Optional[ErrorDefinition]:
        """Get error definition by numeric code"""
        for attr_name in dir(cls):
            if not attr_name.startswith('_') and attr_name != 'get_by_numeric_code':
                attr = getattr(cls, attr_name)
                if isinstance(attr, ErrorDefinition) and attr.numeric_code == numeric_code:
                    return attr
        return None