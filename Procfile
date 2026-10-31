web: gunicorn nestova.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --threads 2 --worker-class gthread --timeout 120 --max-requests 1000 --max-requests-jitter 100
worker: celery -A nestova worker --loglevel=info --pool=solo
beat: celery -A nestova beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler