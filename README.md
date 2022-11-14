# email-address-mutation
The email mutation gateway is implemnted as a webservice using the [Django](https://docs.djangoproject.com/en/4.1/) framework. The web-client/mysite 
directory contails all the source code.

## Prerequisits
You need followings installed to run the email mutation gateway:
1. Python 3+.
1. Django. Here's the django installion process [instruction](https://www.djangoproject.com/download/)

## Running the server
To run the server, we will run following commands. All commands will be run under directroy `web-client/mysite`
1. `python3 manage.py runserver`. This will launch the email mutation gateway as a webserver.
1. `python manage.py migrate`. The models are stored in a Sqlite database, this command will create necessary tables into the DB.
