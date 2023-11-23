#!/bin/bash

ip1=$1

docker swarm init --advertise-addr $ip1
docker network create --attachable --driver overlay testnet