import re
from lxml import etree
from datetime import datetime, timedelta

from transform import *

def inc_masks(collection, folder_name):
	one_day = timedelta(days=1)
	today = datetime.today()
	cur = collection.find({'folder_name':folder_name},{'publish_date':1,'_id':0}).sort([('publish_date', -1)]).limit(1)
	if cur.count() > 0:
		current_date = list(cur)[0]['publish_date'] + one_day
	else:
		current_date = datetime.today() - timedelta(days=7)
	masks = []
	while current_date <= today:
		date1 = current_date.strftime('%Y%m%d')
		date2 = (current_date + one_day).strftime('%Y%m%d')
		masks.append('*_inc_{date1}_000000_{date2}_000000_*.xml.zip'.format(date1=date1, date2=date2))
		current_date += one_day
	return masks

def notifications_etl(ftp, collection, update_type):
	re_file = re.compile('.*\..*') # filter folders
	folders = (name for name in ftp.nlst() if not re_file.match(name))
	for region in folders:
		ftp.cwd('/{region}/notifications'.format(region=region))
		if update_type == 'inc':
			ftp.cwd('daily')
			masks = inc_masks(collection, region)
		elif update_type == 'all':
			masks = ('*.xml.zip',)
		for mask in masks:
			files = nlst(ftp, mask)
			for f in files:
				xml_file = extract(ftp, f)
				if xml_file:
					documents = []
					for event, xml in etree.iterparse(xml_file, tag='{http://zakupki.gov.ru/oos/export/1}*'):
						if event == 'end' and xml.tag != '{http://zakupki.gov.ru/oos/export/1}export':
							document = transform_notification(xml)
							document['folder_name'] = region
							documents.append(document)
							xml.clear()
					load(collection, documents, upsert=True)

def products_etl(ftp, collection, update_type):
	if update_type == 'all':
		mask = '*.xml.zip'
	else:
		mask = 'nsiProduct_inc_*.xmp.zip'
	ftp.cwd('/auto/product')
	files = ftp.nlst(mask)
	for f in files:
		xml_file = extract(ftp, f)
		if xml_file:
			documents = []
			for event, xml in etree.iterparse(xml_file, tag='{http://zakupki.gov.ru/oos/types/1}nsiProduct'):
				if event == 'end':
					document = transform_product(xml)
					if document:
						documents.append(document)
					xml.clear()
			load(collection, documents, upsert=True)

def contracts_etl(ftp, collection, update_type):
	re_file = re.compile('.*\..*') # filter folders
	folders = (name for name in ftp.nlst() if not re_file.match(name))
	for region in folders:
		ftp.cwd('/{region}/contracts'.format(region=region))
		if update_type == 'inc':
			ftp.cwd('daily')
			masks = inc_masks(collection, region)
		elif update_type == 'all':
			masks = ('*.xml.zip',)
		for mask in masks:
			files = nlst(ftp, mask)
			for f in files:
				xml_file = extract(ftp, f)
				if xml_file:
					documents = []
					for event, xml in etree.iterparse(xml_file, tag='{http://zakupki.gov.ru/oos/export/1}contract'):
						if event == 'end':
							document = transform_contract(xml)
							document['folder_name'] = region
							documents.append(document)
							xml.clear()
					load(collection, documents, upsert=True)