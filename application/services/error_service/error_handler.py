"""
Production-ready error handler following RFC 7807 standard.
Centralized error handling and response formatting.
"""

from flask import jsonify, current_app as app, request
from werkzeug.exceptions import HTTPException
import logging
import traceback
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

from .exceptions import ReceiptFlowException

logger = logging.getLogger(__name__)


class ErrorResponseHandler:
    """Production-ready error response handler"""
    
    @staticmethod
    def make_error_response(
        message: str,
        status_code: int = 400,
        error_code: str = None,
        error_type: str = None,
        instance: str = None,
        details: Dict[str, Any] = None
    ) -> Tuple[Dict[str, Any], int]:
        """Create RFC 7807 compliant error response"""
        
        error_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        error_response = {
            "type": error_type or f"https://api.receiptflow.com/errors/{error_code or 'generic'}",
            "title": ErrorResponseHandler._get_status_title(status_code),
            "status": status_code,
            "detail": message,
            "instance": instance or (request.path if request else None),
            "timestamp": timestamp,
            "error_id": error_id
        }
        
        if error_code:
            error_response["code"] = error_code
            
        if details:
            error_response["details"] = details
        
        if app.config.get('DEBUG'):
            error_response["debug"] = {
                "request_id": getattr(request, 'id', None) if request else None,
                "user_agent": request.headers.get('User-Agent') if request else None,
                "method": request.method if request else None,
                "url": request.url if request else None
            }
        
        logger.error(
            f"Error {error_id}: {message}",
            extra={
                "error_id": error_id,
                "status_code": status_code,
                "error_code": error_code,
                "path": request.path if request else None
            }
        )
        
        return jsonify(error_response), status_code
    
    @staticmethod
    def handle_receiptflow_exception(e: ReceiptFlowException) -> Tuple[Dict[str, Any], int]:
        """Handle all ReceiptFlow-specific exceptions with structured error codes"""
        
        error_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        # Build error response using exception properties (which are now JSON-safe)
        error_response = {
            "type": e.type_uri,
            "title": ErrorResponseHandler._get_status_title(e.http_status),
            "status": e.http_status,
            "detail": e.user_message,
            "code": e.code,
            "numeric_code": e.numeric_code,
            "category": e.category,  # This is now a string, not an enum
            "instance": request.path if request else None,
            "timestamp": timestamp,
            "error_id": error_id
        }
        
        # Add details if present
        if e.details:
            error_response["details"] = e.details
        
        # Add debug info in development
        if app.config.get('DEBUG'):
            error_response["debug"] = {
                "technical_message": e.message,
                "exception_type": type(e).__name__,
                "request_id": getattr(request, 'id', None) if request else None,
                "user_agent": request.headers.get('User-Agent') if request else None,
                "method": request.method if request else None,
                "url": request.url if request else None
            }
        
        # Log with structured data
        logger.error(
            f"ReceiptFlow error {error_id}: {e.code} - {e.message}",
            extra={
                "error_id": error_id,
                "error_code": e.code,
                "numeric_code": e.numeric_code,
                "category": e.category,
                "http_status": e.http_status,
                "path": request.path if request else None
            }
        )
        
        return jsonify(error_response), e.http_status
    
    @staticmethod
    def handle_general_exception(e: Exception) -> Tuple[Dict[str, Any], int]:
        """Handle unexpected errors with proper logging"""
        error_id = str(uuid.uuid4())
        
        logger.error(
            f"Unexpected error {error_id}: {str(e)}",
            extra={"error_id": error_id, "exception": str(e)},
            exc_info=True
        )
        
        if app.config.get('DEBUG'):
            details = {
                "exception_type": type(e).__name__,
                "traceback": traceback.format_exc().split('\n')
            }
            message = f"Unexpected error: {str(e)}"
        else:
            details = None
            message = "An unexpected error occurred. Please try again or contact support."
        
        return ErrorResponseHandler.make_error_response(
            message=message,
            status_code=500,
            error_code="INTERNAL_SERVER_ERROR",
            details=details
        )
    
    @staticmethod
    def _get_status_title(status_code: int) -> str:
        """Get standard HTTP status titles"""
        titles = {
            400: "Bad Request",
            401: "Unauthorized", 
            403: "Forbidden",
            404: "Not Found",
            405: "Method Not Allowed",
            409: "Conflict",
            422: "Unprocessable Entity",
            429: "Too Many Requests",
            500: "Internal Server Error",
            502: "Bad Gateway",
            503: "Service Unavailable"
        }
        return titles.get(status_code, "Error")