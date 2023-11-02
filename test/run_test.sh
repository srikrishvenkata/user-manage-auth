#!/bin/bash
echo "Create user"
curl -s -X POST "http://localhost:5000/create/user?username=helloworld&email=helloworld@helloworld.com&password=12345678"
read
echo "List user"
curl -s -X GET "http://localhost:5000/list/user?email=helloworld@helloworld.com"
read
echo "Update user"
curl -s -X PUT "http://localhost:5000/update/user?username=helloworld&email=helloworld@helloworld.com&password=910111213"
read
echo "Login user"
curl -s -X POST "http://localhost:5000/login/user?email=helloworld@helloworld.com&password=910111213"
read
echo "List user"
curl -s -X GET "http://localhost:5000/list/user?email=helloworld@helloworld.com"
read

echo "Login user"
curl -s -X POST "http://localhost:5000/login/user?email=helloworld@helloworld.com&password=910111213"
read

echo "List user"
curl -s -X GET "http://localhost:5000/list/user?email=helloworld@helloworld.com"
read

echo "Is user logged in"
curl -s -X GET "http://localhost:5000/login/user?email=helloworld@helloworld.com"
read

echo "Log out  user"
curl -s -X GET "http://localhost:5000/logout/user?email=helloworld@helloworld.com"
read

echo "Log out  user"
curl -s -X GET "http://localhost:5000/logout/user?email=helloworld@helloworld.com"
read


echo "Delete user"
curl -s -X DELETE "http://localhost:5000/delete/user?username=helloworld&email=helloworld@helloworld.com"