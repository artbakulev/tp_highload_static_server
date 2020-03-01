FROM ubuntu:18.04

RUN apt-get -y update &&\
    apt-get -y upgrade &&\
    apt-get -y install python3-pip &&\
    apt-get install atop -y

ADD . .

RUN pip3 install -r requirements.txt


EXPOSE 80

CMD python3 main.py