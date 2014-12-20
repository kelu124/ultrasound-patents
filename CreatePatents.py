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
query = ("SELECT pShortID, pBackWard, pForWard, pTitre, pAbstract, pGeo, pInventors, pAppDate FROM patents WHERE pMaj < %s")

queryUpdate = ("UPDATE patents SET pMaj = %s WHERE pShortID = %s ")

DateMoinsUnMois = datetime.now() - timedelta(days=10000)

cursor.execute(query,DateMoinsUnMois)
result = cursor.fetchall()
site = pywikibot.Site()

for patent in result:
	pAb = str(patent[4])
	pAb = filter(allowed.__contains__, pAb)

	print(pAb)
	pTitre = "Patent " + patent[0]
	print(pTitre)
	page = pywikibot.Page(site, pTitre)
	#print page.text
	text = page.text
	#print("-%s-" % text)
	OutPut = "\n\n\n\n=" + patent[0] + " : " + patent[3] + " = \n\n"
	OutPut += "\n\n== Invention date ==\n\n"
	OutPut += patent[7]
	OutPut += "\n\n== Inventeurs et bénéficiaires ==\n\n"
	ForWard = patent[6].split(', ')
	if len(ForWard)>0:
		OutPut += "=== Inventeur(s) === \n* "
		for item in ForWard:
			OutPut += "* [[" + item + "]]\n"

	ForWard = patent[5].split(', ')
	if len(ForWard)>0:
		OutPut += "=== Bénéficiaires === \n* "
		for item in ForWard:
			OutPut += "* [[" + item + "]]\n"

	OutPut += "\n\n= Abstract =\n\n"
	OutPut += pAb + "\n"
	OutPut += "= Patents Backwards =\n\n"
	BackWard = patent[1].split(', ')
	if len(BackWard)>1:
		for item in BackWard:
			OutPut += "* [[Patent " + item + "]]\n"
	OutPut += "= Patents Forwards =\n\n"
	ForWard = patent[2].split(', ')
	if len(ForWard)>1:
		for item in ForWard:
			OutPut += "* [[Patent " + item + "]]\n"

	OutPut += "[[Category:Patents]][[Category:Brevets]][[Category:CoolHand]]"
	

	OutPut = unicode(OutPut, "utf-8")
	OutPut = unicodedata.normalize('NFKD', OutPut).encode('ASCII', 'ignore')

	
	page.text = OutPut #unicode(OutPut, "utf-8")

	page.save(u"Lukes Cool Hand")

	ItsNow = datetime.now()
	ItsNow = ItsNow
	cursor.execute(queryUpdate,(ItsNow, patent[0]))



db.commit()
cursor.close()
db.close()
