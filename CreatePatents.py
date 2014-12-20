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

	#print(pAb)
	pTitre = "Patent " + patent[0]
	#We do have the page tittle
	page = pywikibot.Page(site, pTitre)
	#print page.text
	text = page.text
	#print("-%s-" % text)
	OutPut = "\n\n\n\n=" + patent[0] + " : " + patent[3] + " = \n\n"
	OutPut += "\n\n== Invention date ==\n\n"
	OutPut += patent[7]
	OutPut += "\n\n== Lien vers Brevet ==\n\n"
	OutPut += "http://www.google.com/patents/"+patent[0]+"\n"

	OutPut += "\n\n== Inventeurs et bénéficiaires ==\n\n"
	ForWard = patent[6].split(', ')
	ForWard = filter(None, ForWard)
	if len(ForWard)>0:
		OutPut += "=== Inventeur(s) === \n"
		for item in ForWard:
			OutPut += "* [[" + item + "]]\n"

	ForWard = patent[5].split(', ')
	#removing possible empty beneficiaries
	ForWard = filter(None, ForWard)
	if len(ForWard)>0:
		OutPut += "=== Bénéficiaires === \n"
		for item in ForWard:
			OutPut += "* [[" + item + "]]\n"
	# putting the abstract text in
	OutPut += "\n\n= Abstract =\n\n"
	OutPut += pAb + "\n"
	#adding backwards patents
	BackWard = patent[1].split(', ')
	if len(BackWard)>1:
		OutPut += "= Patents Backwards =\n\n"
		for item in BackWard:
			OutPut += "* [[Patent " + item + "]]\n"
	#adding forward 
	ForWard = patent[2].split(', ')
	if len(ForWard)>1:
		OutPut += "= Patents Forwards =\n\n"
		for item in ForWard:
			OutPut += "* [[Patent " + item + "]]\n"
	#lets add categories
	OutPut += "[[Category:Patents]][[Category:Brevets]][[Category:CoolHand]]"
	
	#lets clean it
	OutPut = unicode(OutPut, "utf-8")
	OutPut = unicodedata.normalize('NFKD', OutPut).encode('ASCII', 'ignore')
	# Output is put instead of the page.text
	page.text = OutPut #unicode(OutPut, "utf-8")

	ReZ = page.save(u"Lukes Cool Hand") # Comment ofr the wiki update track
	#print(ReZ)
	# Now we update the SQL record to mark it as archived
	ItsNow = datetime.now()
	ItsNow = ItsNow
	cursor.execute(queryUpdate,(ItsNow, patent[0]))
	#and the loop is closed


db.commit()
cursor.close()
db.close()
