#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import json

import hashlib
import sqlite3
import urllib2
import time
import pickle as cPickle
import re

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# Manages the tables
def check_or_create_all_tables(mydb):
	conn = sqlite3.connect(mydb)
	cursor = conn.cursor()
	## Parsed data
	cursor.execute("""CREATE TABLE if not exists patents
		          (p_id text, p_title text, p_date text, 
			   p_link text, p_inventor text, p_beneficiary,
			   p_abstract text, p_backward text, p_forward text) 
		       """)


def get_soup(id_patent,mydb):


	conn = sqlite3.connect(mydb)
	cursor = conn.cursor()
	Request =  'SELECT p_id FROM patents WHERE p_id LIKE "'+id_patent+'"'
	print Request
	cursor.execute(Request)
	numrows = cursor.fetchone()
	print numrows

	FullObject = []
	ForWardList = []
	BackWardList = []
	Found = 0
	if not(numrows):
		print "Brevet pas trouve!"

		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		opener.addheader = [('Accept-Encoding', 'utf-8')]
		pURL = "http://www.google.com/patents/"+id_patent
		try:
			r =  opener.open(pURL).read()
		except urllib2.HTTPError:
			return [1,[],[]]

		
		soup = BeautifulSoup(r,"lxml")

		## Obtention des differents parametres
		

		PatentTitle = soup.find_all("span", class_="patent-title")[0].get_text()
		PatentLongID = soup.find_all("td", class_="single-patent-bibdata")[0].get_text()
		PatentShortID = id_patent
		PatentAppDate = soup.find_all("td", class_="single-patent-bibdata")[3].get_text()

		Geos = soup.find_all("tr", class_="patent-bibdata-list-row")
		Geos = Geos[1].find_all("span", class_="patent-bibdata-value")
		
		GeoList = []

		for child in Geos:
			if len(child.find_all("a")):
				GeoList.append(str(child.find_all("a")[0].get_text()))
			    #print(child.find_all("a")[0].get_text())
		GeoList = filter(None, GeoList)
		GeoList = ', '.join(GeoList)
		print GeoList

		Inventors = soup.find_all("tr", class_="patent-bibdata-list-row")
		Inventors = Inventors[2].find_all("span", class_="patent-bibdata-value")
		InventorList = []

		for child in Inventors:
		    InventorList.append(str(child.find_all("a")[0].get_text()))
		    #print(child.find_all("a")[0].get_text())
		InventorList = filter(None, InventorList)
		InventorList = ', '.join(InventorList)
		

		PatentAbstractTest = soup.find_all("div", class_="abstract")
		PatentDesc = soup.find_all("div", class_="patent-description-section")

		if len(PatentAbstractTest) == 0:
			PatentAbstract = PatentDesc[0].get_text()

		if len(PatentAbstractTest) :
			PatentAbstract = PatentAbstractTest[0].get_text()

		BackWardC = soup.find_all(id="backward-citations")

		#print BackWardC
		if len(BackWardC) :
			BackWardC = soup.find(id="backward-citations").parent.find_all("a")
			for child in BackWardC:
		   		BackWardList.append(str(child.get_text()))

		ForWardC = soup.find_all(id="forward-citations")

		if len(ForWardC) :
			ForWardC = soup.find(id="forward-citations").parent.find_all("a")
			for child in ForWardC:
		    		ForWardList.append(str(child.get_text()))

		BackWardList = filter(None, BackWardList)
		ForWardList = filter(None, ForWardList)
		BackWardList = ', '.join(BackWardList)
		ForWardList = ', '.join(ForWardList)
		#encodage en UTF8.. on ne sait jamais

		FullObject.append(PatentShortID)
		FullObject.append(PatentTitle)
		FullObject.append(PatentAppDate)

		FullObject.append(pURL)
		FullObject.append(GeoList)
		FullObject.append(InventorList)


		FullObject.append(PatentAbstract)
		FullObject.append(BackWardList)
		FullObject.append(ForWardList)

		cursor = conn.cursor()
		cursor.execute("INSERT INTO patents VALUES (?,?,?,?,?,?,?,?,?)",FullObject)
		conn.commit()
		conn.close()


	else:
		Found = 1
		print "Already found"

	conn.close()
	#time.sleep(2)

	return [Found,BackWardList,ForWardList]



