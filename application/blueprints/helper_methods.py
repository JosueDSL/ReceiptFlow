# Description: Helper methods for handling exceptions and creating error responses.

# Import the necessary libraries
from flask import make_response, request, jsonify, current_app as app
from werkzeug.exceptions import HTTPException
from flask_jwt_extended.exceptions import NoAuthorizationError
import httpx


class ErrorHandler:
    """
    A class to handle exceptions and create error responses.
    """

    @staticmethod
    def make_error_response(message, status_code=400):
        """
        Create an error JSON response with a given error message and status code.

        Args:
            error_message (str): The error message to include in the response.
            status_code (int, optional): The HTTP status code for the response. Defaults to 400.

        Returns:
            Response: A Flask response object with the error message and status code.
        """
        response = jsonify({'error': message})
        response.status_code = status_code
        return make_response(response, status_code)
    
    @staticmethod
    def handle_general_exception(e):
        """
        Handle exceptions raised during a request, including HTTP errors.

        Args:
            e (Exception): The exception that was raised.

        Returns:
            Response: A Flask response object with the error message and a 500 status code.
        """

        # If the exception is an HTTPException, use its code and description
        if isinstance(e, HTTPException):
            response = {
                'error': e.name,
                'message': e.description
            }
            return jsonify(response), e.code
        else:
            # For non-HTTP exceptions, return a generic 500 error
            app.logger.error(str(e), exc_info=True)
            response = {
                "error": str(e),
                "message": "An error occurred."
            }
            return jsonify(response), 500


    @staticmethod
    def handle_exceptions(func):
        """
        Handle the errors that may arise during the execution of a function.

        Args:
            func (function): The function to execute.

        Returns:
            Any: The result of the function if no errors are raised.
            Response: A Flask response object with the error message and status code if an error is raised.
        """
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError as e:
                app.logger.error('ValueError: %s', e, exc_info=True)
                return ErrorHandler.make_error_response(str(e), 400)
            except TypeError as e:
                app.logger.error('TypeError: %s', e, exc_info=True)
                return ErrorHandler.make_error_response(str(e), 400)
            except AttributeError as e:
                app.logger.error('AttributeError: %s', e, exc_info=True)
                return ErrorHandler.make_error_response(str(e), 400)
            except KeyError as e:
                app.logger.error('KeyError: %s', e, exc_info=True)
                return ErrorHandler.make_error_response(str(e), 400)
            except HTTPError as e:
                app.logger.error('HTTPError: %s', e, exc_info=True)
                return ErrorHandler.make_error_response(str(e), e.response.status)
            except IOError as e:
                app.logger.error('IOError: %s', e, exc_info=True)
                return ErrorHandler.make_error_response(str(e), 400)
            except RuntimeError as e:
                app.logger.error('RuntimeError: %s', e, exc_info=True)
                return ErrorHandler.make_error_response(str(e), 400)
            except ZeroDivisionError as e:
                app.logger.error('ZeroDivisionError: %s', e, exc_info=True)
                return ErrorHandler.make_error_response(str(e), 400)
            except NoAuthorizationError as e:
                app.logger.error('NoAuthorizationError: %s Authorization required. Please log in first.' , e)
                return ErrorHandler.make_error_response(str('Authorization required. Please log in first.'), 401)
            except Exception as e:
                app.logger.error('An error occurred: %s', e, exc_info=True)
                return ErrorHandler.make_error_response(str(e), 500)
        return wrapper
        

    @staticmethod
    def get_json_payload() -> dict:
        """
        Extracts the JSON payload from the request safely.

        Returns:
            dict: The JSON payload if valid.
            Response: A 400 response if the JSON is invalid.
        """
        try:
            payload = request.get_json()
            if payload is None:
                raise ValueError("No JSON payload found")
            return payload

        except Exception as e:
            return make_response("Invalid or broken JSON request", 400)


# Custom errors for the application

class HTTPError(httpx.HTTPStatusError):
    """
    Custom error class to handle HTTP errors.
    """

    pass
