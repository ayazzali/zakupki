import re
from lxml import etree
from datetime import datetime, timedelta

from extract import *

# def inc_masks(collection):
# 	today = datetime.today().strftime('%Y%m%d')
# 	yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')
# 	last_date = collection.find().sort([('dt', -1)]).limit(1)
# 	print list(last_date)[0]
# 	return None # '_inc_{y}_000000_{t}_000000_*.xml.zip'.format(y=yesterday, t=today)

def notifications_etl(ftp, collection, update_type):
	re_file = re.compile('.*\..*') # filter folders
	folders = (name for name in ftp.nlst() if not re_file.match(name))
	# if update_type == 'all':
		# collection.drop()
	for region in folders:
		ftp.cwd('/{region}/notifications'.format(region=region))
		if update_type == 'inc':
			ftp.cwd('daily')
			masks = inc_masks(collection)
		elif update_type == 'all':
			mask = '*.xml.zip'
		files = ftp.nlst(mask)
		for f in files:
			xml_file = extract(ftp, f)
			documents = []
			for event, xml in etree.iterparse(xml_file, tag='{http://zakupki.gov.ru/oos/export/1}*'):
				if event == 'end' and xml.tag != '{http://zakupki.gov.ru/oos/export/1}export':
					documents.append(transform_notification(xml))
					xml.clear()
			load(collection, documents)

		# xml = extract()
		# file_names = get_file_names(ftp, db, update_type, 'notifications', region)
		# insert_notifications(file_names, db, ftp, region)