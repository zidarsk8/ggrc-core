#!/usr/bin/env bash

# DB_NAME is taken from settings.sh
DB_USER="some_username"
DB_PASSWORD="some_password"
DB_IP="555.111.111.111"
export GGRC_DATABASE_URI="mysql+mysqldb://${DB_USER}:${DB_PASSWORD}@${DB_IP}/${DB_NAME}?charset=utf8"
