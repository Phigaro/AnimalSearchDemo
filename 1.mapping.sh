#!/bin/bash 

######################################
#Mapping Kibana Collection Sample
#검색 대상인 문서들의 스키마 정의하는 단계
#
#참고 https://www.elastic.co/guide/en/kibana/5.4/tutorial-load-dataset.html
######################################

IP=127.0.0.1
ES_PORT=9200
ES_INDEX=animal


curl -XPUT ${IP}:${ES_PORT}/${ES_INDEX}'?pretty' -H 'Content-Type: application/json' -d'
{
 "settings" : {
  "index":{
   "analysis":{
    "analyzer":{
      "korean":{
      "type":"custom",
      "tokenizer":"mecab_ko_standard_tokenizer"
      }
    }
   }
  }
 },
 "mappings" : {
  "_default_" : {
   "properties" : {
    "url"             : {"type": "keyword" }, 
    "providerUrl"     : {"type": "keyword" }, 
    "providerName"    : {"type": "keyword" }, 
    "channelUrl"      : {"type": "keyword" }, 
    "channelName"     : {"type": "keyword" }, 
    "thumbnail"       : {"type": "keyword" }, 
    "title"           : {"type": "text", "analyzer": "korean", "similarity": "BM25"}, 
    "desc"            : {"type": "text", "analyzer": "korean", "similarity": "BM25"}, 
    "playCount"       : {"type": "integer" }, 
    "likeCount"       : {"type": "integer" } 
   }
  }
 }
}
'

