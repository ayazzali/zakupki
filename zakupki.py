from lxml import etree
import json

filepath = '/Users/roveo/Downloads/contract__Ivanovskaja_obl_inc_20110401_000000_20110501_000000_57.xml'
events = ('end', )
tag = '{http://zakupki.gov.ru/oos/export/1}contractProcedure'
xml = etree.iterparse(filepath, events=events, tag=tag)


def get_element_path(element):
    path = ''
    while element is not None:
        name = etree.QName(element).localname
        path = name + '.' + path
        element = element.getparent()
    return path


def get_element_dict(element):
    localname = etree.QName(element).localname
    if len(element) == 0:
        return element.text
    children_names = [etree.QName(child).localname for child in element]
    print(children_names)
    if len(children_names) == len(set(children_names)):
        return {localname: {etree.QName(x).localname: get_element_dict(x) for x in element.iterchildren()}}
    else:
        return [get_element_dict(x) for x in element.iterchildren()]

for event, element in xml:
    print(json.dumps(get_element_dict(element)))
    element.clear()
