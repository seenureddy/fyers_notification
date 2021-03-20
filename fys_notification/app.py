# Third party imports

from flask import Blueprint
from flask_restful import Api

# Local imports
from fys_notification.resources.swagger import StaticResource
from fys_notification.resources.email import (
    EmailResource, CSVEmailResource, SendAdminEmailResource
)


# Add Blueprint to flask App

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(StaticResource, '/swagger')
api.add_resource(EmailResource, '/fys/email')
api.add_resource(CSVEmailResource, '/fys/csv_upload')
api.add_resource(SendAdminEmailResource, '/fys/admin')
