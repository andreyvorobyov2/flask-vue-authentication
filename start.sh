#!/bin/bash

cd frontend
npm cache clean -f
rm -rf dist node_modules package-lock.json
npm install
npm run build

cd ../

# останавливаем и удаляем все контейнеры и сети
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker network rm $(docker network ls)

# создаем контейнер и сеть
docker build -t flask-vue-auth .
docker network create --subnet=172.20.0.0/16 mynetwork

# запускаем контейнер -it интерактивно -d фоново
docker run --net mynetwork --ip 172.20.0.10 -d flask-vue-auth
