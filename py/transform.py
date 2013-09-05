from utils import *
from datetime import datetime
import traceback

def transform_notification(xml):
	document = {}
	document['id'] = retrieve(xml, './s:id/text()', int)
	document['notification_number'] = retrieve(xml, './s:notificationNumber/text()', int)
	document['version_number'] = retrieve(xml, './s:versionNumber/text()', int)
	document['placing_way'] = retrieve(xml, './s:placingWay/s:code/text()')
	document['create_date'] = retrieve(xml, './s:createDate/text()', parse_date)
	document['placer_reg_num'] = retrieve(xml, './s:order/s:placer/s:regNum/text()', int)
	document['publish_date'] = retrieve(xml, './s:publishDate/text()', parse_date)
	document['href'] = retrieve(xml, './s:href/text()')
	document['document_metas'] = []
 	for meta_xml in xml.xpath('./s:documentMetas/s:documentMeta', namespaces=ns()):
 		meta = {}
 		meta['file_name'] = retrieve(meta_xml, './s:fileName/text()')
 		meta['url'] = retrieve(meta_xml, './s:url/text()')
 		meta['doc_description'] = retrieve(meta_xml, './s:docDescription/text()')
 		document['document_metas'].append(meta)
	document['lots'] = []
	for lot_xml in xml.xpath('./s:lots/s:lot', namespaces=ns()):
		lot = {}
		lot['ordinal_number'] = retrieve(lot_xml, './s:ordinalNumber/text()', int)
		lot['customer_requirements'] = []
		for requirement_xml in lot_xml.xpath('./s:customerRequirements/s:customerRequirement', namespaces=ns()):
			requirement = {}
			requirement['quantity'] = retrieve(requirement_xml, './s:quantity/text()', int)
			requirement['max_price'] = retrieve(requirement_xml, './s:maxPrice/text()', int)
			requirement['delivery_term'] = retrieve(requirement_xml, './s:deliveryTerm/text()')
			lot['customer_requirements'].append(requirement)
		lot['products'] = []
		for product_xml in lot_xml.xpath('./s:products/s:product', namespaces=ns()):
			lot['products'].append(retrieve(product_xml, './s:code/text()', int))
		document['lots'].append(lot)
	return document