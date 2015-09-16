from zakupki import Zsource, Zparser
import json
import codecs

klu = ['Kaluzhskaja_obl']

zs = Zsource()
zs.refresh_list(klu)
fgen = zs.get_files(document_type='notification')

zp = Zparser()
with codecs.open('/Users/roveo/Desktop/test.json', 'w', encoding='UTF-8') as output:
    for f in fgen:
        dgen = zp.to_dicts(f)
        for doc in dgen:
            json.dump(doc, output, ensure_ascii=False)
            output.write('\n')
