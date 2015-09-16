from lxml import etree
import json
import collections


def localname(element):
    return etree.QName(element).localname


class Zparser:

    ''' Use to parse raw XML files with document records.
    '''

    def __init__(self):
        ''' __init__
        '''

    def to_dicts(self, f):
        ''' Extract all documents from a file and return them as
            generator of dicts.
        '''
        document_element = f.name.split('_')[0]
        xml = etree.iterparse(f)
        for event, element in xml:
            name = localname(element)
            if name == document_element:
                result = self.element_to_dict(element)
                result['doc_type'] = name
                yield result

    def element_to_dict(self, element):
        ''' Recursively convert a single etree.Element node into dict.
        '''
        if len(element) == 0:  # leaf node, no children
            return element.text
        # non-leaf
        name_counts = collections.Counter([localname(child) for child in element.iterchildren()])
        result = {}
        for child in element.iterchildren():
            name = localname(child)
            if name_counts[name] == 1:  # node can be represented as nested dict
                result[name] = self.element_to_dict(child)
            else:  # multiple elements should be represented as nested list
                if name not in result:
                    result[name] = []
                result[name].append(self.element_to_dict(child))
        return result
