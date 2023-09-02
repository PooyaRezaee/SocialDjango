FROM nginx:1.25

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d

RUN mkdir -p /var/www/social