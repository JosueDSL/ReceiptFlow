"""
Request validation services with structured error codes.
Provides validation utilities for different types of requests and data.
"""

from flask import request
from typing import Dict, Any, List, Optional, Union
import re
from datetime import datetime
import logging

from application.services.error_service.exceptions import RequestValidationError, ValidationError
from application.services.error_service.error_codes import ErrorCodes

logger = logging.getLogger(__name__)


class RequestValidator:
    """Comprehensive request validation utilities"""
    
    # Common validation patterns
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    UUID_PATTERN = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$', re.IGNORECASE)
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> None:
        """
        Validate that all required fields are present in the data
        
        Args:
            data: Dictionary to validate
            required_fields: List of required field names
            
        Raises:
            RequestValidationError: If any required field is missing
        """
        missing_fields = []
        
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == '':
                missing_fields.append(field)
        
        if missing_fields:
            raise RequestValidationError(
                ErrorCodes.REQUIRED_FIELDS_MISSING,
                details={"missing_fields": missing_fields}
            )
    
    @staticmethod
    def validate_field_types(data: Dict[str, Any], field_types: Dict[str, type]) -> None:
        """
        Validate that fields have the correct types
        
        Args:
            data: Dictionary to validate
            field_types: Dictionary mapping field names to expected types
            
        Raises:
            RequestValidationError: If any field has wrong type
        """
        type_errors = []
        
        for field, expected_type in field_types.items():
            if field in data and data[field] is not None:
                if not isinstance(data[field], expected_type):
                    type_errors.append({
                        "field": field,
                        "expected": expected_type.__name__,
                        "actual": type(data[field]).__name__
                    })
        
        if type_errors:
            raise RequestValidationError(
                ErrorCodes.INVALID_FIELD_TYPES,
                details={"type_errors": type_errors}
            )
    
    @staticmethod
    def validate_string_length(data: Dict[str, Any], field_lengths: Dict[str, Dict[str, int]]) -> None:
        """
        Validate string field lengths
        
        Args:
            data: Dictionary to validate
            field_lengths: Dictionary mapping field names to min/max length constraints
                          Example: {"username": {"min": 3, "max": 50}}
            
        Raises:
            RequestValidationError: If any string field violates length constraints
        """
        length_errors = []
        
        for field, constraints in field_lengths.items():
            if field in data and isinstance(data[field], str):
                value_length = len(data[field])
                min_length = constraints.get('min', 0)
                max_length = constraints.get('max', float('inf'))
                
                if value_length < min_length:
                    length_errors.append({
                        "field": field,
                        "length": value_length,
                        "min_required": min_length,
                        "error": "too_short"
                    })
                elif value_length > max_length:
                    length_errors.append({
                        "field": field,
                        "length": value_length,
                        "max_allowed": max_length,
                        "error": "too_long"
                    })
        
        if length_errors:
            raise RequestValidationError(
                ErrorCodes.STRING_LENGTH_INVALID,
                details={"length_errors": length_errors}
            )
    
    @staticmethod
    def validate_email(email: str, field_name: str = "email") -> None:
        """
        Validate email format
        
        Args:
            email: Email string to validate
            field_name: Name of the field for error reporting
            
        Raises:
            ValidationError: If email format is invalid
        """
        if not RequestValidator.EMAIL_PATTERN.match(email):
            raise ValidationError(
                ErrorCodes.INVALID_EMAIL_FORMAT,
                field=field_name,
                details={"provided_email": email}
            )
    
    @staticmethod
    def validate_uuid(uuid_str: str, field_name: str = "id") -> None:
        """
        Validate UUID format
        
        Args:
            uuid_str: UUID string to validate
            field_name: Name of the field for error reporting
            
        Raises:
            ValidationError: If UUID format is invalid
        """
        if not RequestValidator.UUID_PATTERN.match(str(uuid_str)):
            raise ValidationError(
                ErrorCodes.INVALID_UUID_FORMAT,
                field=field_name,
                details={"provided_uuid": str(uuid_str)}
            )
    
    @staticmethod
    def validate_numeric_range(data: Dict[str, Any], field_ranges: Dict[str, Dict[str, Union[int, float]]]) -> None:
        """
        Validate numeric field ranges
        
        Args:
            data: Dictionary to validate
            field_ranges: Dictionary mapping field names to min/max constraints
                         Example: {"price": {"min": 0, "max": 10000}}
            
        Raises:
            RequestValidationError: If any numeric field is out of range
        """
        range_errors = []
        
        for field, constraints in field_ranges.items():
            if field in data and isinstance(data[field], (int, float)):
                value = data[field]
                min_value = constraints.get('min', float('-inf'))
                max_value = constraints.get('max', float('inf'))
                
                if value < min_value:
                    range_errors.append({
                        "field": field,
                        "value": value,
                        "min_allowed": min_value,
                        "error": "below_minimum"
                    })
                elif value > max_value:
                    range_errors.append({
                        "field": field,
                        "value": value,
                        "max_allowed": max_value,
                        "error": "above_maximum"
                    })
        
        if range_errors:
            raise RequestValidationError(
                ErrorCodes.NUMERIC_RANGE_INVALID,
                details={"range_errors": range_errors}
            )
    
    @staticmethod
    def validate_date_format(date_str: str, field_name: str = "date", date_format: str = "%Y-%m-%d") -> datetime:
        """
        Validate and parse date string
        
        Args:
            date_str: Date string to validate
            field_name: Name of the field for error reporting
            date_format: Expected date format
            
        Returns:
            datetime: Parsed datetime object
            
        Raises:
            ValidationError: If date format is invalid
        """
        try:
            return datetime.strptime(date_str, date_format)
        except ValueError:
            raise ValidationError(
                ErrorCodes.INVALID_DATE_FORMAT,
                field=field_name,
                details={
                    "provided_date": date_str,
                    "expected_format": date_format
                }
            )
    
    @staticmethod
    def validate_allowed_values(data: Dict[str, Any], field_values: Dict[str, List[Any]]) -> None:
        """
        Validate that fields contain only allowed values
        
        Args:
            data: Dictionary to validate
            field_values: Dictionary mapping field names to lists of allowed values
                         Example: {"status": ["active", "inactive", "pending"]}
            
        Raises:
            RequestValidationError: If any field contains disallowed values
        """
        value_errors = []
        
        for field, allowed_values in field_values.items():
            if field in data and data[field] not in allowed_values:
                value_errors.append({
                    "field": field,
                    "provided_value": data[field],
                    "allowed_values": allowed_values
                })
        
        if value_errors:
            raise RequestValidationError(
                ErrorCodes.INVALID_FIELD_VALUES,
                details={"value_errors": value_errors}
            )
    
    @staticmethod
    def validate_content_type(expected_types: List[str]) -> None:
        """
        Validate request content type
        
        Args:
            expected_types: List of acceptable content types
            
        Raises:
            RequestValidationError: If content type is not acceptable
        """
        content_type = request.content_type
        
        if not content_type or not any(expected_type in content_type for expected_type in expected_types):
            raise RequestValidationError(
                ErrorCodes.INVALID_CONTENT_TYPE,
                details={
                    "provided_content_type": content_type,
                    "expected_types": expected_types
                }
            )
    
    @staticmethod
    def validate_file_size(file_size: int, max_size: int = 10 * 1024 * 1024, min_size: int = 1024) -> None:
        """
        Validate file size constraints
        
        Args:
            file_size: Size of the file in bytes
            max_size: Maximum allowed size in bytes (default: 10MB)
            min_size: Minimum allowed size in bytes (default: 1KB)
            
        Raises:
            RequestValidationError: If file size is invalid
        """
        if file_size > max_size:
            raise RequestValidationError(
                ErrorCodes.FILE_TOO_LARGE,
                details={
                    "file_size": file_size,
                    "max_size": max_size,
                    "max_size_mb": max_size / 1024 / 1024
                }
            )
        
        if file_size < min_size:
            raise RequestValidationError(
                ErrorCodes.FILE_TOO_SMALL,
                details={
                    "file_size": file_size,
                    "min_size": min_size
                }
            )


class ReceiptValidationMixin:
    """Specific validation rules for receipt-related requests"""
    
    @staticmethod
    def validate_receipt_upload_request() -> None:
        """Validate receipt upload request structure and content"""
        
        # Validate content type for image uploads
        RequestValidator.validate_content_type([
            'image/jpeg', 
            'image/png', 
            'multipart/form-data'
        ])
        
        # If multipart, validate file presence
        if 'multipart/form-data' in (request.content_type or ''):
            if not request.files:
                raise RequestValidationError(ErrorCodes.MULTIPART_FILES_MISSING)

class AuthValidationMixin:
    """Specific validation rules for authentication requests"""
    
    @staticmethod
    def validate_login_request(login_data: Dict[str, Any]) -> None:
        """
        Validate login request data
        
        Args:
            login_data: Login data to validate
        """
        required_fields = ['username', 'password']
        RequestValidator.validate_required_fields(login_data, required_fields)
        
        field_types = {
            'username': str,
            'password': str
        }
        RequestValidator.validate_field_types(login_data, field_types)
        
        field_lengths = {
            'username': {'min': 3, 'max': 50},
            'password': {'min': 8, 'max': 128}
        }
        RequestValidator.validate_string_length(login_data, field_lengths)
    
    @staticmethod
    def validate_registration_request(registration_data: Dict[str, Any]) -> None:
        """
        Validate user registration request data
        
        Args:
            registration_data: Registration data to validate
        """
        required_fields = ['username', 'email', 'password']
        RequestValidator.validate_required_fields(registration_data, required_fields)
        
        field_types = {
            'username': str,
            'email': str,
            'password': str
        }
        RequestValidator.validate_field_types(registration_data, field_types)
        
        field_lengths = {
            'username': {'min': 3, 'max': 50},
            'password': {'min': 8, 'max': 128}
        }
        RequestValidator.validate_string_length(registration_data, field_lengths)
        
        # Email validation
        RequestValidator.validate_email(registration_data['email'])


""" Convenience functions for common validation scenarios """
def validate_json_request(
    data: Dict[str, Any],
    required_fields: Optional[List[str]] = None,
    field_types: Optional[Dict[str, type]] = None,
    field_lengths: Optional[Dict[str, Dict[str, int]]] = None
) -> None:
    """
    Convenience function for common JSON request validation
    
    Args:
        data: Data to validate
        required_fields: List of required field names
        field_types: Dictionary of field name to type mappings
        field_lengths: Dictionary of field name to length constraint mappings
    """
    if required_fields:
        RequestValidator.validate_required_fields(data, required_fields)
    
    if field_types:
        RequestValidator.validate_field_types(data, field_types)
    
    if field_lengths:
        RequestValidator.validate_string_length(data, field_lengths)


def validate_pagination_params(
    page: Optional[int] = None, 
    per_page: Optional[int] = None,
    max_per_page: int = 100
) -> Dict[str, int]:
    """
    Validate pagination parameters
    
    Args:
        page: Page number
        per_page: Items per page
        max_per_page: Maximum items per page allowed
        
    Returns:
        Dict with validated pagination parameters
    """
    validated_page = max(1, page or 1)
    validated_per_page = min(max_per_page, max(1, per_page or 20))
    
    return {
        'page': validated_page,
        'per_page': validated_per_page,
        'offset': (validated_page - 1) * validated_per_page
    }