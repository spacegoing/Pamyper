# -*- coding: utf-8 -*-
__author__ = 'spacegoing'
##
import fnmatch
import networkx
import os

root = '/Users/spacegoing/AllSymlinks/macANU/honorsProjects/Proposal/PAMI'


def find_all_PDFs(root, filetype = 'pdf'):
    '''

    :param root:
    :param filetype:
    :return:
    files: 2D list of String. [[absPath, filename],...]
    '''
    regexp = '*.' + filetype
    files = []
    for currpath, dirnames, filenames in os.walk(root):
        for filename in fnmatch.filter(filenames, regexp):
            files.append([os.path.join(currpath, filename), filename])

    return files

##
