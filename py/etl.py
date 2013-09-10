import re
from lxml import etree
from datetime import datetime, timedelta

from transform import *
from utils import inc_masks

def contracts_etl(ftp, collection, update_type):
	'''
		For each folder on FTP: if 'inc' cwd to daily,
		get file masks from inc_masks (returns file masks
		from last date in db up to today).
		
		Load and parse files, for each file call transform
		appending it to the dict list, upsert the list.
	'''
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

