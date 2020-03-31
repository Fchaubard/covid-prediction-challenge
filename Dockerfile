# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.7-slim AS build-stage1

# Install production dependencies.
RUN pip install Flask gunicorn
RUN pip install flask-bootstrap
RUN pip install pandas
RUN apt-get update
RUN apt-get -y install git
RUN apt-get -y install cron
RUN apt-get -y install curl

# Downloading gcloud package
RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz

# Installing the package
RUN mkdir -p /usr/local/gcloud \
  && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
  && /usr/local/gcloud/google-cloud-sdk/install.sh
RUN pip install gsutil






FROM build-stage1 as build-stage2

ENV APP_HOME /app
WORKDIR $APP_HOME
ADD . ./

RUN git clone https://github.com/CSSEGISandData/COVID-19.git $APP_HOME/data


# Setup the cron
ADD crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
#RUN service cron start
RUN touch /var/log/cron.log
RUN crontab /etc/cron.d/crontab

CMD cron && tail -f /var/log/cron.log

# Run the cron on start
CMD bash $APP_HOME/task.sh
CMD exec gunicorn --bind :80 --workers 1 --threads 8 app:app

