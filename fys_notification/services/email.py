# Third party imports

from datetime import date, timedelta
import smtplib
import jinja2
import logging
import csv
from flask import abort
from base64 import b64encode

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Local Imports
from fys_notification.config import (
    FYS_SMPT_EMAIL, SMPT_SERVER, SMPT_PORT, FYS_SMPT_PASSWORD, FYS_ADMIN_EMAIL
)
from fys_notification.models.db_models import db

from fys_notification.models.email_data_models import EmailDataAnalytics


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # noqa: W1202

email_logger = logging.getLogger("EmailLog")


def send_internal_email(total_sent_emails):
    admin_req_parse = dict(
        user_name="Fyres Team",
        mail_to=FYS_ADMIN_EMAIL,
        subject="Analytics: Number of emails sent.",
        body=total_sent_emails,
        message_title="Email Sent  Analytics."

    )
    send_default_email(admin_req_parse, template='admin.html')


def send_client_email(req_parse):
    """
    Send client email
    :param req_parse:
    :return:
    """
    message_title = "Thanks you for contacting us."
    req_parse['message_title'] = message_title
    return send_default_email(req_parse)


def send_default_email(req_parse, template=None):

    message_title = req_parse['message_title']
    user_name = req_parse['user_name']
    # Create the root message and fill in the from, to, and subject headers
    tos = req_parse['mail_to'].split(',')

    msg_base = MIMEMultipart('related')
    msg_base['Subject'] = f"Subject: {req_parse['subject']}"
    msg_base['From'] = FYS_SMPT_EMAIL

    msg_base['To'] = ", ".join(tos)
    if req_parse.get('cc_mail_to'):
        cc_recipients = req_parse['cc_mail_to'].split(',')
        msg_base['Cc'] = ", ".join(cc_recipients)
        # Adding the CC Email Address.
        tos.extend(cc_recipients)
    if req_parse.get('bcc_mail_to'):
        bcc_recipients = req_parse['bcc_mail_to'].split(',')
        msg_base['Bcc'] = ", ".join(bcc_recipients)
        # Adding the BCC Email Address.
        tos.extend(bcc_recipients)

    msg_base.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msg_base.attach(msgAlternative)

    message = f"{req_parse['body']}"

    # Plain Text
    msgText = MIMEText('You are missing the email format and images.\n' + message)
    msgAlternative.attach(msgText)

    # Create HTML From Template
    # If regular email use default template.
    if template is None:
        html = render_template(
            'base_client_email.html', message=message, message_title=message_title, user_name=user_name)
    else:
        email_logger.info(f'template {template}')
        html = render_template(template, message=message, message_title=message_title, user_name=user_name)

    # HTML
    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText(html, 'html')
    msgAlternative.attach(msgText)

    return send_email(msg_base, tos)


def csv_file_read_send_email(csv_file_read):
    data = {}
    with open(csv_file_read) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                email_logger.info(f'Column names are {", ".join(csv_reader.fieldnames)}')
                line_count += 1
            email_logger.info(f'{row}')
            line_count += 1
            row['mail_to'] = row['mail_to'].replace('[', '').replace(']', '')
            row['cc_mail_to'] = row['cc_mail_to'].replace('[', '').replace(']', '')
            row['bcc_mail_to'] = row['bcc_mail_to'].replace('[', '').replace(']', '')
            # sending an email
            result = send_client_email(row)
            email_logger.info(f'Processed {line_count} lines.')
            data[row['user_name']] = result

        # data commit
        email_data = EmailDataAnalytics(email_sent_number=line_count)
        db.session.add(email_data)
        db.session.commit()
    return data


def send_email(msg_base, tos):
    """
    :param msg_base:
    :param tos:
    :return:
    """
    # Create a secure SSL context

    # Send the email (this example assumes SMTP authentication is required)
    smtp = smtplib.SMTP(SMPT_SERVER)
    smtp.connect(SMPT_SERVER, port=SMPT_PORT)
    # Secure the connection
    smtp.starttls()
    if not (FYS_SMPT_EMAIL and FYS_SMPT_PASSWORD):
        raise abort(400, "No login credentials provided")
    smtp.login(FYS_SMPT_EMAIL, FYS_SMPT_PASSWORD)
    # tos = req_parse['mail_to'].split(',')
    email_logger.info(tos)
    try:
        email_logger.info("Sending an email")
        smtp.sendmail(FYS_SMPT_EMAIL, tos, msg_base.as_string())
        smtp.quit()
    except Exception as error:
        return error
    return "Successfully Sent Email"


def render_template_dict(template, render_dict):
    """ renders a Jinja template into HTML """

    templateLoader = jinja2.FileSystemLoader(searchpath="fys_notification/static/templates")

    templateEnv = jinja2.Environment(loader=templateLoader)
    templ = templateEnv.get_template(template)
    return templ.render(render_dict)


def render_template(template, **kwargs):
    """ renders a Jinja template into HTML """

    templateLoader = jinja2.FileSystemLoader(searchpath="fys_notification/static/templates")

    templateEnv = jinja2.Environment(loader=templateLoader)
    templ = templateEnv.get_template(template)
    return templ.render(**kwargs)


def get_sent_email_analytics_data():

    day = date.today()
    next_day = day + timedelta(days=1)
    my_data = db.session.query(EmailDataAnalytics). \
        filter(EmailDataAnalytics.lastest_date_time >= day, EmailDataAnalytics.lastest_date_time < next_day).all()
    email_logger.info(f"data: {my_data}")
    sent_email_analytics = {'total_sent_emails': 0}
    for data in my_data:
        sent_email_analytics['total_sent_emails'] = sent_email_analytics.get('total_sent_emails') + data.email_sent_number
    send_internal_email(sent_email_analytics['total_sent_emails'])
