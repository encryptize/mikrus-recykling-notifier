
# mikrus-recykling-notifier

Prosty bot w Pythonie sprawdzający stan recyklingu Mikrusa

## Instalacja
Do działania bota jest potrzebne:

 - Docker (po lekkich przeróbkach można używać bez, ale jest zalecany),
 - Bot API token do Telegrama (można go otrzymać [tutaj](https://t.me/botfather))
 - ID kanału, na którym ma być robiony announce
### docker-compose (zalecany)
```bash
wget https://raw.githubusercontent.com/Encryptize/mikrus-recykling-notifier/master/docker-compose.yaml
# Podmień zmienne w pliku na własne
docker-compose up -d
```

### Docker
```bash
git clone https://github.com/Encryptize/mikrus-recykling-notifier.git && cd mikrus-recykling-notifier
docker build -t encryptize/mikrus-recykling-notifier .
docker run -d --name=recykling_cron \
-e BOT_TOKEN=000000:xxxxxxxxxxxxxxxxxxxx \
-e CHANNEL_ID=-000000000000
-e TZ=Europe/Warsaw \
--restart unless-stopped \
encryptize/mikrus-recykling-notifier
```

## Licencja
[GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html). Plik licencji jest dostępny [tutaj](LICENSE).
