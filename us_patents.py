#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------
# (c) kelu124
# cc-by-sa/4.0/
# -------------------------
# Requires GraphViz and Wand
# -------------------------
# Use ./makedoc.py full  
# to have the graphs generated
# -------------------------


from patents_lib import *

'''Description: XX.'''

__author__      = "kelu124"
__copyright__   = "Copyright 2016, Kelu124"
__license__ 	= "cc-by-sa/4.0/"

MaDB = "patents.db"
check_or_create_all_tables(MaDB)
result = get_soup("US3256733",MaDB)
print result
if not result[0]:
	BackItem = result[1].split(", ")
	for item in BackItem:
		print get_soup(item,MaDB)
	ForwardItem = result[2].split(", ")
	for item in ForwardItem:
		print get_soup(item,MaDB)
