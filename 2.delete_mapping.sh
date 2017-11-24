#!/bin/bash 

######################################
#지정된 Mapping을 삭제 
#정확히는 index를 삭제하는 거라, 삭제 후에는 index정의, 색인 새로해야함 
######################################

IP=127.0.0.1
ES_PORT=9200

REMOVE_INDEX_NAME=animal
curl -XDELETE ${IP}:${ES_PORT}/${REMOVE_INDEX_NAME}'?pretty'
curl -XGET ${IP}:${ES_PORT}'/_cat/indices?v&pretty'

