#!/bin/bash

cd app

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python start_app.py

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@mail.ru', 'admin')" | python manage.py shell

gunicorn --bind 0.0.0.0:5858 NearestTrucksTestCase.wsgi
