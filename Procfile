web: flask db upgrade; gunicorn main:app -b "$HOST:$PORT" -w 3
worker: celery worker --app=app.celery