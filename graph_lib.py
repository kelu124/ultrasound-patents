#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from glob import glob
import markdown
import re
import graphviz as gv
import functools
# Wand for SVG to PNG Conversion
from wand.api import library
import wand.color
import wand.image
import Image
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup
import urllib2

 

styles = {
    'graph': {
        'label': 'Mapping patents',
	'layout':"neato",
	'fontsize':"9",

	#'outputorder':'edgesfirst',
	"overlap":"false",
        #'rankdir': 'BT',
    }
}

def apply_styles(graph, styles):
    graph.graph_attr.update(
        ('graph' in styles and styles['graph']) or {}
    )

    return graph

# -------------------------
# Aide pour le graphe
# -------------------------

graph = functools.partial(gv.Graph, format='svg')
digraph = functools.partial(gv.Digraph, format='svg')
PatentsGraph =  digraph()

def Svg2Png(svgfile):
	output_filename = svgfile+'.png'
	input_filename = svgfile+'.svg'

	svg_file = open(input_filename,"r")

	with wand.image.Image() as image:
	    with wand.color.Color('transparent') as background_color:
		library.MagickSetBackgroundColor(image.wand, background_color.resource) 
	    image.read(blob=svg_file.read())
	    png_image = image.make_blob("png32")

	with open(output_filename, "wb") as out:
	    out.write(png_image)



def getGraph(mydb):
	conn = sqlite3.connect(mydb)
	cursor = conn.cursor()
	SQLrequest = 	"""SELECT p_id , p_title , p_backward , p_forward  FROM patents ORDER BY RANDOM() LIMIT 5"""
	cursor.execute(SQLrequest)
	numrows = cursor.fetchall()

	print numrows
	for item in numrows:
		print item

		PatentsGraph.node(item[0], style="rounded,filled", fillcolor="yellow")
		BackW = item[2].split(", ")
		ForW = item[3].split(", ")

		for BackItem in BackW:
			PatentsGraph.node(BackItem,border="0")	
			PatentsGraph.edge(BackItem,item[0])
			
		for ForwardItem in ForW:
			PatentsGraph.node(ForwardItem,border="0")
			PatentsGraph.edge(item[0],ForwardItem)

	apply_styles(PatentsGraph, styles)

	PatentsGraph.render("graph.data")
	Svg2Png("graph.data")

