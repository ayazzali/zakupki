import re
from lxml import etree
from datetime import datetime, timedelta

from transform import *
from utils import *

def contracts_etl(ftp, collection, update_type):
	'''
		Get a list of files for each region, append to list.

		Load and parse files, for each file call transform,
		then load each document updating metadata.
	'''
	# Build file list
	print ts(), 'Building file list'
	re_file = re.compile('.*\..*') # filter folders
	folders = (name for name in ftp.nlst() if not re_file.match(name))
	files = []
	total_size = 0.0
	for region in folders:
		region_files = inc_files(collection, ftp, region) if update_type == 'inc' else all_files(collection, ftp, region)
		size = 0.0
		for f in region_files:
			size += ftp.size(f)
		files.extend([(f, region) for f in region_files])
		print ts(), region, round(size / (1024 * 1024), 2), 'Mb'
		total_size += size
	print ts(), 'Loading {len} files, {size} Mb total'.format(len=len(files), size=round(total_size / (1024 * 1024), 2))
	# inserting files
	meta = collection.database[collection.name + '_meta']
	for (f, region) in files:
		print ts(), f
		xml_file = extract(ftp, f)
		if xml_file:
			for event, xml in etree.iterparse(xml_file, tag='{http://zakupki.gov.ru/oos/export/1}contract'):
				if event == 'end':
					document = transform_contract(xml)
					document['folder_name'] = region
					xml.clear()
					load(collection, document, upsert=True)
					meta.update({'folder_name': region, 'max_date': {'$lt': document['publish_date'] } }, {'$set': {'max_date': document['publish_date'] } })

def products_etl(ftp, collection, update_type):
	if update_type == 'all':
		mask = '*.xml.zip'
	elif update_type == 'inc':
		mask = 'nsiProduct_inc_*.xml.zip'
	ftp.cwd('/auto/product/')
	print mask
	files = nlst(ftp, mask)
	print files
	size = 0.0
	for f in files:
		size += ftp.size(f)
	print 'Loading {len} files, {size} Mb total.'.format(len=len(files), size=round(size / (1024 * 1024), 2))
	for f in files:
		print ts(), f
		xml_file = extract(ftp, f)
		if xml_file:
			for event, xml in etree.iterparse(xml_file, tag='{http://zakupki.gov.ru/oos/types/1}nsiProduct'):
				if event == 'end':
					document = transform_product(xml)
					if document: # products document can be None if code is a string (it happens)
						load(collection, document, upsert=True)
					xml.clear()
		else:
			print ts(), 'Error loading file!'
