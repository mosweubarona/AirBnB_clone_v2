#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static

#install nginx
apt-get update
apt-get install -y nginx

mkdir -p /data/web_static/releases/
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
echo "Release test" >> /data/web_static/releases/test/index.html
# Create link
ln -sfn /data/web_static/releases/test /data/web_static/current
chown -R ubuntu:ubuntu /data/ 

#static

printf %s "server {
        listen 80 default_server;
        listen [::]:80 default_server;
        add_header X-Served-By $HOSTNAME;
        root /var/www/html;
        index index.html;
        
        location /hbnb_static {
            alias /data/web_static/current;
            index index.html index.htm;
        }
}" > /etc/nginx/sites-available/default

service nginx restart
