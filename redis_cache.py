"""
    The module provides functions for persisting, removing of Client Token
"""
import os
import logging
import redis

REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = int(os.environ["REDIS_PORT"])
REDIS = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def persist_client_token(email, token):
    """
    The function persist_client_token stores a client token in Redis using the client's email as the
    key.

    :param email: The email parameter is a string that represents the email address of the client
    :param token: The token is a unique identifier or authentication token that is associated with a
    specific client or user. It is used to verify the identity of the client when making requests or
    accessing certain resources
    """
    try:
        REDIS.set(email, token)
    except redis.exceptions.ConnectionError as ex:
        logging.error('Exception at persist_client_token %s', str(ex))


def is_remove_client_token(email):
    """
    The function `is_remove_client_token` checks if a client token is removed from a Redis database
    based on the provided email.

    :param email: The email parameter is a string that represents the email address of a client
    :return: a boolean value. It returns True if the status of the REDIS delete operation is 1,
    indicating that the client token was successfully removed. It returns False otherwise.
    """
    try:
        status = REDIS.delete(email)
        return status == 1
    except redis.exceptions.ConnectionError as ex:
        logging.error('Exception at is_remove_client_token %s', str(ex))
        return 0


def is_client_token_persists(email):
    """
    The function checks if a client token persists in Redis for a given email.

    :param email: The email parameter is a string that represents the email address of a client
    :return: a boolean value. It returns True if the token associated with the given email exists in the
    REDIS database, and False otherwise.
    """
    try:
        token = REDIS.get(email)
        return token is not None
    except redis.exceptions.ConnectionError as ex:
        logging.error('Exception at is_client_token_persists %s', str(ex))
        return False
