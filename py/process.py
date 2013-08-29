import re
from datetime import datetime

from insert import *

def get_file_names(ftp, db, update_type, section, region):
	if update_type == 'all':
		file_names = ftp.nlst('*.xml.zip')
	elif update_type == 'inc':
		cur = db.cursor()
		ftp.cwd('daily')
		cur.execute('select max(publish_date) from {section} where folder_name = %s;'.format(section=section), (region,))
		last_date = cur.fetchone()[0]
		cur.close()
		if last_date:
			current_date = last_date + timedelta(days=1)
		else:
			current_date = datetime.today() - timedelta(days=30)
		end_date = datetime.today()
		file_names = []
		while current_date <= end_date: # from last date in this region to today
			mask = current_date.strftime('*%Y%m%d_000000_') + (current_date + timedelta(days=1)).strftime('%Y%m%d_000000*.xml.zip')
			file_names.extend(ftp.nlst(mask))
			current_date += timedelta(days=1)
	return file_names

def process_notifications(ftp, db, update_type):
	re_file = re.compile('.*\..*') # filter folders
	folders = (name for name in ftp.nlst() if not re_file.match(name))
	if update_type == 'all':
		cur = db.cursor()
		cur.execute('truncate table notifications cascade;')
		db.commit()
		cur.close()
	for region in folders:
		ftp.cwd('/{region}/notifications'.format(region=region))
		file_names = get_file_names(ftp, db, update_type, 'notifications', region)
		insert_notifications(file_names, db, ftp, region)