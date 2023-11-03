#!/bin/bash
cd ..
echo "Docker Image Build Started"
docker build  --no-cache --tag user-mgmt-auth -f build/Dockerfile .
echo "Docker Image Build completed"
echo "Spawing a Container"
docker run -d --name user-mgmt-auth-container -p 5000:5000 user-mgmt-auth