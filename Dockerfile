# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.7-slim AS build-stage1

RUN apt-get --no-install-recommends update \
  && apt-get --no-install-recommends -y install git cron curl 

# Downloading gcloud package
RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz

# Installing the package
RUN mkdir -p /usr/local/gcloud \
  && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
  && /usr/local/gcloud/google-cloud-sdk/install.sh

RUN rm /tmp/google-cloud-sdk.tar.gz 

# Install production dependencies.
RUN pip install Flask gunicorn flask-bootstrap pandas gsutil werkzeug

FROM build-stage1 as build-stage2

ENV APP_HOME /app
WORKDIR $APP_HOME
ADD . ./

#RUN git clone https://github.com/CSSEGISandData/COVID-19.git $APP_HOME/data

# Setup the cron... this doesnt work on GCE 
#   moving to Google Cron -> covidepredictions.com/update_leaderboard
#COPY crontab /etc/cron.d/crontab

#CMD chmod 0644 /etc/cron.d/crontab \
#  && touch /var/log/cron.log \
#  && crontab /etc/cron.d/crontab \
#  && cron \
#  && tail -f /var/log/cron.log

#CMD ["/bin/bash","/app/task.sh"]
#CMD bash /app/task.sh


# Run the webserver
CMD cd $APP_HOME && \
  exec gunicorn --bind :80 --workers 1 --threads 8 app:app

