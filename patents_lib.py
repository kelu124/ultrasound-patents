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
from collections import Counter

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import wget

import os.path



def GetPatent(id_patent):
    
    output_directory = "./data/"
    if os.path.isfile(output_directory+id_patent):
        print "Already here"
    else:
        url = "http://patents.google.com/patent/"+id_patent
        filename = wget.download(url, out=output_directory)
    return 1

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
    #print Request
    cursor.execute(Request)
    numrows = cursor.fetchone()
    #print numrows

    FullObject = []
    ForWardList = []
    BackWardList = []
    Found = 0
    
    if not(numrows):
        print "-> Patent not found"

        pURL = "./data/"+id_patent
        file_object  = open(pURL, "r") 
        r =  file_object.read()

        soup = BeautifulSoup(r,"lxml")


        ## Obtention des differents parametres

        #PatentTitle = soup.find_all("span", class_="patent-title")[0].get_text()
        PatentTitle = soup.find_all("h1")[0].get_text().strip()
        print "PatentTitle "+PatentTitle
        
        PatentAppDate = soup(itemprop="priorityDate")[0].get_text().strip()
        print "PatentAppDate "+PatentAppDate
        
        #PatentLongID = soup.find_all("td", class_="single-patent-bibdata")[0].get_text()
        PatentLongID = id_patent.strip()
        print "PatentLongID "+PatentLongID
        PatentShortID = id_patent.strip()
        
        
        BackWardC = soup.find_all(itemprop="backwardReferencesOrig")
        #print BackWardC
        BackwardList = []
        if len(BackWardC) :
            print "There are backwards"
            for child in BackWardC:
                #BackWardList.append(str(child.get_text()))
                #print child 
                BWPatent = child.find(itemprop="publicationNumber").get_text().strip()
                print BWPatent
                BackwardList.append(BWPatent)
        else:
            print "No backwards"
        #print BackwardList
        
        
        
        FordWardC = soup.find_all(itemprop="forwardReferencesOrig")
        #print BackWardC
        ForWardList = []
        if len(FordWardC) :
            print "There are forwards"
            for child in FordWardC:
                #BackWardList.append(str(child.get_text()))
                #print child 
                FWPatent = child.find(itemprop="publicationNumber").get_text().strip()
                print FWPatent
                ForWardList.append(FWPatent)
        else:
            print "No forwards"

        

        # Assignes
        AssigneeList = []
        assignees = soup(itemprop="assigneeCurrent")
        if len(assignees):
            for geo in assignees:
                AssigneeList.append(geo.get_text())
        GeoList = ', '.join(AssigneeList)

        # Inventeurs
        InventorList = []
        GeoTrouvetout = soup(itemprop="inventor")
        if len(GeoTrouvetout):
            for geo in GeoTrouvetout:
                InventorList.append(geo.get_text())
        InventorList = ', '.join(InventorList)
        
        # Abstract
        PatentAbstract = soup.find_all(itemprop="abstract")
        PAbText = ""
        if len(PatentAbstract):
            for h in PatentAbstract:
                PAbText = PAbText + h.get_text().strip() + "\n\n"
   
        # Get content
        PatentText = soup.find_all(itemprop="content")
        PText = ""
        if len(PatentText):
            for h in PatentText:
                PText = PText + h.get_text().strip() + "\n\n"



        PatentTXT = PAbText + "\n\n" + PText

         
        BackwardList = filter(None, BackwardList)
        ForWardList = filter(None, ForWardList)
        print BackwardList
        print ForWardList
        BackWardList = ', '.join(BackwardList)
        ForWardList = ', '.join(ForWardList)
        #encodage en UTF8.. on ne sait jamais

        FullObject.append(PatentShortID)
        FullObject.append(PatentTitle)
        FullObject.append(PatentAppDate)

        FullObject.append(pURL)
        FullObject.append(GeoList)
        FullObject.append(InventorList)

        FullObject.append(PatentTXT)
        FullObject.append(BackWardList)
        FullObject.append(ForWardList)

        cursor = conn.cursor()
        cursor.execute("INSERT INTO patents VALUES (?,?,?,?,?,?,?,?,?)",FullObject)
        conn.commit()
        conn.close()


    else:
        Found = 1
        print " -> Patent found"

        conn.close()
        #time.sleep(2)

    return [Found,BackWardList,ForWardList]


def get_top(mydb):

    conn = sqlite3.connect(mydb)
    cursor = conn.cursor()
    Request =  'SELECT p_id, p_backward, p_forward FROM patents'
    #print Request
    cursor.execute(Request)
    Top = []
    DB = []
    for row in cursor:
        DB.append(row[0])
        if len(row[1].split(", ")):
            Top += row[1].split(", ")
        if len(row[2].split(", ")):
            Top +=  row[2].split(", ")
    #print numrows
    #print len(Top)
    Top = filter(None, Top) 
    TopClean = [x for x in Top if x not in DB]
    print len(TopClean)
    counts = Counter(TopClean)
    #print(counts)

    #print DB
    conn.close()

    return counts.most_common(10)

def GetTopPat(MaDB):
    Top3 = get_top(MaDB)
    for k in Top3:
        GetPatent(k[0])
        result = get_soup(k[0],MaDB)
        
    return 1




def get_images(id_patent):

    pURL = "./data/"+id_patent
    file_object  = open(pURL, "r") 
    r =  file_object.read()

    soup = BeautifulSoup(r,"lxml")
    ImgsBig = soup(itemprop="full")
    for img in ImgsBig:
        print img["content"]
        fn = img["content"].split("/")[-1].strip()
        output_directory = "./data/images/"
        if os.path.isfile(output_directory+fn):
            print fn+" is already here"
        else:
            url = img["content"]
            filename = wget.download(url, out=output_directory)
        
    return 1


