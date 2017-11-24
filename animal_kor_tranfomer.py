#-*- coding: utf-8 -*-
def animal_kor_transfomer(animalName):
	## lion find
	if str(animalName).find("lion") != -1:
		return "사자"
	## tiger find
	if str(animalName).find("tiger") != -1:
		return "호랑이"
	## camel find
	if str(animalName).find("camel") != -1:
		return "낙타"
	## egle find
	if str(animalName).find("egle") != -1:
		return "독수리"
	## zebra find
	if str(animalName).find("zebra") != -1:
		return "얼룩말"
	return animalName