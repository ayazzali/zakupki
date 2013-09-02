from lxml import etree
from datetime import datetime
import traceback
from resource import getrusage, RUSAGE_SELF

from utils import *

ns = {'exp': 'http://zakupki.gov.ru/oos/export/1', 's': 'http://zakupki.gov.ru/oos/types/1', 'int': 'http://zakupki.gov.ru/oos/integration/1'} # XML namespace

# def lots_xml(xml, namespaces):
# 	return None

def parse_notification(xml):
	rec_id = retrieve(xml, './s:id/text()', int)
	notification_number = retrieve(xml, './s:notificationNumber/text()')
	notification_type = retrieve(xml, './s:placingWay/s:code/text()')
	version_number = retrieve(xml, './s:versionNumber/text()', int)
	create_date = retrieve(xml, './s:createDate/text()', parse_date)
	publish_date = retrieve(xml, './s:publishDate/text()', parse_date)
	placer_reg_num = retrieve(xml, './s:order/s:placer/s:regNum/text()', int)
	order_name = retrieve(xml, './s:orderName/text()')
	href = retrieve(xml, './s:href/text()')
	print_form = retrieve(xml, './s:printForm/s:url/text()')
	max_price = sum(map(float, xml.xpath('./s:lots/s:lot/s:customerRequirements/s:customerRequirement/s:maxPrice/text()', namespaces=ns, smart_strings=False)))
	return (rec_id, notification_number, notification_type, version_number, create_date, publish_date, placer_reg_num, order_name, href, print_form, max_price)

def parse_lot(xml):
	x = len(xml.xpath('./s:lots/s:lot', namespaces=ns))
	if x != 1:
		print(x)


def parse_organization(xml):
	reg_num = retrieve(xml, './s:regNumber/text()', int)
	short_name = retrieve(xml, './s:shortName/text()')
	full_name = retrieve(xml, './s:fullName/text()')
	okato = retrieve(xml, './s:factualAddress/s:OKATO/text()')
	zip = retrieve(xml, './s:factualAddress/s:zip/text()')
	postal_address = retrieve(xml, './s:postalAddress/text()')
	email = retrieve(xml, './s:email/text()')
	phone = retrieve(xml, './s:phone/text()')
	fax = retrieve(xml, './s:fax/text()')
	last_name = retrieve(xml, './s:contactPerson/s:lastName/text()')
	first_name = retrieve(xml, './s:contactPerson/s:firstName/text()')
	middle_name = retrieve(xml, './s:contactPerson/s:middleName/text()')
	inn = retrieve(xml, './s:inn/text()')
	actual = True if retrieve(xml, './s:actual/text()') == 'true' else False
	return (reg_num, short_name, full_name, okato, zip, postal_address, email, phone, fax, last_name, first_name, middle_name, inn, actual)

def parse_product(xml):
	code = retrieve(xml, './s:code/text()')
	try:
		code = int(code)
	except:
		code = ord(code) # if code is an int, return int, if code is a char, return char ascii value
	parent_code = retrieve(xml, './s:parentCode/text()', int)
	product_name = retrieve(xml, './s:name/text()')
	return (code, parent_code, product_name)







