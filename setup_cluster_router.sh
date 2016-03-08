#!/bin/bash

sudo apt-get install vim -y
sudo apt-get install git -y
sudo apt-get install tor -y
sudo pkill tor
sudo apt-get install tor-arm

sudo apt-get update && sudo apt-get install apache2 -y
echo '<!doctype html><html><body><h1>Hello World!</h1></body></html>' | sudo tee /var/www/html/index.html


git clone https://bootsz@bitbucket.org/bootsz/tor_bootstrap.git

export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`
echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update -y
sudo apt-get install gcsfuse -y

apt-get install tor-arm

