# Fyers_Email_Notification

## Database Setup
Using postgres for my local setup. 
* check config.py file to change db configurations.
* create the database `fyn_db`

change these configurations:

```
POSTGRES_USER=postgres
POSTGRES_URL=localhost
POSTGRES_DB=fys_db
```
or 

For using sqlite database

* change db configuration in config.py file
```SQLALCHEMY_DATABASE_URI: 'sqlite:///db.sqlite'```

doc: https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/

Note: change directory to `fyers_notificaiton`. Run db_script.py file to db context

```python db_script.py```

## Local setup
* Create .env file to add environment variables (`ENV VARIABLES`)
* Create the virtualenv and activate the virtualenv
* Install the requirements `pip install -r requirements.txt`
* Environment Variables
  > LIFE_CYCLE: <configurations for prod, heroku, local>
* Flask run command
  > python -m fys_notification.runserver
* For logs: `fyers_notification/fyers_log.log`
* Docker build `docker build . -t fyn`
* Docker run command `docker run fyn`
* Change the `paths` in logstash.conf and filebeat.yml to local machine full paths
  `/pp/fyers_notification/*_log.log` to `<full_path/pp/fyers_notification/*_log.log`
* Gunicorn run command
```gunicorn 'fys_notification.runserver:app' --preload -b 0.0.0.0:5000 --log-file -```
  
* To get sent email information(`http://0.0.0.0:5000/fys/admin`)

```
from fys_notification.services.email import get_sent_email_analytics_data
```

#### ENV VARIABLES
- LIFE_CYCLE
- POSTGRES_USER
- POSTGRES_URL
- POSTGRES_DB  
- FYS_SMPT_PASSWORD
- FYS_SMPT_EMAIL
- FYS_ADMIN_EMAIL
* Change the default_email is `srinivasulur55.s@gmail.com`

### API Endpoints:
* http://0.0.0.0:5000/fys/csv_upload
* http://0.0.0.0:5000/fys/email
* http://0.0.0.0:5000/fys/admin