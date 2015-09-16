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
        ''' Extract a document from a file and return it as dict.
        '''
        doc_type = f.name.split('_')[0]
        xml = etree.parse(f)
        elements = xml.xpath('/ns2:export/*', namespaces={'ns2': 'http://zakupki.gov.ru/oos/export/1'})
        for element in elements:
            name = localname(element)
            result = self.element_to_dict(element)
            result['doc_type'] = doc_type
            result['node_type'] = name
            yield result

    def element_to_dict(self, element, truncate_size=512):
        ''' Recursively convert a single etree.Element node into dict.
        '''
        if len(element) == 0:  # leaf node, no children
            text = element.text
            if text and len(text) >= truncate_size:
                text = text[:truncate_size] + '[...]'
            return text
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
