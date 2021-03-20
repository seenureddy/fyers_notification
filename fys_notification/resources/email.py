# Third party
import os
import logging
import werkzeug
from flask import request, abort
from flask_restful import Resource, reqparse, fields, marshal_with

# Local import
from fys_notification.services.email import send_client_email, csv_file_read_send_email, get_sent_email_analytics_data
from fys_notification.utils import allowed_file

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # noqa: W1202
resource_file_logger = logging.getLogger("resource_file_log")


class EmailResource(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.req_parse.add_argument(
            "user_name", type='str', required=True, help='No user_name provided', location='json'
        )
        self.req_parse.add_argument('subject', type='str', required=True, help='No subject provided', location='json')
        self.req_parse.add_argument("mail_to", type='str', required=True, help='No subject provided')
        self.req_parse.add_argument("cc_mail_to", type='str', required=True, help='No subject provided')
        self.req_parse.add_argument("bcc_mail_to", type='str', required=True, help='No subject provided')
        self.req_parse.add_argument('body', type='str', required=True, help='No body/message provided', location='json')

    def post(self):
        # request.get_json(force=True)
        # req_parse = self.req_parse.parse_args()
        req_parse = request.get_json(force=True)
        if not req_parse.get('user_name'):
            raise abort(400, "No user_name provided")
        if not req_parse['subject']:
            raise abort(400, "No subject provided")
        if not req_parse['mail_to']:
            raise abort(400, "No mail_to provided")
        if not req_parse['cc_mail_to']:
            raise abort(400, "No cc_mail_to provided")
        if not req_parse['bcc_mail_to']:
            raise abort(400, "No bcc_mail_to provided")
        if not req_parse['body']:
            raise abort(400, "No body provided")

        # Client Email
        resource_file_logger.info(f"request-data: {req_parse}")
        status = send_client_email(req_parse)
        return {'status': 'Success', 'data': status}, 200


class CSVEmailResource(Resource):
    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.req_parse.add_argument(
            'csv_file', type=werkzeug.datastructures.FileStorage, required=True, help='No subject provided',
            location='files')

    def post(self):
        req_parse = request.get_json(force=True)
        resource_file_logger.info(f"request-data: {req_parse}")
        csv_file_name = req_parse['csv_file']
        if csv_file_name == '':
            raise abort(400, "No file found")
        if not (csv_file_name and allowed_file(csv_file_name)):
            raise abort(400, "Only filename.csv file format is accepted")
        if not os.path.isfile(csv_file_name):
            raise abort(404, f"No {csv_file_name} file found.")
        resource_file_logger.info(f"file_name {csv_file_name}, format_allowed: {allowed_file(csv_file_name)}")
        # Client Email
        status = csv_file_read_send_email(csv_file_name)
        return {'status': 'Success', 'data': status}, 200


class SendAdminEmailResource(Resource):
    def get(self):
        get_sent_email_analytics_data()
        return {'status': 'Success'}, 200