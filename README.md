
# mikrus-recykling-notifier

Prosty bot w Pythonie sprawdzający stan recyklingu Mikrusa

## Instalacja
Do działania bota jest potrzebne:

 - Docker (zalecany, ale można używać bez),
 - W zależności od platformy odpowiednie dane do możliwości wysyłania powiadomienia
### docker-compose (zalecany)
```bash
wget https://raw.githubusercontent.com/Encryptize/mikrus-recykling-notifier/master/docker-compose.yaml
# Utwórz katalog "data", i wyypełnij w nim odpowiednio config z example-config.yml
# zmieniając jego nazwę na config.yml
docker-compose up -d
```

### Docker
```bash
git clone https://github.com/Encryptize/mikrus-recykling-notifier.git && cd mikrus-recykling-notifier
docker build -t encryptize/mikrus-recykling-notifier .
# W katalogu "data" wypełnij odpowiednio config z example-config.yml i nazwij go config.yml
docker run -d --name=recykling_cron \
-e TZ=Europe/Warsaw \
-v $(pwd)/data:/config \
--restart unless-stopped \
encryptize/mikrus-recykling-notifier
```

## Licencja
[GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html). Plik licencji jest dostępny [tutaj](LICENSE).
