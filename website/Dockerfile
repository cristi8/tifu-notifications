FROM nginx:stable

COPY public/ /var/www/public
COPY nginx.conf /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]
