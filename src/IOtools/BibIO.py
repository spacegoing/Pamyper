# -*- coding: utf-8 -*-
__author__ = 'spacegoing'
##
from pprint import pprint
import bibtexparser

bibfile_path = './temp_bib_file.bib'
with open(bibfile_path,'r') as infile:
    bibdb = bibtexparser.load(infile)

##

##
