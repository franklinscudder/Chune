FROM python:3.8-slim-buster
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y apache2 apache2-dev
RUN pip3 install -r /app/requirements.txt
ENV LC_ALL=C
RUN groupadd chune-group && useradd -g chune-group chune-user
RUN chown chune-user *.dat
USER chune-user
CMD mod_wsgi-express start-server --log-to-terminal --startup-log /app/app.wsgi
