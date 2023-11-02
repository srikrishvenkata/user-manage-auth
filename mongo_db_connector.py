"""
    The above code provides functions for adding, deleting, updating, listing, and logging in users
    in a MongoDB database.
    
    :param username: The username of the user you want to add, delete, or update in the MongoDB
    document
    :param email: The email parameter is used to identify a user in the MongoDB document. It is
    used in functions like add_user, delete_user, update_user, list_user, and login_user to
    perform operations on the user with the specified email
    :param password: The `password` parameter is the password of the user that needs to be added,
    deleted, or updated in the MongoDB document. It is used to authenticate the user and perform
    the necessary operations on the user's data
    :return: The functions in this module return different responses based on the operation being
    performed:
"""
import os
import hashlib
import uuid
import time
from datetime import datetime
import logging
import pymongo
import redis_cache

CONNECTION_STRING = "mongodb://%s:%s" % (
    os.environ["MONGODB_HOST"], os.environ["MONGODB_PORT"])
DBCLIENT = pymongo.MongoClient(
    CONNECTION_STRING, serverSelectionTimeoutMS=5000)
# Database
USER_DB = DBCLIENT["userdatabase"]

# Collection
USERS = USER_DB["users"]
USERLOGIN = USER_DB["userlogin"]


def add_user(username, email, password):
    """
    The function `add_user` adds a user to a MongoDB document, encrypting their password using MD5.

    :param username: The username parameter is a string that represents the username of the user
    you want to add to the MongoDB document
    :param email: The email parameter is the email address of the user that you want to add to the
    MongoDB document
    :param password: The password parameter is the user's password that needs to be added to the
    MongoDB document
    :return: a dictionary with a "status" key. The value of the "status" key depends on whether the
    user was successfully added or not. If the user was added, the value will be "user added". If 
    the user was not added because the email already exists in the database, the value will be 
    "please try with new email address".
    """
    response = {}

    try:
        cursor = USERS.find_one({"email": email})
        encrypted_password = hashlib.md5(password.encode('utf-8')).hexdigest()

        entry = {"username": username, "email": email, "password": encrypted_password}
        if cursor is None:
            USERS.insert_one(entry)
            response = {"status": "user added"}
        else:
            response = {"status": "please try with new email address"}
    except pymongo.errors.ConnectionFailure as ex:
        response = {"exception": "Some issue with MongoDB Connectivity"}
        logging.error('Exception at add_user %s', str(ex))
    return response


def delete_user(username, email):
    """
    The function `delete_user` deletes a user from a MongoDB document based on their username
    and email, and returns a response indicating whether the deletion was successful or not.

    :param username: The username parameter is the username of the user you want to delete from the
    MongoDB document
    :param email: The email parameter is the email address of the user you want to delete from the
    MongoDB document
    :return: a response dictionary with the status of the user deletion. The status can be either
    "user deleted successfully" or "user delete failed".
    """
    query1 = {"email": email}
    query2 = dict(query1)
    query2["username"] = username
    response = {}
    try:
        delete_cursor = USERS.delete_one(query2)
        if delete_cursor.deleted_count == 1:
            response = {"status": "user deleted successfully"}
            USERLOGIN.delete_one(query1)
        else:
            response = {"status": "user delete failed"}
    except pymongo.errors.ConnectionFailure as ex:
        response = {"exception": "Some issue with MongoDB Connectivity"}
        logging.error('Exception at delete_user %s', str(ex))
    return response


def update_user(username, email, encrypted_password):
    """
    The function updates a user's password in a MongoDB document and returns a response indicating
    whether the update was successful or not.

    :param username: The username is the unique identifier for the user in the MongoDB document.
    It is used to locate the specific user that needs to be updated
    :param email: The email parameter is the new email address that you want to update for the user
    :param encrypted_password: The encrypted password is the password that has been transformed
    using a cryptographic algorithm to make it more secure. It is typically stored in a database or
    used for authentication purposes
    :return: a dictionary response with a "status" key indicating whether the update was successful
    or not.
    """
    query_parameters = {"username": username, "email": email}
    new_value = {"$set": {"password": encrypted_password}}
    response = {}
    try:
        update_cursor = USERS.update_one(query_parameters, new_value)
        if update_cursor.modified_count == 1:
            response = {"status": "Update success"}
        else:
            response = {"status": "Update failed"}
    except pymongo.errors.ConnectionFailure as ex:
        response = {"exception": "Some issue with MongoDB Connectivity"}
        logging.error('Exception at update_user %s', str(ex))
    return response


def list_user(email):
    """
    The function "list_user" retrieves user information from a MongoDB document and returns it in a
    formatted response.

    :param email: The email parameter is a string that represents the email address of the user you
    want to retrieve information for
    :return: a dictionary containing information about the user. If the user is not found in the
    database, the dictionary will have a key "user" with the value "Not_Found". If the user is
    found, the dictionary will have keys "username", "email", and "lastlogin". The value of
    "lastlogin" will be a list of readable dates representing the user's last login
    """
    response = {}
    try:
        cursor = USERS.find_one({"email": email})
        if cursor is None:
            response = {"user": "Not_Found"}
        else:
            login_entry_cursor = USERLOGIN.find_one({"email": email})
            if login_entry_cursor is None:
                response = {
                    "username": cursor["username"], "email": cursor["email"]}
                response["lastlogin"] = "user has not logged in"
            else:
                readable_date_array = []
                for login in login_entry_cursor["lastlogin"]:
                    readable_date_array.append(datetime.fromtimestamp(login))
                response = {"username": cursor["username"], "email": cursor["email"],
                            "lastlogin": readable_date_array}
    except pymongo.errors.ConnectionFailure as ex:
        response = {"exception": "Some issue with MongoDB Connectivity"}
        logging.error('Exception at list_user %s', str(ex))
    return response


def login_user(email, encrypted_password):
    """
    The function `login_user` checks if a user with the given email and encrypted password exists
    in the MongoDB document, and if so, generates a valid token and updates the user's login
    history.

    :param email: The email parameter is the email address of the user trying to log in
    :param encrypted_password: The encrypted password is a string that represents the user's 
    password after it has been encrypted or hashed for security purposes
    :return: a dictionary containing the status of the user login and a token. The status can be
    either "user login failed" or "user login success", depending on whether the user with the
    given email and encrypted password exists in the database. If the login is successful, a token
    is also included in the response.
    """
    response = {}
    try:
        cursor = USERS.find_one(
            {"email": email, "password": encrypted_password})
        if cursor is None:
            response = {"status": "user login failed"}
        else:
            token = uuid.uuid4().hex[:6].upper()
            login_entry_cursor = USERLOGIN.find_one({"email": email})
            if login_entry_cursor is None:
                login_entry_record = {
                    "email": email, "lastlogin": [time.time()]}
                USERLOGIN.insert_one(login_entry_record)
            else:
                lastlogin = login_entry_cursor["lastlogin"]
                lastlogin.append(time.time())
                # Update Login History
                query = {"email": email}
                new_value = {"$set": {"lastlogin": lastlogin}}
                USERLOGIN.update_one(query, new_value)
            redis_cache.persist_client_token(email, token)
            response = {"status": "user login success", "token": token}
    except pymongo.errors.ConnectionFailure as ex:
        response = {"exception": "Some issue with MongoDB Connectivity"}
        logging.error('Exception at login_user %s', str(ex))
    return response
