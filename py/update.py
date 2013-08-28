import argparse
from ftplib import FTP
import re
import psycopg2 as db
from lxml import etree
from datetime import datetime, timedelta
import gc

from file_utils import * # ts(), retr(), unzip()
from parse import *      # notification()

if __name__ == '__main__':
	# command line arguments
	argparser = argparse.ArgumentParser()
	argparser.add_argument(dest='type', choices=('daily', 'full'))
	argparser.add_argument('-n', '--notifications', dest='scope', action='append_const', const='notifications')
	args = argparser.parse_args()
	if not args.scope: args.scope = ['notifications']

	# connect FTP
	print(ts(), 'connecting FTP...', end='\t')
	zakupki_ftp = FTP('ftp.zakupki.gov.ru', 'free', 'free')
	print('[DONE]')

	# connect postgresql database
	print(ts(), 'Connecting database zakupki...', end='\t')
	zakupki_db = db.connect(database='zakupki', user='roveo')
	zakupki_cur = zakupki_db.cursor()
	print('[DONE]')

	if args.type == 'full':
		# truncate tables and drop indices
		print(ts(), 'Truncating...', end='\t')
		zakupki_cur.execute('truncate table notifications;')
		zakupki_db.commit()
		print('[DONE]')

	# NLST folders
	re_file = re.compile('.*\..*') # filter folders
	folders = (name for name in zakupki_ftp.nlst() if not re_file.match(name))

	ns = {'d': 'http://zakupki.gov.ru/oos/export/1', 's': 'http://zakupki.gov.ru/oos/types/1'} # XML namespace
	# ['OK', 'EF', 'ZK', 'PO', 'SZ', 'Cancel']

	for scope in args.scope:
		for region in folders:
			zakupki_ftp.cwd('/{region}/{scope}'.format(region=region, scope=scope)) # change wd
			file_names = []
			if args.type == 'daily':
				zakupki_ftp.cwd('daily')
				zakupki_cur.execute('select max(publish_date) from notifications where folder_name = %s;', (region,))
				last_date = zakupki_cur.fetchone()[0]
				if last_date:
					current_date = last_date + timedelta(days=1)
				else:
					current_date = datetime.today() - timedelta(months=1)
				end_date = datetime.today() - timedelta(days=1)
				while current_date <= end_date: # from last date in this region to today
					mask = current_date.strftime('*%Y%m%d_000000_') + (current_date + timedelta(days=1)).strftime('%Y%m%d_000000*.xml.zip')
					file_names.extend(zakupki_ftp.nlst(mask))
					current_date += timedelta(days=1)
			elif args.type == 'full':
				file_names.extend(zakupki_ftp.nlst('*.zip'))
			insert_notifications(file_names, zakupki_db, zakupki_ftp, ns, region)

	zakupki_ftp.close()
	zakupki_cur.close()
	zakupki_db.close()