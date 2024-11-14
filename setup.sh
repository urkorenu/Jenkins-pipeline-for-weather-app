#!/bin/bash

# Install or upgrade ingress-nginx using helm
helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace ingress-nginx --create-namespace

# Wait for the ingress controller pod to be ready
kubectl wait --namespace ingress-nginx --for=condition=ready pod --selector=app.kubernetes.io/name=ingress-nginx --timeout=120s

# Get the Load Balancer DNS
lbDns=$(kubectl get svc ingress-nginx-controller -n ingress-nginx -o jsonpath="{.status.loadBalancer.ingress[0].hostname}")

# Deploy application with helm, passing the Load Balancer DNS as an argument
helm upgrade --install 'my-release' './helm' --set ingress.host="${lbDns}"

# Output the Load Balancer DNS for verification
echo "Helm deployment completed successfully with Load Balancer DNS: ${lbDns}"

