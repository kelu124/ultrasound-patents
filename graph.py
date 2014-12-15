#!/usr/bin/python
import sys
from urllib2 import urlopen
import bs4 as BeautifulSoup
import urllib2
# Requis pour MySQL connection
# Requis pour MySQL connection
import MySQLdb
from tecpass import * 

# USAGE 
# python graph.py > ./Bureau/graph.gdf

cursor=db.cursor()


query = ("SELECT pShortID, pBackWard, pForWard, pTitre FROM patents ")

cursor.execute(query,)
result = cursor.fetchall()

print 'nodedef>name VARCHAR,label VARCHAR, color VARCHAR'
for row in result:
	Current = row[0]
	BackWard = row[1]
	BackWard = BackWard.split(', ')
	Forward = row[2]
	Forward = Forward.split(', ')
	Titre = row[3]
	print "%s, %s, '114,116,177'" % (Current, Titre)

print 'edgedef>node1 VARCHAR,node2 VARCHAR,directed BOOLEAN'
for row in result:
	Current = row[0]
	BackWard = row[1]
	BackWard = BackWard.split(', ')
	if len(BackWard)>1:
		for item in BackWard:
			print "%s, %s, true" % (Current, item)
	Forward = row[2]
	Forward = Forward.split(', ')
	if len(Forward)>1:
		for item in Forward:
			print "%s, %s, true" % (item, Current)
	Titre = row[3]
	#print '%s, %s' % (Current, Titre)


db.commit()
cursor.close()
db.close()
