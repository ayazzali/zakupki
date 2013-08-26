from ftplib import FTP
import re
import psycopg2 as db
from lxml import etree
from datetime import datetime, timedelta
import traceback

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
zakupki_db = db.connect(database='zakupki', user='roveo')
zakupki_cur = zakupki_db.cursor()
print('[DONE]')
# truncate tables and drop indices
print(ts(), 'Truncating...', end='\t')
zakupki_cur.execute('truncate table notifications;')
zakupki_db.commit()
print('[DONE]')

for region in folders:
	# months' records
	zakupki_ftp.cwd('/' + region + '/notifications') # change wd
	file_names = zakupki_ftp.nlst('*.zip') # list zip files
	try:
		insert_notifications(file_names, zakupki_db, zakupki_ftp, ns, region)
		print('[DONE]')
	except KeyboardInterrupt:
		quit()
	except:
		traceback.print_exc()

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
		insert_notifications(file_names, zakupki_db, zakupki_ftp, ns, region)

zakupki_ftp.close()
zakupki_cur.close()
zakupki_db.close()