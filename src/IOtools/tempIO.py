# -*- coding: utf-8 -*-
__author__ = 'spacegoing'
##
from src.GraphTools.PaperGraph import PaperGraph

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
##
