FROM python:3.9-alpine

WORKDIR /app

# Install requirements
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add crontab file in the cron directory
ADD . ./
RUN /usr/bin/crontab /app/crontab

VOLUME [ "/config" ]
ENTRYPOINT [ "/app/entrypoint.sh" ]
