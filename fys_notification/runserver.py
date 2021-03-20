# Third party
import os
import logging
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

# Local imports

from fys_notification.appi import api_bp
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

flask_app = Flask(__name__)


def create_app():
    """
    Create flask app with all blueprints and configurations options
    :return:
    """

    flask_app.register_blueprint(api_bp)
    flask_app.register_blueprint(swaggerrui_blueprint, url_prefix=SWAGGER_URL)

    # DB Configuration
    flask_app.config.from_object('fys_notification.config')
    flask_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    db.init_app(flask_app)

    return flask_app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", debug=True, port=5000)