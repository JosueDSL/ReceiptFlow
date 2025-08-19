"""
Request handling decorators for consistent error handling across all endpoints.
"""

from functools import wraps
from flask_jwt_extended.exceptions import NoAuthorizationError
from werkzeug.exceptions import HTTPException

from application.services.error_service import (
    ErrorResponseHandler,
    ReceiptFlowException
)
from application.services.error_service.error_codes import ErrorCodes


def handle_request_exceptions(func):
    """
    Comprehensive exception handling decorator for Flask routes.
    Provides centralized error handling for all common exceptions.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        
        except ReceiptFlowException as e:
            # This handles ALL ReceiptFlow exceptions with structured error codes
            return ErrorResponseHandler.handle_receiptflow_exception(e)
        
        except NoAuthorizationError as e:
            # Convert to ReceiptFlowException for consistency
            from application.services.error_service.exceptions import AuthenticationError
            auth_error = AuthenticationError(ErrorCodes.JWT_REQUIRED)
            return ErrorResponseHandler.handle_receiptflow_exception(auth_error)
        
        except HTTPException as e:
            return ErrorResponseHandler.make_error_response(
                e.description or e.name,
                e.code,
                e.name.upper().replace(' ', '_')
            )
        
        except ValueError as e:
            return ErrorResponseHandler.make_error_response(
                str(e), 
                400, 
                "VALUE_ERROR"
            )
        
        except Exception as e:
            return ErrorResponseHandler.handle_general_exception(e)
    
    return wrapper