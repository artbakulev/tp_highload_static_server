### Highload python static server based on asyncio

#### Запуск через Docker:

```
docker build -t artbakulev .
docker run -p 80:80 -v httpd.conf:/etc/httpd.conf:ro -v /{absolute_path_to_project}/tp_highload_static_server/http-test-suite:/var/www/html:ro tp-highload-hw1:latest
```

#### Запуск без контейнера:

```
python main.py
```
все конфиги в configs.yaml

#### Прогон тестов:
```
cd http-test-suite
python2 httptest.py
```
 
 #### Нагрузка через ab:
 
 ```
 ab -n 100000 -c 100 127.0.0.1/httptest/wikipedia_russia.html
 ```
 
 #### Запуск nginx:
 
 ```
docker run -it -v /{absolute_path_to_project}/tp_highload_static_server/http-test-suite:/usr/share/nginx/html:ro -p 80:80 nginx
 ```
 
 #### My server RPS:
![](benchmarks/my_inside_docker.png)
 
 #### Nginx RPS:
 ![](benchmarks/nginx_inside_docker.png)
