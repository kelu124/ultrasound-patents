#!/usr/bin/python
import sys
from urllib2 import urlopen
import bs4 as BeautifulSoup
import urllib2
import MySQLdb
from tecpass import * 


# USAGE
# python patent.py US3541840 US3714817 US3864660
#


cursor=db.cursor()

add_patent = ("INSERT INTO patents "
               "(pTitre, pLongID, pShortID, pAppDate, pInventors, pAbstract, pBackWard, pForWard, pGeo) "
               "VALUES (%s, %s, %s, %s, %s,  %s, %s, %s, %s)")


RootURL = 'http://www.google.com/patents/'

t = sys.argv
del t[0]
print t

for patentID in t:

	query = ("SELECT uID FROM patents "
	"WHERE pShortID LIKE %s ")
	numrows = cursor.execute(query, patentID)

	if not(numrows):
		print "Brevet pas trouve!"
		pURL = RootURL + patentID
		print pURL
		req = urllib2.Request(pURL, headers={'User-Agent' : "foobar"})
		response = urllib2.urlopen(req)
		html = response.read()
		soup = BeautifulSoup.BeautifulSoup(html)

		## Obtention des differents parametres
		pURL = RootURL + patentID

		PatentTitle = soup.find_all("span", class_="patent-title")[0].get_text()
		PatentLongID = soup.find_all("td", class_="single-patent-bibdata")[0].get_text()
		PatentShortID = patentID
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
		BackWardList = []
		#print BackWardC
		if len(BackWardC) :
			BackWardC = soup.find(id="backward-citations").parent.find_all("a")
			for child in BackWardC:
		   		BackWardList.append(str(child.get_text()))

		ForWardC = soup.find_all(id="forward-citations")
		ForWardList = []
		if len(ForWardC) :
			ForWardC = soup.find(id="forward-citations").parent.find_all("a")
			for child in ForWardC:
		    		ForWardList.append(str(child.get_text()))

		BackWardList = filter(None, BackWardList)
		ForWardList = filter(None, ForWardList)
		BackWardList = ', '.join(BackWardList)
		ForWardList = ', '.join(ForWardList)
		#encodage en UTF8.. on ne sait jamais
		data_patent = (PatentTitle.encode( "utf-8" ), PatentLongID.encode( "utf-8" ), PatentShortID.encode( "utf-8" ), PatentAppDate.encode( "utf-8" ), InventorList.encode( "utf-8" ), PatentAbstract.encode( "utf-8" ), BackWardList.encode( "utf-8" ), ForWardList.encode( "utf-8" ), GeoList.encode( "utf-8" ))
		cursor.execute(add_patent, data_patent)





db.commit()
cursor.close()
db.close()
