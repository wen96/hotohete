release: python manage.py migrate --settings=hotohete.production
web: gunicorn hotohete.wsgi --logfile=-