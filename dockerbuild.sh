#!/bin/bash

docker-compose rm -vf
docker-compose build --no-cache
docker-compose up 


