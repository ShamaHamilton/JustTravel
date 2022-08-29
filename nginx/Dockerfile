FROM nginx:1.23.1-alpine

WORKDIR /usr/src/app

RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx/nginx.conf /etc/nginx/conf.d/
COPY ./ssl/justtrav.crt /etc/ssl/certs/
COPY ./ssl/justtrav_key.pem /etc/ssl/private/