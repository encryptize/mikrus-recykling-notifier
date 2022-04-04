FROM python:3.9-slim

WORKDIR /app

# Install required dependencies
RUN set -ex && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get update && \
    apt-get install -y cron && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install requirements
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/mikrus
RUN chmod 0644 /etc/cron.d/mikrus && touch /var/log/cron.log

# Install cron script
COPY . ./

ENTRYPOINT [ "/app/entrypoint.sh" ]