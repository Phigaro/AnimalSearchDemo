#!/bin/bash 

######################################
#index 확인 
######################################

IP=127.0.0.1
ES_PORT=9200

curl -XGET ${IP}:${ES_PORT}'/_cat/indices?v&pretty'

