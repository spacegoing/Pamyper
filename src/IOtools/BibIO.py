# -*- coding: utf-8 -*-
__author__ = 'spacegoing'
##
from pprint import pprint
from src.GraphTools.PaperGraph import PaperGraph
import bibtexparser

bibfile_path = './temp_bib_file.bib'

with open(bibfile_path, 'r') as infile:
    bibdb = bibtexparser.load(infile)

project_name = 'Honours_Project'
PG = PaperGraph(project_name)
##


##
for i,e in enumerate(bibdb.entries):
    try:
        bib_title = e.get('title',
                          '\tBib_key_error. Bib No.: %d' % i)

        [node,title] = PG.find_node_with_attrs(bib_title,['title'])
        PG.node_add_attr(title,BibTex=e)
    except:
        print('BibTex\'s Title not found')
        print('BibTex No: %d'%i)
        print('BibTex Title: %s'%e['title'])
        print('PaperG Title: %s\n'%PG.node[i]['title'])

##
if __name__=='__main__':



##

##
