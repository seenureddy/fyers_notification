# Third party
import os
import logging
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

# Local imports

from fys_notification.app import api_bp
from fys_notification.models.db_models import db
# from fys_notification.config import Config


logging.basicConfig(
    filename='fyers_log.log', level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)


SWAGGER_URL = '/docs'
API_URL = '/swagger'

swaggerrui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "FYS Notification REST API Service"
    },
)

# Media files

UPLOAD_FOLDER = os.getcwd() + '/fys_notification/media'


def create_app():
    """
    Create flask app with all blueprints and configurations options
    :return:
    """

    app = Flask(__name__)

    app.register_blueprint(api_bp)
    app.register_blueprint(swaggerrui_blueprint, url_prefix=SWAGGER_URL)

    # DB Configuration
    app.config.from_object('fys_notification.config')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # with app.app_context():
    #     db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", debug=True, port=5000)
