web: newrelic-admin run-program flask db upgrade; gunicorn main:app -b "$HOST:$PORT" -w 3
worker: newrelic-admin run-program celery worker --app=app.celery