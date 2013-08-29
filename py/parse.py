from lxml import etree
from datetime import datetime
import traceback
from resource import getrusage, RUSAGE_SELF

from utils import *

ns = {'d': 'http://zakupki.gov.ru/oos/export/1', 's': 'http://zakupki.gov.ru/oos/types/1'} # XML namespace

# def lots_xml(xml, namespaces):
# 	return None

def parse_notification(xml):
	rec_id = retrieve(xml, './s:id/text()', int)
	notification_number = retrieve(xml, './s:notificationNumber/text()')
	notification_type = retrieve(xml, './s:placingWay/s:code/text()')
	version_number = retrieve(xml, './s:versionNumber/text()', int)
	create_date = retrieve(xml, './s:createDate/text()', parse_date)
	publish_date = retrieve(xml, './s:publishDate/text()', parse_date)
	placer_regnum = retrieve(xml, './s:order/s:placer/s:regNum/text()')
	placer_name = retrieve(xml, './s:order/s:placer/s:fullName/text()')
	order_name = retrieve(xml, './s:orderName/text()')
	last_name = retrieve(xml, './s:contactInfo/s:contactPerson/s:lastName/text()')
	first_name = retrieve(xml, './s:contactInfo/s:contactPerson/s:firstName/text()')
	middle_name = retrieve(xml, './s:contactInfo/s:contactPerson/s:middleName/text()')
	post_address = retrieve(xml, './s:contactInfo/s:orgPostAddress/text()')
	email = retrieve(xml, './s:contactInfo/s:contactEMail/text()')
	phone = retrieve(xml, './s:contactInfo/s:contactPhone/text()')
	href = retrieve(xml, './s:href/text()')
	print_form = retrieve(xml, './s:printForm/s:url/text()')
	max_price = sum(map(float, xml.xpath('./s:lots/s:lot/s:customerRequirements/s:customerRequirement/s:maxPrice/text()', namespaces=ns, smart_strings=False)))
	return (rec_id, notification_number, notification_type, version_number, create_date, publish_date, placer_regnum, placer_name, order_name, last_name, first_name, middle_name, post_address, email, phone, href, print_form, max_price)

# def parse_lots(xml, namespaces):
# 	return (len(xml.xpath('./s:lots/s:lot', namespaces=namespaces)), len(xml.xpath('./s:lots/s:lot/s:products/s:product', namespaces=namespaces)), len(xml.xpath('./s:lots/s:lot/s:customerRequirements/s:customerRequirement', namespaces=namespaces)))

