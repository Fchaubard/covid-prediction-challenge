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
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
#RUN git clone https://github.com/CSSEGISandData/COVID-19.git /app/data

FROM build-stage1 as build-stage2

# Copy local code to the container image.
#COPY crontab /etc/cron.d/crontab
#RUN chmod 0644 /etc/cron.d/crontab
#RUN service cron start


# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.

CMD exec gunicorn --bind :80 --workers 1 --threads 8 app:app

#CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
