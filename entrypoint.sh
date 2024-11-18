#!/bin/sh

set -e

python studentManagementSystem/manage.py makemigrations --noinput
python studentManagementSystem/manage.py migrate --noinput

exec "$@"
