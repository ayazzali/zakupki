from zakupki import Zsource, Zparser
import json
import codecs

klu = ['Kaluzhskaja_obl']

zs = Zsource()
zs.refresh_list(klu)
fgen = zs.get_files(document_type='protocol')

zp = Zparser()
with codecs.open('/home/roveo/Desktop/test.json', 'w', encoding='UTF-8') as output:
    for f in fgen:
        print(f.name)
        dgen = zp.to_dicts(f)
        for d in dgen:
            json.dump(d, output, ensure_ascii=False)
            output.write('\n')
