"""
    This is a Python module that provides a CRUD REST API for managing user objects.
    :return: The code is returning a Flask app that provides a CRUD REST API for User objects.
    The API includes endpoints for listing users, creating users, logging in users,
    updating users, and deleting users. Each endpoint returns a JSON response with a message and
    a status code.
"""

import hashlib
import os
import sys
import logging
from flask import Flask, jsonify, request
import redis_cache
import mongo_db_connector
import validate_param
import appconstants

# creating a Flask app
APP = Flask(__name__)


@APP.route('/list/user', methods=['GET'])
def list_user():
    """
    The function "list_user" takes an email parameter, validates it, and returns a JSON response
    containing user profile information if the email is valid.
    :return: a JSON response and a status code. The JSON response contains the user profile
    information if the email parameter is valid and the email is valid. If the email parameter is
    missing or the email value is not valid, an error message is returned. The status code
    indicates the success or failure of the request.
    """
    email = request.args.get("email")
    response = {}
    status_code = 200
    if validate_param.is_parameter_value_valid(email):
        if validate_param.is_parameter_value_valid_email(email):
            response = mongo_db_connector.list_user(email)
            if "exception" in response.keys():
                status_code = 500
        else:
            response = appconstants.BAD_EMAIL_VALUE
            status_code = 400
    else:
        status_code = 400
        response = appconstants.PARAM_EMAIL_ABSENT
    return (jsonify(response), status_code)


@APP.route('/create/user', methods=['POST'])
def create_user():
    """
    The `create_user` function is a Flask route that creates a new user by validating the provided
    username, email, and password parameters and then adding the user to a MongoDB database.
    :return: The function `create_user()` returns a JSON response and a status code. The JSON
    response contains the response data, which can be either a success message or an error message.
    The status code indicates the success or failure of the request.
    """
    username = request.args.get("username")
    email = request.args.get("email")
    password = request.args.get("password")
    response = {}
    status_code = 200
    if (validate_param.is_parameter_value_valid(username)
            and validate_param.is_parameter_value_valid(email)
            and validate_param.is_parameter_value_valid(password)):
        if validate_param.is_parameter_value_valid_email(email):
            if validate_param.is_parameter_value_valid_password(password):
                response = (mongo_db_connector.add_user(
                    username, email, password))
                if "exception" in response.keys():
                    status_code = 500
            else:
                response = appconstants.BAD_PASSWORD_VALUE
        else:
            response = appconstants.BAD_EMAIL_VALUE
            status_code = 400
    else:
        response = appconstants.MANDATORY_PARAMETER_U_E_P_MISSING
        status_code = 400
    return (jsonify(response), status_code)


@APP.route('/login/user', methods=['POST'])
def login_user():
    """
    The function `login_user()` is a route handler for the `/login/user` endpoint that handles user
    login by validating the email and password parameters, encrypting the password, and calling the
    `login_user()` function from the `mongo_db_connector` module.
    :return: a JSON response and a status code. The JSON response contains the response data, which
    could be a success message or an error message. The status code indicates the status of the
    response, such as 200 for a successful request or 400 for a bad request.
    """
    email = request.args.get("email")
    password = request.args.get("password")
    response = {}
    status_code = 200

    if (validate_param.is_parameter_value_valid(email)
            and validate_param.is_parameter_value_valid(password)):
        if validate_param.is_parameter_value_valid_email(email):
            encrypted_password = hashlib.md5(
                password.encode('utf-8')).hexdigest()
            response = (mongo_db_connector.login_user(
                email, encrypted_password))
            if "exception" in response.keys():
                status_code = 500
        else:
            response = appconstants.BAD_EMAIL_VALUE
            status_code = 400
    else:
        response = appconstants.MANDATORY_PARAMETER_E_P_MISSING
        status_code = 400
    return (jsonify(response), status_code)


@APP.route('/login/user', methods=['GET'])
def check_logged_in():
    """
    The function `check_logged_in` checks if a user with a given email is logged in and
    returns a response message indicating their login status.
    :return: a tuple containing a JSON response and a status code. The JSON response contains a
    message indicating whether the provided email is logged in or not. The status code indicates
    the success or failure of the request.
    """
    email = request.args.get("email")
    response = {}
    status_code = 200

    if validate_param.is_parameter_value_valid(email):
        if validate_param.is_parameter_value_valid_email(email):
            if redis_cache.is_client_token_persists(email):
                response = ({"message": email + " is logged in"})
            else:
                response = ({"message": email + " is not logged in"})
        else:
            response =  appconstants.BAD_EMAIL_VALUE
            status_code = 400
    else:
        response =  appconstants.PARAM_EMAIL_ABSENT
        status_code = 400
    return (jsonify(response), status_code)


@APP.route('/logout/user', methods=['GET'])
def log_out():
    """
    The function `log_out()` logs out a user based on their email and returns a response message.
    :return: a tuple containing a JSON response and a status code. The JSON response contains a
    message indicating whether the user was successfully logged out or not. The status code
    indicates the success or failure of the request.
    """
    email = request.args.get("email")
    response = {}
    status_code = 200

    if validate_param.is_parameter_value_valid(email):
        if validate_param.is_parameter_value_valid_email(email):
            if redis_cache.is_client_token_persists(email):
                if redis_cache.is_remove_client_token(email):
                    response = ({"message": email + " logged out"})
                else:
                    response = ({"message": email + " failed to logged out"})
            else:
                response = ({"message": email + " not logged in. Hence cannot log out"})
        else:
            response = appconstants.BAD_EMAIL_VALUE
            status_code = 400
    else:
        response = appconstants.PARAM_EMAIL_ABSENT
        status_code = 400
    return (jsonify(response), status_code)


@APP.route('/update/user', methods=['PUT'])
def update_user():
    """
    The function `update_user()` updates a user's information in a database, including their
    username, email, and password, and returns a response with a status code.
    :return: a JSON response and a status code. The JSON response contains the updated user
    information or an error message, depending on the validation of the parameters. The
    status code indicates the success or failure of the request.
    """
    username = request.args.get("username")
    email = request.args.get("email")
    password = request.args.get("password")
    response = {}
    status_code = 200
    if (validate_param.is_parameter_value_valid(username) and validate_param.is_parameter_value_valid(email)
            and validate_param.is_parameter_value_valid(password)):
        if validate_param.is_parameter_value_valid_email(email):
            if validate_param.is_parameter_value_valid_password(password):
                encrypted_password = hashlib.md5(
                    password.encode('utf-8')).hexdigest()
                response = (mongo_db_connector.update_user(
                    username, email, encrypted_password))
                if "exception" in response.keys():
                    status_code = 500
            else:
                response = appconstants.BAD_PASSWORD_VALUE
                status_code = 400
        else:
            response = appconstants.BAD_EMAIL_VALUE
            status_code = 400
    else:
        response = appconstants.MANDATORY_PARAMETER_U_E_P_MISSING
        status_code = 400
    return (jsonify(response), status_code)


@APP.route('/delete/user', methods=['DELETE'])
def delete_user():
    """
    The function `delete_user()` is a route in a Python Flask application that deletes a user
    from a database based on their username and email.
    :return: a JSON response and a status code. The JSON response contains the response message
    and the status code indicates the success or failure of the request.
    """
    username = request.args.get("username")
    email = request.args.get("email")
    response = {}
    status_code = 200
    if (validate_param.is_parameter_value_valid(username)
            and validate_param.is_parameter_value_valid(email)):
        if validate_param.is_parameter_value_valid_email(email):
            response = (mongo_db_connector.delete_user(username, email))
            if "exception" in response.keys():
                status_code = 500
        else:
            response = appconstants.BAD_EMAIL_VALUE
            status_code = 400
    else:
        response = appconstants.MANDATORY_PARAMETER_E_U_MISSING
        status_code = 400
    return (jsonify(response), status_code)


if __name__ == '__main__':
    if ("MONGODB_HOST" not in os.environ or "MONGODB_PORT" not in os.environ or
            "REDIS_HOST" not in os.environ or "REDIS_PORT" not in os.environ):
        logging.error(
            "One of the Mandatory Environment Variables ( MONGODB_HOST, MONGODB_PORT, REDIS_HOST, REDIS_PORT  ) are not set.")
        sys.exit()
    else:
        logging.info("App Env. MONGODB_HOST %s, MONGODB_PORT %d, REDIS_HOST %s, REDIS_PORT %d ",
                    os.environ["MONGODB_HOST"], os.environ["MONGODB_PORT"], os.environ["REDIS_HOST"], os.environ["REDIS_PORT"])
        APP.run(debug=True)
