#Containerized microservice application built on flask and docker

# How to built it:

pip install -r requirements

#To run:

python rx.py

It will start the receiver application on localhost @ port 5000

Sample JSON payload to send as a request from any client(POSTMAN application)
{
"packetID": "1",
"timeStamp": "11:59"
}

URL to send http request with JSON payload --  http://127.0.0.1:5000/

#Jaeger Dependency:

Requires Jaeger to be installed.

Simplest way - run a docker container of jaeger

docker run -d --name jaeger \
  -e COLLECTOR_ZIPKIN_HTTP_PORT=9411 \
  -p 5775:5775/udp \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 14268:14268 \
  -p 9411:9411 \
  jaegertracing/all-in-one:latest

To access Jaeger UI : http://localhost:16686

#To run in docker:
Need to build the docker image first using the docker file
The docker alpine file is used to keep the image size small and loaded with network tools like ping, traceroute, ssh, telnet etc.

docker build -t rx -f dockerfile_alpine .
docker run -it rx

#NOTE

Bydefault the application is meant to run in docker, to run it locally please uncomment the code in the rx.py file