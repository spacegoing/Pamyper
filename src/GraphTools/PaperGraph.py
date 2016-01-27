# -*- coding: utf-8 -*-
__author__ = 'spacegoing'
##
import networkx as nx
import os
import json
from pprint import pprint

file_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.abspath(os.path.join(file_path, *2 * [os.path.pardir]))
graph_database_path = project_path + '/GraphDatabase/'
config_path = project_path + '/config/'


# TODO: Refract attrs. Isolate add_paper and self.attrs
# TODO: Add funcs for parse/resemble topic list
# TODO: Read BibTex
# TODO: Chinese Compatible
# File No: 32 	 高阶马尔科夫随机场及其在场景理解中的应用
# abbr: 高

class PaperGraph:
    '''

    Paper Node and attributes:
    [node_no, {title:string, absPath:string, descrip:string,
                    abbr:string, apa:string,
                    topic: ',' concat string tokens,
                    tag:',' concat string tokens}]

    node_no: int, incre from 0, step 1.

    '''

    def __init__(self, project_name):
        self.project_name = project_name + '.gml'
        self.config_name = project_name + '.pamyper'
        files_list = os.listdir(graph_database_path)
        if self.project_name in files_list:
            with open(config_path + self.config_name, 'r') as infile:
                config_file = json.load(infile)
            self.main_paper = config_file['main_paper']
            self.attrs = config_file['attrs']
            self.G = nx.read_gml(graph_database_path + self.project_name)
        else:
            self.main_paper = list()
            self.attrs = ['abbr', 'apa', 'absPath', 'descrip', 'tag', 'title',
                          'topic']
            self.G = nx.Graph()

    def set_main_paper(self, node_no):
        self.main_paper.append(node_no)

    def add_paper(self, title, abs_path, topic=[], descrip='', tag=[], apa=''):
        '''


        Check if title exists. If it is, print message to console and quit.

        Warning:
        GML format doesn't support key strings as 'A_B' style,
        so 'abs_path' is named 'absPath'.
        It neither support list(). so topic is parsed as strings
        concatenated by ',' .

        :param tag:
        :param descrip:
        :param title:
        :param abs_path:
        :param topic:
        :return:
        [node_no, {title:string, absPath:string, descrip:string,
                    abbr:string, apa:string,
                    topic: ',' concat string tokens,
                    tag:',' concat string tokens}]
        '''
        node_no = self.G.number_of_nodes()
        nodes_list = [i[1]['title'] for i in self.G.nodes(data=True)]
        title = title.strip().lower()
        topic = ','.join(topic)
        tag = ','.join(tag)

        if title not in nodes_list:
            abbr = ''.join([i[0] for i in title.split()])
            self.G.add_node(node_no, title=title.strip().lower(), abbr=abbr,
                            absPath=abs_path, topic=topic, descrip=descrip,
                            tag=tag, apa='')
        else:
            print('Paper Already Exists: ' + title)

    def _find_with_title(self, title):
        title = title.strip().lower()
        nodes_title_abbr = [(i[0], i[1]['title'], i[1]['abbr'], i[1]['apa'])
                            for i in self.G.nodes(data=True)]
        node_title_abbr = [i for i in nodes_title_abbr if title.strip().lower() == i[2]]

        assert node_title_abbr, 'Paper not found'
        return node_title_abbr

    def _find_with_abbr(self, abbr):
        '''

        :param abbr:
        :return:
        node_title_abbr: tuple: (node_no:int, title:string, abbr:string),...]
        '''
        abbr = abbr.strip().lower()
        nodes_title_abbr = [(i[0], i[1]['title'], i[1]['abbr'], i[1]['apa'])
                            for i in self.G.nodes(data=True)]
        node_title_abbr = [i for i in nodes_title_abbr if i[2].startswith(abbr)]

        assert node_title_abbr, 'Paper not found'
        if len(node_title_abbr) > 1:
            print("\nMultiple Matches: ")
            for no, title, abbr, apa in node_title_abbr:
                scheme = 'File No: %d \t %s \t %s\nabbr: %s'
                print(scheme % (no, title, apa, abbr))
            assert False

        return node_title_abbr

    def _find_with_APA(self, apa):
        apa = apa.strip().lower()
        nodes_title_abbr = [(i[0], i[1]['title'], i[1]['abbr'], i[1]['apa'])
                            for i in self.G.nodes(data=True)]
        node_title_abbr = [i for i in nodes_title_abbr if i[3] == apa]

        assert node_title_abbr, 'Paper not found'
        if len(node_title_abbr) > 1:
            print("\nMultiple Matches: ")
            for no, title, abbr, apa in node_title_abbr:
                scheme = 'File No: %d \t %s \t %s\nabbr: %s'
                print(scheme % (no, title, apa, abbr))
            assert False

        return node_title_abbr

    def _auto_find_by_identity(self, identity):
        identity = identity.strip().lower()
        if len(identity.split(' ')) == 1:
            if identity[-1].isdigit():
                node_title_abbr = self._find_with_APA()
            else:
                node_title_abbr = self._find_with_abbr(identity)
        else:
            node_title_abbr = self._find_with_title(identity)

        return node_title_abbr

    def alter_attr(self, identity, **kwargs):
        '''

        :param identity: Can either be full title,
                        or abbr of first char of each
                        word in title.
        :param kwargs: {title:string, absPath:string, descrip:string,
                        abbr:string, apa:string,
                        topic: ',' concat string tokens,
                        tag:',' concat string tokens}
        :return:
        '''
        node_title_abbr = self._auto_find_by_identity(identity)
        node_no = node_title_abbr[0]

        coma_conca_attrs_list = ['topic', 'tag']
        for k, v in kwargs.items():
            if k in self.attrs:

                if k in coma_conca_attrs_list:
                    new_attr = self.G.node[node_no][k] + ','.join(v)
                    nx.set_node_attributes(self.G, k, {node_no: new_attr})
                else:
                    nx.set_node_attributes(self.G, k, {node_no: v})
            else:
                print('Key: "%s" is not an attribute of this graph' % k)

    def node_add_attr(self, identity, **kwargs):
        '''

        :param identity:
        :param kwargs:
        :return:
        '''
        node_title_abbr = self._auto_find_by_identity(identity)
        node_no = node_title_abbr[0]

        for k, v in kwargs.items():
            nx.set_node_attributes(self.G, k, {node_no: v})
            if k not in self.attrs:
                self.attrs.append(k)

    def write_config(self):
        with open(config_path + self.config_name, 'w') as outfile:
            json.dump({'main_paper': self.main_paper,
                       'attrs': self.attrs}, outfile)

    def save_graph(self):
        self.write_config()
        npath = graph_database_path + self.project_name
        nx.write_gml(self.G, npath)

    def describe_paper(self, identity):
        node_title_abbr = self._auto_find_by_identity(identity)
        node_attrs = self.G.node[node_title_abbr[0]]

        print('File No: ' + str(node_title_abbr[0]))
        for k, v in node_attrs.items():
            print(k + ': ' + v)

    def display_by_apa(self, apa):
        nodes_attr = self.G.nodes(data=True)
        for node, attrs in nodes_attr:
            if apa == attrs['apa']:
                self.describe_paper(attrs['title'])

    def display_papers(self):
        for node, data in self.G.nodes_iter(data=True):
            scheme = 'File No: %d \t %s\nabbr: %s'
            print(scheme % (node, data['title'], data['abbr']))

    def display_papers_with_attrs(self):
        pprint(self.G.nodes(data=True))


if __name__ == '__main__':
    project_name = 'Honours_Project'
    PG = PaperGraph(project_name)
    abs_path = '/Users/spacegoing/AllSymlinks/macANU/honor' \
               'sProjects/Proposal/PAMI/pami14-linEnvLearn.pdf'
    title = 'Learning Weighted Lower Linear Envelope Po' \
            'tentials in Binary Markov Random Fields'
    PG.add_paper(title, abs_path)
    PG.display_papers_with_attrs()
    PG.describe_paper('lwll')
    PG.save_graph()
##
