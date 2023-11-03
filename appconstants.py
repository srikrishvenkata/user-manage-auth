# The code block you provided defines a set of variables that store different messages or status
# values related to an application. These variables are used to provide specific messages or status
# updates to the user or developer based on different scenarios or conditions in the application. For
# example, the variable `BAD_EMAIL_VALUE` stores a message indicating that the value provided for the
# email parameter is bad, while the variable `USER_ADDED` stores a status indicating that a user has
# been successfully added. These variables can be used throughout the application to provide
# consistent and meaningful messages or status updates.
# Application Message Properties

BAD_EMAIL_VALUE = {"message": "bad value to the parameter email"}
BAD_PASSWORD_VALUE = {"message": "bad value to the parameter password"}
USER_ADDED = {"status": "user added successfully"}
EMAIL_ALREADY_EXISTS = {"status": "please try with new email address"}
MONGODB_CONNECTIVITY_ISSUE = {"exception": "Some issue with MongoDB Connectivity"}
USER_DELETED = {"status": "user deleted successfully"}
USER_DELETE_FAILED =  {"status": "user delete failed"}
USER_UPDATE = {"status": "user profile updated successfully"}
USER_UPDATE_FAILED = {"status": "user profile update failed"}
USER_NOT_FOUND =  {"user": "user not found"}
USER_FIRST_LOGIN = "user has not logged in"
USER_LOGIN_FAILED = {"status": "user login failed"}
USER_LOGIN_SUCCESS = {"status": "user login successful"}
PARAM_EMAIL_ABSENT = {"message": "parameter email missing"}
MANDATORY_PARAMETER_U_E_P_MISSING = {"message": "one of the mandatory parameter is missing ( username, email, password )"}
MANDATORY_PARAMETER_E_P_MISSING = {"message": "one of the mandatory parameter is missing ( email, password )"}
MANDATORY_PARAMETER_E_U_MISSING = {"message": "one of the mandatory parameter is missing ( email, username )"}