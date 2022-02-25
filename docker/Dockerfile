FROM python:3.9

RUN apt-get update \
    && apt-get install nginx supervisor -y

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY base.py base.py
COPY docker/nginx.conf /etc/nginx/conf.d/scraper.conf
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN unlink /etc/nginx/sites-enabled/default

EXPOSE 80 443
CMD ["/usr/bin/supervisord"]
