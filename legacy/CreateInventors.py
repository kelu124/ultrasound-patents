import pywikibot
# Requis pour MySQL connection
# Requis pour MySQL connection
import MySQLdb
from tecpass import * 
from datetime import datetime, date, timedelta
import unicodedata
import string # pour echapper abstract
punctuation = '''!$%*()_-=+.,><:;' ?|'''
allowed = string.digits + string.letters + punctuation + "\n"


cursor=db.cursor()
query = ("SELECT pShortID, pTitre, pAppDate, pGeo, pInventors FROM patents")

queryUpdate = ("UPDATE patents SET pMaj = %s WHERE pShortID = %s ")

DateMoinsUnMois = datetime.now() - timedelta(days=10000)

cursor.execute(query,)
result = cursor.fetchall()
site = pywikibot.Site()

lInventors = []
lInvUnique = []
ReZ = []
print("\n")
for patent in result:
	Liste = patent[3] + ', ' + patent[4]
	Liste = Liste.split(', ')
	Liste = filter(None, Liste)
	lInventors = lInventors + Liste
	pTitre = "Main_Page"

[lInvUnique.append(item) for item in lInventors if item not in lInvUnique]

for GeoT in lInvUnique:
	OutPut = "\n= Inventeur =\n"
	OutPut += GeoT
	CoInv = []
	CoInvUnique = []
	BrevInv = []
	OutPut += "\n= Brevets =\n"
	for patent in result:
		Liste = patent[3] + ', ' + patent[4]
		Liste = Liste.split(', ')
		Liste = filter(None, Liste)
		if GeoT in Liste:
			BrevInv.append(patent[0])
			OutPut += "* [[Patent "+patent[0]+"]]: '''"+patent[1]+"''' (''"+patent[2]+"'').\n"
			for Inven in Liste:
				if Inven <> GeoT:
					CoInv.append(Inven)

	[CoInvUnique.append(item) for item in CoInv if item not in CoInvUnique]
	CoInvUnique.sort()
	OutPut += "\n= CoInventeurs =\n"
	for Pote in CoInvUnique:
		OutPut += "* [["+Pote+"]]\n"
	
	OutPut += "[[Category:Inventors]][[Category:CoolHand]]"
	pTitre = GeoT
	page = pywikibot.Page(site, pTitre)
	page.text = OutPut #unicode(OutPut, "utf-8")	
	ReZ = page.save(u"Lukes Cool Hand likes inventors")
	


db.commit()
cursor.close()
db.close()
