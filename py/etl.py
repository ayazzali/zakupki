import re
from lxml import etree
from datetime import datetime, timedelta

from transform import *
from utils import *

def contracts_etl(ftp, collection, update_type):
	'''
		Get a list of files for each region, append to list.

		Load and parse files, for each file call transform
		appending it to the dict list, upsert the list.
	'''
	# Build file list
	print ts(), 'Building file list'
	re_file = re.compile('.*\..*') # filter folders
	folders = (name for name in ftp.nlst() if not re_file.match(name))
	files = []
	for region in folders:
		print ts(), region
		region_files = inc_files(collection, ftp, region) if update_type == 'inc' else all_files(collection, ftp, region)
		files.extend(region_files)
	size = 0.0
	for f in files:
		size += ftp.size(f)
	print ts(), 'Loading {len} files, {size} Mb total'.format(len=len(files), size=round(size / (1024 * 1024), 2))
	for f in files:
		print ts(), f
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