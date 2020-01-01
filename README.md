# rmndr - task reminder app

Demo: [rmndr-py.herokuapp.com](https://rmndr-py.herokuapp.com/)

Version: 1.0

A simple app to send email reminders of your scheduled tasks.

## Getting Started

Python 3 with Flask framework

Database: PostgreSQL

Celery broker: Redis (for running asynchronous tasks)

Mail server: Gmail (for sending email reminders)

## Installing

1- See [requirements.txt](requirements.txt) file for installing prerequisite Python packages or run the command below:

```
pip install -r requirements.txt
```

2- Configure SQL database, Gmail server, and Celery broker URL in [config.py](config.py) file.

3- Then run the Flask-Migrate commands below to initialize and setup database:

```
flask db init
```

```
flask db migrate
```

```
flask db upgrade
```

4- Finally, run the web server:

```
flask run
```

## Creator

[Tuan Hoang](http://hoanganhtuan.name/)