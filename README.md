# Email-app in django (python)

- deployed application: https://email-app-sharma59.herokuapp.com/

# How to run the app

- clone the github repo

```
git clone https://github.com/nirbhay-design/django_email_app.git
```

- open email_system/settings.py file and do the following changes

```
debug = True
```

- now create a virtual env in python

```
python -m venv <your_env_name>
```

```
source <your_env_name>/Scripts/activate
```

- now install the dependencies using

```
pip install -r requirements.txt
```

- now run the following command

```
python manage.py runserver
```

# How to deploy the application

- install gunicorn, whitenoise
- make Procfile
- make requirements.txt
- debug = False
- change allowed_hosts
- add static path for django (STATIC_ROOT)
- add whitenoise middleware just below the security middleware

# Deploy procedure

- heroku login
- heroku create
- git init
- git add .
- git commit -m "msg"
- git push heroku master