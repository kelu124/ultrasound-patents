# -*- coding: utf-8 -*-
import pywikibot
# Requis pour MySQL connection
# Requis pour MySQL connection
import MySQLdb
from tecpass import * 
from datetime import datetime, date, timedelta
import unicodedata
import time
import string # pour echapper abstract

cursor=db.cursor()

# choisissons la date la plus vieille
query = ("SELECT tDate FROM tweets ORDER BY tDate LIMIT 1")
cursor.execute(query,)

result = cursor.fetchall()

for itemMax in result:
	mamax = str(itemMax[0])
	dt_obj = datetime.strptime(mamax, '%Y-%m-%d %H:%M:%S')
	mMin = date(dt_obj.year, dt_obj.month, 1)
	#mMax = date(dt_obj.year+(dt_obj.month+1)/12 , (dt_obj.month+1)%12, 1)
mNow = datetime.now()
site = pywikibot.Site()


mCurrent = datetime(mMin.year, mMin.month, mMin.day)

while (mCurrent <= mNow):
   	#print 'The date is:', mCurrent

	query = ("SELECT * FROM `tweets` WHERE `tDate` BETWEEN %s AND %s ORDER BY `tDate` ASC")
	mNext = datetime(mCurrent.year+(mCurrent.month)/12, (mCurrent.month)%12+1, 1)
	cursor.execute(query,(mCurrent,mNext))

	result = cursor.fetchall()
	

	#print(pAb)
	pTitre = "Tweets for " + mCurrent.strftime("%B") + " " + str(mCurrent.year)
	#We do have the page tittle
	page = pywikibot.Page(site, pTitre)
	#print page.text
	text = page.text
	#print("-%s-" % text)
	OutPut = "\n\n\n\n= Liste des tweets = \n\n"


	for tw33t in result:
		tWho = str(tw33t[2])
		tWhat = str(tw33t[3])
		tWhat = string.replace(tWhat, 'RT ', 'RT @') 
		tWhat = string.replace(tWhat, '@@', '@')
		tDate = str(tw33t[4])
		OutPut += "* '''"+tWho+"''' ''"+tWhat+"'' ("+tDate+")\n"
	

	OutPut += "[[Category:Twitter]][[Category:SocialNetWork]][[Category:CoolHand]]"	
	OutPut = unicode(OutPut, "latin-1")
	OutPut = unicodedata.normalize('NFKD', OutPut).encode('ASCII', 'ignore')

	page.text = OutPut #
	ReZ = page.save(u"Lukes Cool Hand was there") # Comment ofr the wiki update track
	

	mCurrent = mNext

	

print ("Good bye!")


db.commit()
cursor.close()
db.close()
