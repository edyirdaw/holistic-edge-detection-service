#!/usr/bin/env bash
sudo docker build -t singularitynet/edge-detection-service .
sudo docker run -d -v /home/zelalem/pytorch-hed/etcd:/pytorch-hed/etcd -v /etc/letsencrypt:/etc/letsencrypt -it -p 8001:8001 -p 8002:8002 --name edge-detection-service singularitynet/edge-detection-service