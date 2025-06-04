
# сборка
# docker build -t flask-vue-auth .

# запуск
# docker run -it flask-vue-auth

# запуск с конкретным IP адресом
# docker network create --subnet=172.20.0.0/16 customnetwork
# docker run --net customnetwork --ip 172.20.0.10 -d flask-vue-auth

FROM ubuntu:22.04
RUN apt-get update -y
#RUN apt-get upgrade -y

# установка apache2
RUN apt-get install -y apache2

# установка mod_wsgi
RUN apt-get install -y libapache2-mod-wsgi-py3
RUN apt-get install -y python3-virtualenv

# вкючение mod_wsgi
RUN a2enmod rewrite

COPY backend/ /var/www/flask-vue-auth
COPY frontend/dist/ /var/www/flask-vue-auth/static
WORKDIR /var/www/flask-vue-auth

# установка зависимостей
RUN pip install -r requirements.txt

# инициализация баз данных
RUN flask db init
RUN flask db migrate -m "Initial migration."
RUN flask db upgrade

# настройка apache2
COPY apache2/flask-vue-auth.conf /etc/apache2/sites-available
COPY apache2/apache2.conf /etc/apache2
COPY apache2/ports.conf /etc/apache2

RUN a2ensite flask-vue-auth
RUN chown -R root:root instance
RUN chmod -R 777 instance

EXPOSE 80 8080

CMD ["/usr/sbin/apachectl", "-D", "FOREGROUND"]