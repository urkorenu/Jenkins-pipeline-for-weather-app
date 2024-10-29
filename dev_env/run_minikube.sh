#! /bin/bash

# Script that initiate your image on minikube env

read -p "Enter image: " repo
read -p "Enter tag: " tag
echo $repo -- $tag
echo ------------------------
echo Install docker
echo ------------------------

if [[ $(sudo systemctl status docker | grep active | awk {'print $2'}) != active ]]; then
    sudo apt install docker.io
fi

sudo usermod -aG docker $USER
# newgrp docker

echo ------------------------
echo Install helm
echo ------------------------

#install helm
wget https://get.helm.sh/helm-v3.9.3-linux-amd64.tar.gz
tar xvf helm-v3.9.3-linux-amd64.tar.gz
sudo mv linux-amd64/helm /usr/local/bin
rm helm-v3.9.3-linux-amd64.tar.gz
rm -rf linux-amd64

echo ------------------------
echo Install minikube locally
echo ------------------------

# Download and Install Minikube Binary
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Install Kubectl tool
curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# start minikube
minikube start

echo ------------------------
echo Start the app
echo ------------------------
helm upgrade --install dev-app helm --set image.repo="$repo" --set image.tag="$tag"

svc_port=$(kubectl get svc dev-app -o jsonpath='{.spec.ports[?(@.nodePort)].nodePort}')
mini_ip=$(minikube ip)
echo The app running on "$mini_ip:$svc_port"

