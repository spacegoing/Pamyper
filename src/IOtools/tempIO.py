# -*- coding: utf-8 -*-
__author__ = 'spacegoing'
## Read title, shell files and save to PaperGraph
from src.GraphTools.PaperGraph import PaperGraph
from src.IOtools.BibIO import query
shell_path = '/Users/spacegoing/AllSymlinks/macANU' \
             '/honorsProjects/Proposal/PAMI/pdflist.sh'
title_path = '/Users/spacegoing/AllSymlinks/macANU/honors' \
             'Projects/Proposal/PAMI/pdfstitles.txt'
shell_prefix = '! open "'
shell_suffix = '"\n'
with open(shell_path, 'r') as infile:
    path_command_list = infile.readlines()
    path_list = [i[len(shell_prefix):-len(shell_suffix)]
                 for i in path_command_list]
with open(title_path, 'r') as infile:
    title_list = infile.readlines()
    title_list = [i.strip() for i in title_list]

project_name = 'Honours_Project'
PG = PaperGraph(project_name)
for t, p in zip(title_list, path_list):
    PG.add_paper(t, p)
PG.display_papers()
PG.save_graph()
## Retrieve all PaperGraph's bibTex from Google
# Write the bib_list to .bib file
from src.GraphTools.PaperGraph import PaperGraph
from src.IOtools.GoogleInterface import query
project_name = 'Honours_Project'
PG = PaperGraph(project_name)
bib_list=list()
for i in range(0,35):
    bib_list.append(query(PG.node[i]['title']))
import pickle
with open('temp_bib_file.bib','w') as outfile:
    for i in bib_list:
        outfile.write(i[0])
##