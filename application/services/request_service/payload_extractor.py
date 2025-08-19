"""
Payload extraction services with structured error codes.
Supports JSON, image, and multipart form data extraction with validation.
"""

from flask import request, current_app as app
from abc import ABC, abstractmethod
from typing import Union, Dict, Any
import logging

from application.services.error_service.exceptions import PayloadExtractionError, ImageValidationError
from application.services.error_service.error_codes import ErrorCodes

logger = logging.getLogger(__name__)


class PayloadExtractor(ABC):
    """Abstract base class for payload extraction strategies"""
    
    @abstractmethod
    def extract(self) -> Union[Dict[str, Any], Any]:
        """Extract and validate payload from request"""
        pass
    
    @abstractmethod
    def validate(self, payload: Any) -> bool:
        """Validate the extracted payload"""
        pass


class ImagePayloadExtractor(PayloadExtractor):
    """Handles image payload extraction from various sources with comprehensive validation"""
    
    IMAGE_SIGNATURES = {
        b'\xff\xd8\xff': 'image/jpeg',
        b'\x89\x50\x4e\x47': 'image/png',
    }
    
    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
    MIN_IMAGE_SIZE = 1024  # 1KB
    
    def extract(self) -> Union[Dict[str, Any], Any]:
        """Extract image payload using multiple strategies"""
        
        self._log_request_debug_info()
        
        try:
            # Strategy 1: Multipart file upload
            if request.files:
                return self._extract_from_files()
            
            # Strategy 2: Raw binary data (primary for mobile)
            if request.data and len(request.data) > 0:
                return self._extract_from_binary()
            
            # Strategy 3: Base64 in JSON
            if request.is_json and request.json:
                return self._extract_from_json()
            
            # Strategy 4: Form data
            if request.form:
                return self._extract_from_form()
            
            raise PayloadExtractionError(ErrorCodes.IMAGE_PAYLOAD_MISSING)
            
        except ImageValidationError:
            raise
        except PayloadExtractionError:
            raise
        except Exception as e:
            logger.error(f"Image extraction failed: {str(e)}")
            raise PayloadExtractionError(
                ErrorCodes.IMAGE_PAYLOAD_MISSING, 
                details={"original_error": str(e)}
            )
    
    def validate(self, payload: Any) -> bool:
        """Validate extracted image payload"""
        if isinstance(payload, dict) and 'data' in payload:
            return self._validate_binary_image(payload['data'])
        return True
    
    def _extract_from_files(self) -> Any:
        """Extract from multipart/form-data files"""
        logger.info("Extracting image from multipart files")
        
        file_key = 'image' if 'image' in request.files else list(request.files.keys())[0]
        file_obj = request.files[file_key]
        
        if file_obj.filename == '':
            raise PayloadExtractionError(ErrorCodes.MULTIPART_FILE_EMPTY)
        
        file_data = file_obj.read()
        if not self._validate_binary_image(file_data):
            raise ImageValidationError(ErrorCodes.MULTIPART_FILE_INVALID)
        
        file_obj.seek(0)
        return file_obj
    
    def _extract_from_binary(self) -> Dict[str, Any]:
        """Extract from raw binary request body"""
        logger.info(f"Extracting raw binary image: {len(request.data)} bytes")
        
        if not self._validate_binary_image(request.data):
            raise ImageValidationError(ErrorCodes.BINARY_IMAGE_INVALID)
        
        content_type = self._detect_image_type(request.data) or request.content_type or 'application/octet-stream'
        
        return {
            'data': request.data,
            'content_type': content_type,
            'size': len(request.data),
            'source': 'binary'
        }
    
    def _extract_from_json(self) -> Dict[str, Any]:
        """Extract from JSON payload (base64 encoded)"""
        logger.info("Extracting image from JSON payload")
        
        json_data = request.json
        image_keys = ['image', 'file', 'data', 'photo']
        
        for key in image_keys:
            if key in json_data:
                return {**json_data, 'source': 'json'}
        
        raise PayloadExtractionError(ErrorCodes.IMAGE_PAYLOAD_MISSING)
    
    def _extract_from_form(self) -> Dict[str, Any]:
        """Extract from form data"""
        logger.info("Extracting image from form data")
        
        form_data = dict(request.form)
        form_data['source'] = 'form'
        return form_data
    
    def _validate_binary_image(self, image_data: bytes) -> bool:
        """Validate binary image data"""
        
        if len(image_data) > self.MAX_IMAGE_SIZE:
            raise ImageValidationError(
                ErrorCodes.IMAGE_TOO_LARGE,
                details={"size": len(image_data), "max_size": self.MAX_IMAGE_SIZE}
            )
        
        if len(image_data) < self.MIN_IMAGE_SIZE:
            raise ImageValidationError(
                ErrorCodes.IMAGE_TOO_SMALL,
                details={"size": len(image_data), "min_size": self.MIN_IMAGE_SIZE}
            )
        
        if not self._detect_image_type(image_data):
            raise ImageValidationError(ErrorCodes.IMAGE_FORMAT_UNSUPPORTED)
        
        return True
    
    def _detect_image_type(self, image_data: bytes) -> str:
        """Detect image type from magic numbers"""
        for signature, mime_type in self.IMAGE_SIGNATURES.items():
            if image_data.startswith(signature):
                return mime_type
        return None
    
    def _log_request_debug_info(self):
        """Log comprehensive request debugging information"""
        if app.config.get('DEBUG'):
            logger.debug("=== REQUEST DEBUG INFO ===")
            logger.debug(f"Method: {request.method}")
            logger.debug(f"Content-Type: {request.content_type}")
            logger.debug(f"Content-Length: {request.content_length}")
            logger.debug(f"Files: {list(request.files.keys())}")
            logger.debug(f"Form keys: {list(request.form.keys())}")
            logger.debug(f"Args: {dict(request.args)}")
            
            if request.data:
                logger.debug(f"Binary data: {len(request.data)} bytes")
                logger.debug(f"Data preview (hex): {request.data[:20].hex()}")
            
            logger.debug("========================")


class JSONPayloadExtractor(PayloadExtractor):
    """Handles JSON payload extraction and validation"""
    
    def extract(self) -> Dict[str, Any]:
        """Extract JSON payload from request"""
        try:
            payload = request.get_json()
            if payload is None:
                raise PayloadExtractionError(ErrorCodes.JSON_PAYLOAD_MISSING)
            
            if not self.validate(payload):
                raise PayloadExtractionError(ErrorCodes.JSON_PAYLOAD_INVALID)
            
            return payload
            
        except Exception as e:
            if isinstance(e, PayloadExtractionError):
                raise
            
            logger.error(f"JSON extraction failed: {str(e)}")
            raise PayloadExtractionError(
                ErrorCodes.JSON_PARSE_ERROR,
                details={"original_error": str(e)}
            )
    
    def validate(self, payload: Any) -> bool:
        """Validate JSON payload structure"""
        return isinstance(payload, dict)


class PayloadExtractorFactory:
    """Factory for creating appropriate payload extractors"""
    
    @staticmethod
    def get_extractor(payload_type: str) -> PayloadExtractor:
        """Get appropriate extractor based on payload type"""
        extractors = {
            'json': JSONPayloadExtractor,
            'image': ImagePayloadExtractor
        }
        
        extractor_class = extractors.get(payload_type.lower())
        if not extractor_class:
            raise ValueError(f"Unsupported payload type: {payload_type}")
        
        return extractor_class()


# Convenience functions for easy usage
def extract_json_payload() -> Dict[str, Any]:
    """Extract JSON payload from request"""
    extractor = PayloadExtractorFactory.get_extractor('json')
    return extractor.extract()


def extract_image_payload() -> Union[Dict[str, Any], Any]:
    """Extract image payload from request"""
    extractor = PayloadExtractorFactory.get_extractor('image')
    return extractor.extract()