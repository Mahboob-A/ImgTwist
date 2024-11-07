#!/bin/bash 


set -o errexit 


set -o nounset 


python /home/imgtwist/app/manage.py makemigrations --no-input 
python /home/imgtwist/app/manage.py migrate --no-input 
python /home/imgtwist/app/manage.py collectstatic --no-input  --clear 

# For development in django server 
# django dev server port: 8000. In this case, change port on nginx/default.conf upstream block to 8000, and on .envs
# exec /home/imgtwist/app/manage.py runserver 0.0.0.0:${DJANGO_APP_PORT}

# Gunicorn app server 
# docker dev server port: 8009
exec /usr/local/bin/gunicorn Img_Twist.wsgi:application --bind 0.0.0.0:${DJANGO_APP_PORT} --chdir=/home/imgtwist/app

