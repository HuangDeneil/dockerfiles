FROM nginx:1.27.0-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/conf.d/mirror.conf