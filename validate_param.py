"""
    The module provides functions for validating parameter values, including email addresses and
    passwords.
"""
import re

def is_parameter_value_valid(parameter):
    """
    The function checks if a parameter value is not None and has a length greater than 0.
    :param parameter: The parameter is a variable that can hold any value. It is used to 
    check if the value is valid or not
    :return: a boolean value. It returns True if the parameter is not None and has a length
    greater than 0, indicating that the parameter value is valid. It returns False otherwise.
    """
    return parameter is not None and len(parameter) > 0

def is_parameter_value_valid_email(parameter):
    """
    The function is_parameter_value_valid_email checks if a given parameter is a valid
    email address.
    :param parameter: The parameter is a string that represents an email address
    :return: the result of the regular expression match. If the parameter value is a valid
    email address, the match will be successful and a match object will be returned. If the
    parameter value is not a valid email address, the match will be unsuccessful and None
    will be returned.
    """
    return re.match(r"[^@]+@[^@]+\.[^@]+", parameter)

def is_parameter_value_valid_password(parameter):
    """
    The function is_parameter_value_valid_password checks if a given parameter is a
    valid password, which should contain at least 8 characters and can include
    uppercase letters, lowercase letters, numbers, and special characters.
    :param parameter: The parameter in the function `is_parameter_value_valid_password`
    is a string that represents a password
    :return: the result of the re.fullmatch() method, which is a match object if the
    parameter value is a valid password, or None if it is not.
    """
    return re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', parameter)
