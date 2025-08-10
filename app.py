# Import the create_app function from the application package
from application import create_app
from application.blueprints.helper_methods import ErrorHandler


# Create an instance of the Flask application
app = create_app()


# Setup error handler for the application
@app.errorhandler(Exception)
def handle_error(e):
    return ErrorHandler.handle_general_exception(e)

# Health check route
@app.route('/health')
def health():
    return 'OK', 200


# Run the application
if __name__ == '__main__':
     app.run()
