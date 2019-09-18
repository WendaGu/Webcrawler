#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# @Version :   1.0
# @Author  :   WendaGu
# @Software:   Python3.6
# @File    :   Webcrawler.py


import requests
import re
from requests.exceptions import RequestException
import json

#Erfassen des Quellcodes der Webseite
def getHTMLText(url):
	kv = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
	try:
		response = requests.get(url, headers = kv)
		if response.status_code == 200:
			return response.text
		return None
	except RequestException:
		return None

#Erfassen die List der Masterarbeiten 
def parseThesisList(slist, thesis_list_url):
	html = getHTMLText(thesis_list_url)
	#Analysieren die Nummer jeder Masterarbeit mit regular expression
	pattern = re.compile('<h4>.*?masterarbeit/job/(\d{3,4}).*?', re.S)
	aufgabe_num = re.findall(pattern, html)	
	for each in aufgabe_num:
		slist.append(each)

#Erfassen die Informationen von jeder Masterarbeit	
def getThesisInfo(slist, thesis_info_url):
	for each in slist:
		url = thesis_info_url + each + "/"
		html = getHTMLText(url)
		
		try:
			#Analysieren 'Titel', 'Studiengänge' und 'Aufgabe' mit regular expression
			pattern = re.compile('<div class="tx-zwbisdreijobs-pi2"><h1>(.*?)</h1>.*?Studiengänge: (.*?)</h5>.*?<h2>Aufgaben</h2><p>(.*?)</p>', re.S)
			items = re.findall(pattern, html)
			for item in items:
				yield{
				'Titel': item[0],
				'Studiengänge': item[1],
				'Aufgabe': item[2]
				}		
		except:
			continue
				

def main():
	thesis_list_url = 'https://www.fzi.de/de/bei-uns-arbeiten/liste/cat/studentische-abschlussarbeit/subcat/masterarbeit/'
	thesis_info_url = 'https://www.fzi.de/de/bei-uns-arbeiten/detail/cat/studentische-abschlussarbeit/subcat/masterarbeit/job/'
	output_file = 'D://KIT_ThesisInfo.txt'
	slist = []
	parseThesisList(slist, thesis_list_url)
	
	#Formatieren mit json module
	for item in getThesisInfo(slist, thesis_info_url):
		print(json.dumps(item, ensure_ascii=False, indent=1) + '\n')
		
	
if __name__ == '__main__':
	main()
				

