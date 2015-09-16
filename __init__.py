import codecs
from time import sleep


def get_element_path(element):
    path = ''
    while element is not None:
        name = etree.QName(element).localname
        path = name + '.' + path
        element = element.getparent()
    return path


def get_element_dict(element):
    if len(element) == 0:  # leaf element
        return element.text if len(element.text) <= 512 else '...'
    # non-leaf
    name_counts = collections.Counter([etree.QName(child).localname for child in element.iterchildren()])
    result = {}
    for child in element.iterchildren():
        name = etree.QName(child).localname
        if name_counts[name] == 1:
            result[name] = get_element_dict(child)
        else:
            if name not in result:
                result[name] = []
            result[name].append(get_element_dict(child))
    return result
