# Import the create_app function from the application package
from application import create_app
from application.services.error_service import ErrorResponseHandler


# Create an instance of the Flask application
app = create_app()


# Global error handlers for uncaught exceptions
@app.errorhandler(404)
def handle_not_found(e):
    """Handle 404 Not Found errors"""
    return ErrorResponseHandler.make_error_response(
        message="The requested resource was not found",
        status_code=404,
        error_code="NOT_FOUND"
    )


@app.errorhandler(405)
def handle_method_not_allowed(e):
    """Handle 405 Method Not Allowed errors"""
    return ErrorResponseHandler.make_error_response(
        message="Method not allowed for this endpoint",
        status_code=405,
        error_code="METHOD_NOT_ALLOWED"
    )


@app.errorhandler(500)
def handle_internal_error(e):
    """Handle 500 Internal Server Error"""
    return ErrorResponseHandler.handle_general_exception(e)


# Catch-all error handler for any uncaught exceptions
@app.errorhandler(Exception)
def handle_general_exception(e):
    """Global exception handler for any uncaught exceptions"""
    return ErrorResponseHandler.handle_general_exception(e)


# Health check route
@app.route('/health')
def health():
    """Health check endpoint for load balancers and monitoring"""
    return {'status': 'healthy', 'service': 'ReceiptFlow'}, 200


# Run the application
if __name__ == '__main__':
    app.run(
        host=app.config.get('HOST'),
        port=app.config.get('PORT'),
        debug=app.config.get('DEBUG', False)
    )