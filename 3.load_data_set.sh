#!/bin/bash 

######################################
#BULK API를 사용해서 데이터를 load
#
#여기서 load라는 의미는 검색에 사용할 문서를 불러와서, elasticsearch에 색인하는 의미 
#
#참조 문서 : https://www.elastic.co/guide/en/elasticsearch/reference/5.4/docs-bulk.html
######################################

COLL_DIR=/home/elastick/SearchAnimalVideo/coll
#COLL_NAME=es_bulk_coll_sample.txt
COLL_NAME=es_bulk_coll_sample.txt

IP=127.0.0.1
ES_PORT=9200
ES_INDEX=animal
ES_TYPE=basic


#색인할 데이터 있는 위치로 이동 
cd ${COLL_DIR}

curl -H 'Content-Type: application/x-ndjson' -XPOST ${IP}:${ES_PORT}/${ES_INDEX}/${ES_TYPE}'/_bulk?pretty' --data-binary @${COLL_NAME}


