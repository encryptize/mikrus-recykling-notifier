#!/usr/bin/env python3

import os
import random
import logging
import requests
import json

# enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

TG_TOKEN = os.environ.get("TG_TOKEN", None)
TG_CHANNEL_ID = os.environ.get("TG_CHANNEL_ID", None)
DSC_WEBHOOK = os.environ.get("DSC_WEBHOOK", None)

MIKRUS_OFFERS = "https://mikr.us/recykling.txt"
TELEGRAM_URL = "https://api.telegram.org/bot{0}/sendMessage"

TEXT_OFFERS = ["A w dzisiejszym recyklingu znajdziemy...", "Na dzisiejszy recykling oddano:"]
TEXT_NOTHING = ["Wygląda na to, że dzisiaj żaden Mikrus nie znajduje się na recyklingu :("]

def get_offers() -> list:
    response = requests.get(MIKRUS_OFFERS)
    response.raise_for_status()

    if 'Baza jest aktualnie pusta' not in response.text:
        servers = []
        for line in response.text.splitlines():
            srv_raw = line.replace("dni=", "").split(";")
            srv_json = {"id": srv_raw[0], "version": srv_raw[1], "param": srv_raw[2], "days": f"{srv_raw[3]} dni"}
            servers.append(srv_json)
            
        return sorted(servers, key=lambda srv: srv['version'], reverse=True)
    else:
        return []

def generate_message(offers_list: list) -> str:
    if offers_list:
        message = f"**{random.choice(TEXT_OFFERS)}**\n\n"
        for offer in offers_list:
            srv = " | ".join(str(x[1]) for x in offer.items())
            message += f"- `{srv}`,\n"
        message += "\nLink do recyklingu: https://mikr.us/recykling.html"
        return message
    else:
        return f"**{random.choice(TEXT_NOTHING)}**"

def tg_send_message(message_text: str, disable_notification: bool = False):
    query = {
        "chat_id": TG_CHANNEL_ID, 
        "text": message_text, 
        "disable_web_page_preview": True,
        "disable_notification": disable_notification
    }

    requests.post(TELEGRAM_URL.format(TG_TOKEN), query)

def dsc_send_message(message_text: str):
    query = {
        "username": "Mikrusowy recykling",
        "avatar_url": "",
        "content": message_text,
        "embeds": [],
        "components": []
    }

    requests.post(DSC_WEBHOOK, data=json.dumps(query), headers={'Content-Type': 'application/json'})

if __name__ == "__main__":    
    logger.info("Starting to check offers")
    offers = get_offers()
    text = generate_message(offers)
    
    if TG_TOKEN and TG_CHANNEL_ID:
        tg_send_message(message_text=text, disable_notification=bool(not offers))
    else:
        logger.warning("Credentials not provided for Telegram")

    if DSC_WEBHOOK:
        dsc_send_message(message_text=text)
    else:
        logger.warning("Credentials not provided for Discord")
    
    logger.info("Task finished!")
