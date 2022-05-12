#!/bin/sh

echo TZ=$TZ >> /etc/environment
echo TG_TOKEN=$TG_TOKEN >> /etc/environment
echo TG_CHANNEL_ID=$TG_CHANNEL_ID >> /etc/environment
echo DSC_WEBHOOK=$DSC_WEBHOOK >> /etc/environment

/usr/sbin/crond -f -l 8