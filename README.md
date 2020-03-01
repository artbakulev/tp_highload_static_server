docker build . -t artbakulev
docker run -p 80:80 -v httpd.conf:/etc/httpd.conf:ro -v /Users/artyombakulev/Learning/tp_highload_static_server/http-test-suite:/var/www/html:ro artbakulev:latest
