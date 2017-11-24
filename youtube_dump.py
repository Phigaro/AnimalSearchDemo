#!/usr/bin/env python2.7
#-*- coding:utf-8 -*- 

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

import time
import numpy as np
import json
import thumb_extract as th
import animal_kor_tranfomer as akt

DEVELOPER_KEY = "{{use your API key}}"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

YOUTUBE_VIDEO_URL_PREFIX="https://www.youtube.com/watch?v="
YOUTUBE_CHANNEL_URL_PREFIX="https://www.youtube.com/channel/"


def getVideoIdList(youtube, query_list, max_results, wait_time=0.1):
	video_id_list = [] 
	for query in query_list:
		search_response = youtube.search().list(
			q=query,
			part="id",
			maxResults=max_results
		).execute()		

		for search_result in search_response.get("items", []):
			if search_result["id"]["kind"] == "youtube#video":
				video_id_list.append(search_result["id"]["videoId"])
		
		#API로 가져올 때 지연 
		time.sleep(wait_time)
	return [video_id_list[0]]

def getVideoIdInfo(youtube, video_id_list, wait_time=0.1):
	video_id_info = dict()
	VIDEO_SECTION_NUM=10

	count = 0 
	#중복해서 id 조회할 필요없으니깐 set으로 바꿔서 하나씩 조회 
	for video_id in set(video_id_list):
		video = dict() 

		search_response = youtube.videos().list(
			id=video_id,
			part="id,snippet,statistics"
		).execute()

		for search_result in search_response.get("items", []): #video_id로 조회하는 거라 한 개씩 나오지만 
			if ("snippet" in search_result) and ("statistics" in search_result):
				#youtube API에서 statistics에 일부 누락된 경우가 있은데, 그 때는 default값으로 0
				play_count = int(search_result["statistics"]["viewCount"]) if "viewCount" in search_result["statistics"] else 0
				like_count = int(search_result["statistics"]["likeCount"]) if "likeCount" in search_result["statistics"] else 0

				#ADD thumbnail classify value
				thumout = th.thumbnail_extract(search_result["snippet"]["thumbnails"]["high"]["url"])
				video = {"url":YOUTUBE_VIDEO_URL_PREFIX + search_result["id"],
					"providerUrl":"https://www.youtube.com",
					"provdierName":"YouTube",
					"channelUrl":YOUTUBE_CHANNEL_URL_PREFIX+search_result["snippet"]["channelId"],
					"channelName":search_result["snippet"]["channelTitle"],
					"thumbnail":search_result["snippet"]["thumbnails"]["high"]["url"],
					"title":search_result["snippet"]["title"],
					"desc":search_result["snippet"]["description"],
					"playCount":play_count,
					"likeCount":like_count,
					"contentThumb":[akt.animal_kor_transfomer(thumout[1]), str(thumout[2])],
					"channelFeature" : []
					}
				print "THIS IS THUMOUT"
				print [thumout[0],thumout[1],str(thumout[2])]
				# print json.dumps(video, encoding='utf-8', ensure_ascii=False)
	
				count = count + 1
				if count % 100 == 0: print count 	

		#동영상 SECTION 모두 제대로 덤프받았을 때 
		# if len(video) == VIDEO_SECTION_NUM:
		# 	print "SUCCESS"
		# 	video_id_info[video_id] = video
		# else:
		# 	print "FAILED"
		video_id_info[video_id] = video
		time.sleep(wait_time)
	return video_id_info

def youtube_dump(options):
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
		developerKey=DEVELOPER_KEY)

	#유튜브에 검색 API로 조회해올 질의 리스트 
	query_list = np.loadtxt(options.query_list_path, delimiter="\t", dtype="str").tolist()	
	print "len(query_list) : ", len(query_list)

	#해당 질의들로 유튜브 검색해서 video id를 수집 
	video_id_list = getVideoIdList(youtube, query_list, options.max_results, wait_time=0.1)
	print "len(video_id_list) : ", len(video_id_list)
	print "len(set(video_id_list)) : ", len(set(video_id_list))
	
	#video_id로 youtube에 조회해서 json형태의 데이터 수집하고, dict으로 저장  
	video_id_info = getVideoIdInfo(youtube, video_id_list, wait_time=0.1)
	print "len(video_id_info) : ", len(video_id_info)	

	#데이터를 json 포멧의 text로 저장 
	with open(options.dump_output_path, 'w') as output:
		for video_id in video_id_info:
			#print video_id, json.dumps(video, ensure_ascii=False)
			output.write(json.dumps(video_id_info[video_id], ensure_ascii=False) + "\n")	
	
		

if __name__ == "__main__":
	argparser.add_argument("--query-list-path", help="Query List Path", default="./conf/animal_list_sample.txt")
	argparser.add_argument("--dump-output-path", help="Dump Output Path", default="./output/dump_sample.txt")
	argparser.add_argument("--max-results", help="Max results", default=25)
	args = argparser.parse_args()

	try:
		youtube_dump(args)
	except HttpError, e:
		print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)	
	

