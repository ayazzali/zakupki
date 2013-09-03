from utils import *
from datetime import datetime

ns = {'exp': 'http://zakupki.gov.ru/oos/export/1', 's': 'http://zakupki.gov.ru/oos/types/1', 'int': 'http://zakupki.gov.ru/oos/integration/1'} # XML namespace

def retrieve(xml, path, fun=lambda x: x):
	try:
		return fun(xml.xpath(path, namespaces=ns)[0])
	except:
		return None

def parse_date(date_str):
	return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')

def extract(ftp, f):
	print ts(), f
	try:	
		zip_file = retr(ftp, f)
		xml_file = unzip(zip_file)
	except KeyboardInterrupt:
		traceback.print_exc()
		exit()
	except AttributeError:
		traceback.print_exc()
		exit()
	except:
		traceback.print_exc()
	# zip_file.close()
	return xml_file

def load(collection, documents):
	for document in documents:
		collection.insert(document)

def transform_notification(xml):
	document = {}
	document['id'] = retrieve(xml, './s:id/text()', int)
	document['notification_number'] = retrieve(xml, './s:notificationNumber/text()', int)
	document['version_number'] = retrieve(xml, './s:versionNumber/text()', int)
	document['create_date'] = retrieve(xml, './s:createDate/text()')
	document['placer_reg_num'] = retrieve(xml, './s:placer/s:regNum/text()')
	document['publish_date'] = retrieve(xml, './s:publishDate/text()', parse_date)
	document['href'] = retrieve(xml, './s:href/text()')
	document['document_metas'] = []
 	for meta_xml in xml.xpath('./s:documentMetas/s:documentMeta', namespaces=ns):
 		meta = {}
 		meta['file_name'] = retrieve(meta_xml, './s:fileName/text()')
 		meta['url'] = retrieve(meta_xml, './s:url/text()')
 		meta['doc_description'] = retrieve(meta_xml, './s:docDescription/text()')
 		document['document_metas'].append(meta)
	document['lots'] = []
	for lot_xml in xml.xpath('./s:lots/s:lot', namespaces=ns):
		lot = {}
		lot['ordinal_number'] = retrieve(lot_xml, './s:ordinalNumber/text()', int)
		lot['customer_requirements'] = []
		for requirement_xml in xml.xpath('./s:customerRequirements/s:customerRequirement', namespaces=ns):
			requirement = {}
			requirement['quantity'] = retrieve(requirement_xml, './s:quantity/text()', int)
			requirement['max_price'] = retrieve(requirement_xml, './s:maxPrice/text()', int)
			requirement['delivery_term'] = retrieve(requirement_xml, './s:deliveryTerm/text()')
			lot['customer_requirements'].append(requirement)
		lot['products'] = []
		for product_xml in xml.xpath('./s:products/s:product', namespaces=ns):
			lot['products'].append(retrieve(product_xml, './s:code/text()', int))
		document['lots'].append(lot)
	return document