# -*- coding: utf-8 -*-
__author__ = 'spacegoing'
##
import networkx as nx
import os
import json
from pprint import pprint

# file_path = os.path.dirname(os.path.abspath(__file__))
# project_path = os.path.abspath(os.path.join(file_path, *2 * [os.path.pardir]))
# graph_database_path = project_path + '/GraphDatabase/'
# config_path = project_path + '/config/'
graph_database_path = '/Users/spacegoing/AllSymlinks/mac' \
                      'CodeLab/Python/Pamyper/GraphDatabase/'
config_path = '/Users/spacegoing/AllSymlinks/macCodeLab/Python/Pamyper/config/'


# TODO: Identity decoriter lower strip
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
            self.main_paper = set(config_file['main_paper'])
            self.attrs = set(config_file['attrs'])
            self.list_to_comma_sep_attrs = \
                set(config_file['list_to_comma_sep_attrs'])
            self.G = nx.read_gml(graph_database_path + self.project_name)
        else:
            self.main_paper = set()
            self.attrs = {'abbr', 'apa', 'absPath', 'descrip', 'tag', 'title',
                          'topic'}
            self.list_to_comma_sep_attrs = {'topic', 'tag'}
            self.G = nx.Graph()

        self.node = self.G.node

    def _list_to_comma_sep_string(self, raw_list):
        if isinstance(raw_list, list):
            return ','.join(raw_list)
        else:
            return raw_list

    def _comma_sep_string_to_list(self, raw_string):
        if isinstance(raw_string, list):
            return raw_string
        else:
            return raw_string.split(',')

    def _conca_list_to_comma_sep_string \
            (self, old_string, string_to_add):
        string_to_add = self._list_to_comma_sep_string(string_to_add)
        if old_string == '':
            return string_to_add
        else:
            if string_to_add == '':
                return old_string
            else:
                return old_string + ',' + string_to_add

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
        topic = self._list_to_comma_sep_string(topic)
        tag = self._list_to_comma_sep_string(tag)

        if title not in nodes_list:
            abbr = ''.join([i[0] for i in title.split()])
            self.G.add_node(node_no, title=title.strip().lower(), abbr=abbr,
                            absPath=abs_path, topic=topic, descrip=descrip,
                            tag=tag, apa='')
        else:
            print('Paper Already Exists: ' + title)

    def _compare_apa(self, identity, node_info):
        if node_info['apa'].startswith(identity):
            return True
        else:
            return False

    def _compare_title(self, identity, node_info):
        if node_info['title'] == identity:
            return True
        else:
            return False

    def _compare_abbr(self, identity, node_info):
        if node_info['abbr'].startswith(identity):
            return True
        else:
            return False

    def _which_id_type(self, identity):
        '''
        Distinguish apa, title, abbr identity.
        If can't determine, raise an error.
        :param identity:
        :return:
        '''
        identity = identity.strip().lower()
        if len(identity.split(' ')) == 1:
            if identity[-1].isdigit():
                return self._compare_apa
            else:
                return self._compare_abbr
        else:
            return self._compare_title

    def find_node_with_attrs(self, identity, attrs_retrieving=['apa', 'abbr', 'title']):
        '''
        Return attrs want to retrieve by specify identity.
        Identity can be automated detected by using
        'apa, title, abbr'.

        :param identity:
        :param attrs_retrieving: list of strings. Default: apa, title, abbr identity
                            If this param is empty[], return node_no only
        :return:
        nodes_attrs: list. [node_no:int, value of attrs_retrieving]
        '''
        identity = identity.lower().strip()
        condition_func = self._which_id_type(identity)
        nodes_attrs = [[i[0]] + [i[1][j] for j in attrs_retrieving]
                       for i in self.G.nodes_iter(data=True)
                       if condition_func(identity, i[1])]
        assert nodes_attrs, 'Paper not found'
        if len(nodes_attrs) > 1:
            print("Multiple Matches")
            for i in nodes_attrs:
                print('Paper No: %d' % i[0])
                print('Paper Title: %s' % self.node[i[0]]['title'])
                print('abbr: %s\tApa: %s' %
                      (self.node[i[0]]['abbr'], self.node[i[0]]['apa']))
            raise Exception('Multiple Matches')  # TODO: Refract this to return

        return nodes_attrs[0]

    def find_node_no(self, identity):
        '''
        The input can be int, string for apa, abbr, title

        :param identity: apa, abbr, title or:
                node_no:int if node_no returned,
                return node_no directly
        :return: int. node_no
        '''
        identity = identity.lower().strip()
        if isinstance(identity, int):
            return identity
        else:
            return self.find_node_with_attrs(identity, [])[0]

    def node_alter_attr(self, identity, **kwargs):
        '''

        :param identity: Can either be full title,
                        or abbr of first char of each
                        or node_no
                        word in title.
        :param kwargs: {title:string, absPath:string, descrip:string,
                        abbr:string, apa:string,
                        topic: ',' concat string tokens,
                        tag:',' concat string tokens}
        :return:
        '''
        node_no = self.find_node_no(identity)

        print('Warning: must call set_list_to_comma_sep_attrs()'
              'before add/alter list_to_comma_sep_attrs')

        for k, v in kwargs.items():
            if k in self.attrs:

                if k in self.list_to_comma_sep_attrs:
                    new_attr = self._conca_list_to_comma_sep_string(
                            self.G.node[node_no][k], v)
                    nx.set_node_attributes(self.G, k, {node_no: new_attr})
                else:
                    nx.set_node_attributes(self.G, k, {node_no: v})
            else:
                print('Key: "%s" is not an attribute of this graph' % k)

    def node_reset_attr(self, identity, *args):
        for i in args:
            if i in self.attrs:
                nx.set_node_attributes(self.G, i, {
                    self.find_node_no(identity): ''
                })
            else:
                print('Node :%s doesn\' has key %s.' % (identity, i))

    def node_add_attr(self, identity, **kwargs):
        '''

        :param identity:
        :param kwargs:
        :return:
        '''
        node_no = self.find_node_no(identity)

        for k, v in kwargs.items():
            nx.set_node_attributes(self.G, k, {node_no: v})
            if k not in self.attrs:
                self.attrs.add(k)

    def graph_delete_node(self, identity_list):
        node_no = self.find_node_no(identity_list)
        self.G.remove_node(node_no)

    def set_list_to_comma_sep_attrs(self, attrs):
        '''

        :param attrs: either be ',' sep string
                      or list of strings
        :return:
        '''
        self.list_to_comma_sep_attrs.add(
                tuple(self._comma_sep_string_to_list(attrs))
        )
        self.attrs.add(tuple(self._comma_sep_string_to_list(attrs)))

    def set_main_paper(self, identity):
        node_no = self.find_node_no(identity)
        self.main_paper.add(node_no)

    def write_config(self):
        with open(config_path + self.config_name, 'w') as outfile:
            json.dump({'main_paper': list(self.main_paper),
                       'attrs': list(self.attrs),
                       'list_to_comma_sep_attrs': list(self.list_to_comma_sep_attrs)
                       }, outfile)

    def save_graph(self):
        self.write_config()
        npath = graph_database_path + self.project_name
        nx.write_gml(self.G, npath)

    def describe_paper(self, identity):
        node_no = self.find_node_no(identity)
        node_attrs = self.G.node[node_no]

        print('File No: ' + str(node_no))
        for k, v in node_attrs.items():
            print(k + ': ' + v)

    def display_papers(self):
        for node, data in self.G.nodes_iter(data=True):
            scheme = 'File No: %d \t %s\nabbr: %s\tapa: %s'
            print(scheme % (node, data['title'], data['abbr'], data['apa']))


if __name__ == '__main__':
    project_name = 'Honours_Project'
    PG = PaperGraph(project_name)
    PG.find_node_no('fast exact inference for recursive cardinality models')
    PG.set_list_to_comma_sep_attrs('BibTex')
    # abs_path = '/Users/spacegoing/AllSymlinks/macANU/honor' \
    #            'sProjects/Proposal/PAMI/pami14-linEnvLearn.pdf'
    # title = 'Learning Weighted Lower Linear Envelope Po' \
    #         'tentials in Binary Markov Random Fields'
    # PG.add_paper(title, abs_path)
    # PG.display_papers_with_attrs()
    # PG.describe_paper('lwll')
    # PG.save_graph()
##
