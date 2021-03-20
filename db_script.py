"""
Doc: https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
"""
from fys_notification.run import create_app
from fys_notification.models.db_models import db
db.create_all(app=create_app())
