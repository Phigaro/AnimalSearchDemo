### Animal Search
- this project extract new feature from youtube API Media Data
- 유튜브 API를 통해 받아온 Media의 Thumbnail을 이용하여 새로운 Feature를 생성 이를 이용하여 검색에 응용함
- 동영상의 썸네일을 이용해 이를 모델을 통해 라벨을 도출.
- 라벨 데이터를 피쳐로 설정하여, 동영상 자체를 검색 할 수 있도록 함

### Dependency
- elasticsearch 5.4
- kibana 5.4
- mecab-ko-lucene-analyzer 5.4 (은전한닢 한글 형태소 분석기)
- keras (resNet50)

### thumbContent Feature
- 유튜브의 썸네일을 학습 모델을 통하여 원하는 동물의 라벨과 그 값을 산출
- 본 프로젝트에서는 Keras ResNet50을 이용하여 작업.
- Ex) "thumbContent":['zebra','0.96'] 의 형태로 저장됨

### Search Engine
- 사용하는 Video의 세션들은 다음과 같음
-    "url"             : {"type": "keyword" }, 
-    "providerUrl"     : {"type": "keyword" }, 
-    "providerName"    : {"type": "keyword" }, 
-    "channelUrl"      : {"type": "keyword" }, 
-    "channelName"     : {"type": "keyword" }, 
-    "thumbnail"       : {"type": "keyword" }, 
-    "title"           : {"type": "text", "analyzer": "korean", -"similarity": "BM25"}, 
-    "desc"            : {"type": "text", "analyzer": "korean", -"similarity": "BM25"}, 
-    "playCount"       : {"type": "integer" }, 
-    "likeCount"       : {"type": "integer" } 

- 현재 검색에 사용하는 feature는 title와 desc를 BM25 모델을 통해 Text를 검색함
- thumbContent 라는 피쳐를 생성.
- title, desc, thubContent 사용


