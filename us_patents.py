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
__copyright__   = "Copyright 2018, Kelu124"
__license__ 	= "cc-by-sa/4.0/"

ListOfPatents =[]


ListOfPatents.append("US3805596A")
ListOfPatents.append("US4092867A")
ListOfPatents.append("US3406564A")
ListOfPatents.append("US3690311A")
ListOfPatents.append("US3721227A")

ListOfPatents.append("US3955561A")
ListOfPatents.append("US3990300A")
ListOfPatents.append("US4200885A")
ListOfPatents.append("US4092867A")
ListOfPatents.append("US4184094A")	

ListOfPatents.append("FR2516272A1")	
ListOfPatents.append("US4274421A")	
ListOfPatents.append("US4418698A")	
ListOfPatents.append("EP0142832A2")	
ListOfPatents.append("EP0186231A2")	
ListOfPatents.append("US3690311A")	

ListOfPatents.append("US3086390A")	
ListOfPatents.append("US3815409A")	
ListOfPatents.append("US3777740A")	
ListOfPatents.append("US3969926A")	
ListOfPatents.append("US4316390A")	

ListOfPatents.append("FR2292457A1")	
ListOfPatents.append("DE2919024A1")	
ListOfPatents.append("US6106471A")	
ListOfPatents.append("DE2709991A1")	
ListOfPatents.append("DE3008553A1")	
ListOfPatents.append("EP0090567A1")	
ListOfPatents.append("US4010634A")	
ListOfPatents.append("US4337661A")

ListOfPatents.append("US3480002A")	
ListOfPatents.append("DE2719130A1")	
ListOfPatents.append("US3990300A")	
ListOfPatents.append("US4200885A")	
ListOfPatents.append("US4274421A")	
ListOfPatents.append("EP0142832A2")	
	

ListOfPatents.append("EP0186231A2")	
ListOfPatents.append("US4515165A")	
ListOfPatents.append("US4141347A")	
ListOfPatents.append("DE3214740A1")	



MaDB = "patents.db"
check_or_create_all_tables(MaDB)
for Patent in ListOfPatents:
	result = get_soup(Patent,MaDB)

if 0:
	BackWards = get_top_back(MaDB)
	for Patent in BackWards:
		result = get_soup(Patent[0],MaDB)
