FROM python:3.6

MAINTAINER Sreenivasulu Reddy <srinivasulur55.s@gmail.com>

COPY /fyres_notification /fyres_notification

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "-m", "fys_notification.runserver"]
