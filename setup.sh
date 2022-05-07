#!/bin/bash

pip3 install -r requirements.txt
pip3 install -e .

rm -rf ~/.mysql-config/
cp -rf mysql/mysql-config ~/.mysql-config

mkdir -p ~/.mysql-storage

rm -rf ~/.grafana
cp -rf grafana ~/.grafana

VERSION=$(python setup.py --version)
docker build . --file Dockerfile --tag carequinha/mysql_client:${{ VERSION }}
docker-compose up -d