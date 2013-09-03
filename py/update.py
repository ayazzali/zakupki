import argparse
from ftplib import FTP
import re
import psycopg2
from lxml import etree
from datetime import datetime, timedelta
import gc

from process import *

config = {
	'notifications': {
		'ftp': FTP('ftp.zakupki.gov.ru', 'free', 'free'),
		'db':  psycopg2.connect(database='zakupki', user='roveo'),
		'process': process_notifications
	},
	'organizations': {
		'ftp': FTP('ftp.zakupki.gov.ru', 'anonymous'),
		'db':  psycopg2.connect(database='zakupki', user='roveo'),
		'process': process_organizations
	},
	'products': {
		'ftp': FTP('ftp.zakupki.gov.ru', 'anonymous'),
		'db':  psycopg2.connect(database='zakupki', user='roveo'),
		'process': process_products
	}
}

if __name__ == '__main__':
	# command line arguments
	argparser = argparse.ArgumentParser()
	argparser.add_argument(dest='type', choices=('inc', 'all')) # incremental or full update
	argparser.add_argument('-n', '--notifications', dest='sections', action='append_const', const='notifications')
	argparser.add_argument('-o', '--organizations', dest='sections', action='append_const', const='organizations')
	argparser.add_argument('-p', '--products', dest='sections', action='append_const', const='products')
	args = argparser.parse_args()
	if not args.sections: args.sections = ['products', 'organizations', 'notifications']

	for section in args.sections:
		db = config[section]['db']
		ftp = config[section]['ftp']
		config[section]['process'](ftp, db, args.type)
		db.close()
		ftp.close()