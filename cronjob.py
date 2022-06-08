#!/usr/bin/env python3

import logging
import json
import yaml
import requests

# enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

MIKRUS_OFFERS = "https://mikr.us/recykling.txt"
TELEGRAM_URL = "https://api.telegram.org/bot{0}/sendMessage"

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
        message = "**Na dzisiejszy recykling oddano:**\n\n"
        for offer in offers_list:
            srv = " | ".join(str(x[1]) for x in offer.items())
            message += f"- `{srv}`,\n"
        message += "\nLink do recyklingu: https://mikr.us/recykling.html"
        return message
    else:
        return "**Wygląda na to, że dzisiaj żaden Mikrus nie znajduje się na recyklingu :(**"

def tg_send_message(message_text: str, disable_notification: bool = False) -> None:
    tg_token = config.get("telegram_settings", {}).get("bot_token", "")
    tg_channel_id = config.get("telegram_settings", {}).get("channel_id", None)

    query = {
        "chat_id": tg_channel_id,
        "parse_mode": "Markdown",
        "text": message_text,
        "disable_web_page_preview": True,
        "disable_notification": disable_notification
    }

    requests.post(TELEGRAM_URL.format(tg_token), query)

def dsc_send_message(message_text: str, offers_list: list) -> None:
    dsc_mention_id = config.get("discord_settings", {}).get("mention_id", None)
    dsc_webhook = config.get("discord_settings", {}).get("webhook_url", None)

    if offers_list and dsc_mention_id:
        message_text += f"\n<@&{dsc_mention_id}>"

    query = {
        "username": "Mikrusowy recykling",
        "avatar_url": "",
        "content": message_text,
        "embeds": [],
        "components": []
    }

    requests.post(dsc_webhook, data=json.dumps(query), headers={'Content-Type': 'application/json'})

if __name__ == "__main__":
    with open("/config/config.yml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    logger.info("Starting to check offers")
    offers = get_offers()
    text = generate_message(offers)

    if config.get("telegram_settings", {}):
        tg_send_message(message_text=text, disable_notification=bool(not offers))
    else:
        logger.warning("Credentials not provided for Telegram")

    if config.get("discord_settings", {}):
        dsc_send_message(message_text=text, offers_list=offers)
    else:
        logger.warning("Credentials not provided for Discord")

    logger.info("Task finished!")
