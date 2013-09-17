from utils import *

# Documents

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

# Info

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

def transform_organization(xml):
	document = {}
	document['_id'] = retrieve(xml, './s:regNumber/text()', int)
	document['short_name'] = retrieve(xml, './s:shortName/text()')
	document['full_name'] = retrieve(xml, './s:fullName/text()')
	document['factual_address'] = {}
	document['factual_address']['okato'] = retrieve(xml, './s:factualAddress/s:OKATO/text()')
	document['factual_address']['building'] = retrieve(xml, './s:factualAddress/s:building/text()', int)
	document['factual_address']['country'] = {}
	document['factual_address']['country']['code'] = retrieve(xml, './s:factualAddress/s:country/s:countryCode/text()', int)
	document['factual_address']['country']['name'] = retrieve(xml, './s:factualAddress/s:country/s:countryFullName/text()')
	document['factual_address']['region'] = {}
	document['factual_address']['region']['type'] = retrieve(xml, './s:factualAddress/s:region/s:kladrType/text()')
	document['factual_address']['region']['code'] = retrieve(xml, './s:factualAddress/s:region/s:kladrCode/text()')
	document['factual_address']['region']['name'] = retrieve(xml, './s:factualAddress/s:region/s:fullName/text()')
	document['factual_address']['city'] = {}
	document['factual_address']['city']['type'] = retrieve(xml, './s:factualAddress/s:city/s:kladrType/text()')
	document['factual_address']['city']['code'] = retrieve(xml, './s:factualAddress/s:city/s:kladrCode/text()')
	document['factual_address']['city']['name'] = retrieve(xml, './s:factualAddress/s:city/s:fullName/text()')
	document['factual_address']['zip'] = retrieve(xml, './s:factualAddress/s:zip/text()', int)
	document['postal_address'] = retrieve(xml, './s:postalAddress/text()')
	document['email'] = retrieve(xml, './s:email/text()')
	document['phone'] = retrieve(xml, './s:phone/text()')
	document['fax'] = retrieve(xml, './s:fax/text()')
	document['contact_person'] = {}
	document['contact_person']['last_name'] = retrieve(xml, './s:contactPerson/s:lastName/text()')
	document['contact_person']['first_name'] = retrieve(xml, './s:contactPerson/s:firstName/text()')
	document['contact_person']['middle_name'] = retrieve(xml, './s:contactPerson/s:middleName/text()')
	document['accounts'] = []
	for account_xml in xml.xpath('./s:accounts/s:account', namespaces=ns()):
		account = {}
		account['bik'] = retrieve(account_xml, './s:bik/text()', int)
		account['payment_account'] = retrieve(account_xml, './s:paymentAccount/text()')
		account['personal_account'] = retrieve(account_xml, './s:personalAccount/text()')
		document['accounts'].append(account)
	document['budgets'] = []
	for budget_xml in xml.xpath('./s:budgets/s:budget', namespaces=ns()):
		budget = {}
		budget['code'] = retrieve(budget_xml, './s:code/text()', int)
		budget['name'] = retrieve(budget_xml, './s:name/text()')
		document['budgets'].append(budget)
	document['inn'] = retrieve(xml, './s:inn/text()', int)
	document['kpp'] = retrieve(xml, './s:kpp/text()', int)
	return document

# Switched off

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