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
zakupki_db = db.connect(host='localhost', database='zakupki', user='roveo', password='test')
zakupki_cur = zakupki_db.cursor()
# truncate tables
zakupki_cur.execute('truncate table notifications;')
zakupki_db.commit()

for region in folders:
	# months' records
	zakupki_ftp.cwd('/' + region + '/notifications') # change wd
	file_names = zakupki_ftp.nlst('*.zip') # list zip files
	for file_name in file_names:
		print(ts(), file_name, end='\t')
		zip_file = retr(zakupki_ftp, file_name)
		xml_file = unzip(zip_file)
		xml = etree.parse(xml_file)
		zip_file.close()
		xml_file.close()
		for notification in xml.xpath('/*/*', namespaces=ns):
			row = notification_xml(notification, ns) + (region,)
			zakupki_cur.execute('''
				insert into notifications
				(rec_id, notification_number, notification_type, version_number, create_date, publish_date, placer_regnum, placer_name, order_name, last_name, first_name, middle_name, post_address, email, phone, href, print_form, folder_name)
				values
				(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
			''', row)
			zakupki_db.commit()
		print('[DONE]')
	break

for region in folders:
	# daily records
	zakupki_ftp.cwd('/' + region + '/notifications/daily')
	# max_date in db
	zakupki_cur.execute('select max(publish_date) from notifications where folder_name = %s;', (region,))
	max_date = zakupki_cur.fetchone()[0]
	# print(max_date)
	start_date = max_date + timedelta(days=1)
	# print(type(max_date))
	mask = '*{date1}_000000_{date2}_000000*'.format(date1=start_date.strftime('%Y%m%d'), date2=(start_date + timedelta(days=1)).strftime('%Y%m%d'))
	print(zakupki_ftp.nlst(mask))
	break

zakupki_ftp.close()
zakupki_cur.close()
zakupki_db.close()
