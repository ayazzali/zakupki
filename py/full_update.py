from ftplib import FTP
import re
import psycopg2 as db
from lxml import etree
from datetime import datetime, timedelta

from file_utils import * # ts(), retr(), unzip()
from parse import *      # notification()

re_file = re.compile('.*\..*') # filter folders

# connect FTP
print(ts(), 'connecting FTP...', end='\t')
zakupki_ftp = FTP('ftp.zakupki.gov.ru', 'free', 'free')
print('[DONE]')

# NLST folders
folders = (name for name in zakupki_ftp.nlst() if not re_file.match(name))

ns = { # XML namespace
		'd': ':http://zakupki.gov.ru/oos/export/1',
		's': 'http://zakupki.gov.ru/oos/types/1'
	}

# n_lst = ['OK', 'EF', 'ZK', 'PO', 'SZ', 'Cancel']

# connect postgresql database
print(ts(), 'Connecting database zakupki...', end='\t')
zakupki_db = db.connect(host='localhost', database='zakupki', user='roveo', password='test')
zakupki_cur = zakupki_db.cursor()
print('[DONE]')
truncate tables
print(ts(), 'Truncating...', end='\t')
zakupki_cur.execute('truncate table notifications;')
zakupki_db.commit()
print('[DONE]')

for region in folders:
	# months' records
	zakupki_ftp.cwd('/' + region + '/notifications') # change wd
	file_names = zakupki_ftp.nlst('*.zip') # list zip files
	for file_name in file_names:
		try:
			print(ts(), file_name, end='\t')
			zip_file = retr(zakupki_ftp, file_name, retry=5)
			xml_file = unzip(zip_file)
			xml = etree.parse(xml_file)
			zip_file.close()
			xml_file.close()
			insert_notifications(zakupki_db, xml, ns, region)
			print('[DONE]')
		except:
			print('[ERROR]')
	break

# daily records
for region in folders:
	cwd = '/' + region + '/notifications/daily/'
	zakupki_ftp.cwd(cwd)
	# max_date in db
	zakupki_cur.execute('select max(publish_date) from notifications where folder_name = %s;', (region,))
	current_date = zakupki_cur.fetchone()[0] + timedelta(days=1)
	end_date = datetime.today()
	while current_date <= end_date: # from last date in this region to today
		mask = '*{date1}_000000_{date2}_000000*'.format(date1=current_date.strftime('%Y%m%d'), date2=(current_date + timedelta(days=1)).strftime('%Y%m%d'))
		file_names = zakupki_ftp.nlst(mask)
		for file_name in file_names:
			try:
				print(ts(), file_name, end='\t')
				zip_file = retr(zakupki_ftp, file_name)
				xml_file = unzip(zip_file)
				xml = etree.parse(xml_file)
				zip_file.close()
				xml_file.close()
				insert_notifications(zakupki_db, xml, ns, region)
				print('[DONE]')
			except:
				print('[ERROR]')
		current_date += timedelta(days=1)

zakupki_ftp.close()
zakupki_cur.close()
zakupki_db.close()