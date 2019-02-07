#!/usr/bin/env bash

# checking if there are any model's changements and creating migrations

python3 manage.py makemigrations

# migrate the changements to the database

python3 manage.py migrate

# running web server

python3 manage.py runserver 192.168.1.118:8000