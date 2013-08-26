from lxml import etree
from datetime import datetime
from file_utils import *

def retrieve(xml, xpath, namespaces, fun=lambda x: x):
	try:
		return fun(xml.xpath(xpath, namespaces=namespaces)[0])
	except:
		return None

def parse_date(date):
	return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')

# def lots_xml(xml, namespaces):
# 	return None

def parse_notification(xml, namespaces):
	rec_id = retrieve(xml, './s:id/text()', namespaces, int)
	notification_number = retrieve(xml, './s:notificationNumber/text()', namespaces)
	notification_type = retrieve(xml, './s:placingWay/s:code/text()', namespaces)
	version_number = retrieve(xml, './s:versionNumber/text()', namespaces, int)
	create_date = retrieve(xml, './s:createDate/text()', namespaces, parse_date)
	publish_date = retrieve(xml, './s:publishDate/text()', namespaces, parse_date)
	placer_regnum = retrieve(xml, './s:order/s:placer/s:regNum/text()', namespaces)
	placer_name = retrieve(xml, './s:order/s:placer/s:fullName/text()', namespaces)
	order_name = retrieve(xml, './s:orderName/text()', namespaces)
	last_name = retrieve(xml, './s:contactInfo/s:contactPerson/s:lastName/text()', namespaces)
	first_name = retrieve(xml, './s:contactInfo/s:contactPerson/s:firstName/text()', namespaces)
	middle_name = retrieve(xml, './s:contactInfo/s:contactPerson/s:middleName/text()', namespaces)
	post_address = retrieve(xml, './s:contactInfo/s:orgPostAddress/text()', namespaces)
	email = retrieve(xml, './s:contactInfo/s:contactEMail/text()', namespaces)
	phone = retrieve(xml, './s:contactInfo/s:contactPhone/text()', namespaces)
	href = retrieve(xml, './s:href/text()', namespaces)
	print_form = retrieve(xml, './s:printForm/s:url/text()', namespaces)
	return (rec_id, notification_number, notification_type, version_number, create_date, publish_date, placer_regnum, placer_name, order_name, last_name, first_name, middle_name, post_address, email, phone, href, print_form)

def insert_notifications(pg_connection, xml, namespaces, region):
	rows = []
	for notification in xml.xpath('/*/*', namespaces=namespaces):
		row = parse_notification(notification, namespaces) + (region,)
		rows.append(row)
	if len(rows) > 0:
		cur = pg_connection.cursor()
		query = cur.mogrify('insert into notifications (rec_id, notification_number, notification_type, version_number, create_date, publish_date, placer_regnum, placer_name, order_name, last_name, first_name, middle_name, post_address, email, phone, href, print_form, folder_name)\nvalues ' + ',\n'.join(['%s'] * len(rows)), rows)
		cur.execute(query)
		pg_connection.commit()
		cur.close()