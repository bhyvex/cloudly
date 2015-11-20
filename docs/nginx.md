###### How to Configure the web server (NGINX without the SSL support)

First and foremost install the NGINX (and Python Flup module), like so:

<pre>
$ apt-get install nginx
$ apt-get install python-flup
</pre>

Open up your NGINX config file:

<pre>
$ vi /etc/nginx/nginx.conf
</pre>

..and paste in the following configuration:

<pre>
user cloudly cloudly;
worker_processes  2;

error_log /var/log/nginx/error_log info;

events {
    worker_connections  1024;
    use epoll;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main
        '$remote_addr - $remote_user [$time_local]'
        '"$request" $status $bytes_sent'
        '"$http_referer" "$http_user_agent"'
        '"$gzip_ratio"';

    gzip on;
    gzip_min_length 1100;
    gzip_buffers 4 8k;
    gzip_types text/plain;
    output_buffers 1 32k;
    postpone_output 1460;
    sendfile on;
    tcp_nopush  on;
    tcp_nodelay on;
    keepalive_timeout 75 20;
    ignore_invalid_headers on;
    index index.xhtml;

    client_header_timeout 10m;
    client_body_timeout 10m;
    send_timeout 10m;
    connection_pool_size 256;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 2k;
    request_pool_size 4k;

    server {
        listen 80;
        server_name projectcloudly.com;
        location /site_media  {
            alias /static/;
            }
        location ~* ^.+\.(jpg|jpeg|gif|png|ico|css|zip|tgz|gz|rar|bz2|doc|xls||pdf|js|counters) {
            access_log   off;
            expires      30d;
            }
        location / {
            fastcgi_pass 127.0.0.1:8080;
            fastcgi_param SERVER_ADDR $server_addr;
            fastcgi_param SERVER_PORT $server_port;
            fastcgi_param SERVER_NAME $server_name;
            fastcgi_param SERVER_PROTOCOL $server_protocol;
            fastcgi_param PATH_INFO $fastcgi_script_name;
            fastcgi_param REQUEST_METHOD $request_method;
            fastcgi_param QUERY_STRING $query_string;
            fastcgi_param CONTENT_TYPE $content_type;
            fastcgi_param CONTENT_LENGTH $content_length;
            fastcgi_pass_header Authorization;
            fastcgi_param REMOTE_ADDR $remote_addr;
            fastcgi_param X_FORWADRD_FOR $proxy_add_x_forwarded_for;
            fastcgi_intercept_errors off;
            }
        access_log  /var/log/nginx/cloudly.access_log main;
        error_log   /var/log/nginx/cloudly.error_log;
        }
    }
</pre>

Great! Now you should be able to run the NGINX server using the WSGI protocol on your very own server (effectively a Django server with the MySQL for the user data and Mongodb for the graphs/logging DB).

For more information about the Django and NGINX configuration see the NGINX Wiki on <a>http://wiki.nginx.org/DjangoFastCGI</a>

For information about the MongoDB visit <a>http://www.mongodb.org/</a>
