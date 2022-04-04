#!/bin/sh

echo TZ=$TZ >> /etc/environment
echo BOT_TOKEN=$BOT_TOKEN >> /etc/environment
echo CHANNEL_ID=$CHANNEL_ID >> /etc/environment

cron && tail -f /var/log/cron.log