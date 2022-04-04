#!/usr/bin/env python3

import os
import random
import logging
import requests

# enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
CHANNEL_ID = os.environ.get("CHANNEL_ID", None)

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
        message = f"<b>{random.choice(TEXT_OFFERS)}</b>\n\n"
        for offer in offers_list:
            srv = " | ".join(str(x[1]) for x in offer.items())
            message += f"- <code>{srv}</code>,\n"
        message += "\nLink do recyklingu: https://mikr.us/recykling.html"
        return message
    else:
        return f"<b>{random.choice(TEXT_NOTHING)}</b>"

def send_message(message_text: str, disable_notification: bool = False):
    body = {"chat_id": CHANNEL_ID, "parse_mode": "HTML", "text": message_text, "disable_web_page_preview": True}
    if disable_notification:
        body["disable_notification"] = True

    requests.post(TELEGRAM_URL.format(BOT_TOKEN), body)

if __name__ == "__main__":
    if not BOT_TOKEN and not CHANNEL_ID:
        logger.error("You need to provide bot token and channel ID for bot! Quitting...")
        exit(1)
    
    logger.info("Starting to check offers")
    offers = get_offers()
    text = generate_message(offers)
    send_message(message_text=text, disable_notification=True if not offers else False)
    logger.info("Task finished!")
