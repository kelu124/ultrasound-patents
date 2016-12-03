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
from graph_lib import *

'''Description: XX.'''

__author__      = "kelu124"
__copyright__   = "Copyright 2016, Kelu124"
__license__ 	= "cc-by-sa/4.0/"

ListOfPatents =["US3918024","US4413629","US4159462","US5295485","US3919683","US4075598","US4030343","US3918025","US3419845","US3166731","US4241608","US3864660","US3911730","US3805596","US3820387","US3693415","US3675472","US3789833","US4253338","US4319489","US4030343"]
MaDB = "patents.db"
check_or_create_all_tables(MaDB)
for Patent in ListOfPatents:
	result = get_soup(Patent,MaDB)
getGraph(MaDB)
