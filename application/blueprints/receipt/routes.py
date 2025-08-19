from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from application.blueprints.decorators import handle_request_exceptions
from application.services.request_service import extract_image_payload
from application.services.error_service.exceptions import ImageValidationError
from application.services.error_service.error_codes import ErrorCodes

# Create a blueprint object
receipt_bp = Blueprint('receipt', __name__)

@receipt_bp.route('/upload', methods=['POST'])
@handle_request_exceptions
# @jwt_required()
def upload_receipt_endpoint():
    """Upload receipt image with comprehensive validation and error handling"""
    
    # Extract image payload using the service
    payload = extract_image_payload()
    
    # Business logic can raise specific exceptions using ErrorCodes
    if isinstance(payload, dict) and payload.get('size', 0) > 5 * 1024 * 1024:
        # Create a custom error definition for this business rule
        from application.services.error_service.error_codes import ErrorDefinition, HttpStatusCodes, ErrorCategories
        
        processing_limit_error = ErrorDefinition(
            code="IMAGE_TOO_LARGE_FOR_PROCESSING",
            http_status=HttpStatusCodes.BAD_REQUEST,
            message="Receipt images should be under 5MB for optimal processing",
            category=ErrorCategories.BUSINESS_LOGIC,
            numeric_code=4102,
            user_message="Please use a smaller image for faster processing"
        )
        
        raise ImageValidationError(
            processing_limit_error,
            details={"size": payload['size'], "limit": 5 * 1024 * 1024}
        )
    
    # Handle different payload types
    if isinstance(payload, dict) and 'data' in payload:
        return jsonify({
            'message': 'Receipt image uploaded successfully!',
            'size': payload['size'],
            'content_type': payload['content_type'],
            'source': payload['source'],
            'success': True
        })
    else:
        filename = getattr(payload, 'filename', 'unknown')
        return jsonify({
            'message': 'Receipt file uploaded successfully!',
            'filename': filename,
            'source': 'multipart',
            'success': True
        })