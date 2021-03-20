# Third party import
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

# Local imports
from fys_notification.models.db_models import db


class EmailDataAnalytics(db.Model):
    __tablename__ = 'email_data_analytics'

    id = db.Column(db.Integer, primary_key=True)
    email_sent_number = db.Column(db.Integer)
    lastest_date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, email_sent_number):
        self.email_sent_number = email_sent_number

    def __repr__(self):
        return '<id {}>'.format(self.id)
