from utils import retrieve, ns

def transform_notification(xml):
	document = {}
	# document['id'] = retrieve(xml, './s:id/text()', int)
	document['_id'] = retrieve(xml, './s:notificationNumber/text()', int) # notificationNumber field, used for update()
	document['version_number'] = retrieve(xml, './s:versionNumber/text()', int)
	document['placing_way'] = retrieve(xml, './s:placingWay/s:code/text()')
	document['create_date'] = retrieve(xml, './s:createDate/text()', parse_datetime)
	document['placer_reg_num'] = retrieve(xml, './s:order/s:placer/s:regNum/text()', int)
	document['publish_date'] = retrieve(xml, './s:publishDate/text()', parse_datetime)
	document['order_name'] = retrieve(xml, './s:orderName/text()')
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
			requirement['max_price'] = retrieve(requirement_xml, './s:maxPrice/text()', float)
			requirement['delivery_term'] = retrieve(requirement_xml, './s:deliveryTerm/text()')
			lot['customer_requirements'].append(requirement)
		lot['products'] = []
		for product_xml in lot_xml.xpath('./s:products/s:product', namespaces=ns()):
			lot['products'].append(retrieve(product_xml, './s:code/text()', int))
		document['lots'].append(lot)
	return document

def transform_product(xml):
	document = {}
	_id = retrieve(xml, './s:code/text()', int)
	if _id: # if conversion successful, set _id to code, else return None
		document['_id'] = _id
	else:
		return None
	document['parent_code'] = retrieve(xml, './s:parentCode/text()', int)
	document['name'] = retrieve(xml, './s:name/text()')
	actual = retrieve(xml, './s:actual/text()')
	document['actual'] = True if actual == 'true' else False
	return document

def transform_contract(xml):
	document = {}
	document['_id'] = retrieve(xml, './s:id/text()', int)
	document['reg_num'] = retrieve(xml, './s:regNum/text()')
	# document['number'] = retrieve(xml, './s:number/text()', int)
	document['publish_date'] = retrieve(xml, './s:publishDate/text()', parse_datetime)
	document['sign_date'] = retrieve(xml, './s:signDate/text()', parse_date)
	document['version_number'] = retrieve(xml, './s:versionNumber/text()', int)
	document['customer'] = {}
	document['customer']['reg_num'] = retrieve(xml, './s:customer/s:regNum/text()', int)
	document['customer']['inn'] = retrieve(xml, './s:customer/s:inn/text()', int)
	document['price'] = retrieve(xml, './s:price/text()', float)
	document['products'] = []
	for product_xml in xml.xpath('./s:products/s:product', namespaces=ns()):
		product = {}
		product['okdp_code'] = retrieve(product_xml, './s:OKDP/s:code/text()', int)
		product['name'] = retrieve(product_xml, './s:name/text()')
		product['okei_code'] = retrieve(product_xml, './s:OKEI/s:code/text()', int)
		product['price'] = retrieve(product_xml, './s:price/text()', float)
		product['quantity'] = retrieve(product_xml, './s:quantity/text()', int)
		product['sum'] = retrieve(product_xml, './s:sum/text()', float)
		document['products'].append(product)
	document['suppliers'] = []
	for supplier_xml in xml.xpath('./s:suppliers/s:supplier', namespaces=ns()):
		supplier = {}
		supplier['participant_type'] = retrieve(supplier_xml, './s:participantType/text()')
		supplier['inn'] = retrieve(supplier_xml, './s:inn/text()', int)
		supplier['organization_form'] = retrieve(supplier_xml, './s:organizationForm/text()')
		document['suppliers'].append(supplier)
	document['url'] = retrieve(xml, './s:printForm/s:url/text()')
	document['current_contract_stage'] = retrieve(xml, './s:currentContractStage/text()')
	return document