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


def CreateMD(mydb):

    conn = sqlite3.connect(mydb)
    cursor = conn.cursor()

    Request =  'SELECT p_id, p_title, p_date, p_abstract, p_backward, p_forward FROM patents ORDER BY p_date'
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
