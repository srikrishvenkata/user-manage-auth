# user-manage-auth
## A Simple user management and authentication system in Python based on Flask Framework.
## This Application require MongoDB ( To persist User information ) and Redis ( To persist User Tokens )

# build directory -
To Build the user-manage-auth Image and spawn a container

# test directory -
To run scenario based tests

# Current directory -
## server.py - contains the Flask Application
## appconstants.py - contains the Application Constants
## mongo_db_connector.py  - contains the code to connect to mongodb, create, update, delete, read Users
## redis_cache.py  - contains the code to cache Client Token in Redis
## validate_param.py  - contains the code to validate input paramters
