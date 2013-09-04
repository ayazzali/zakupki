import argparse
from ftplib import FTP
from pymongo import MongoClient

from etl import *
from utils import *

conf = {
	'notifications': {
		'etl': notifications_etl,
		'ftp': FTP('ftp.zakupki.gov.ru', 'free', 'free')
	}
}

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Update zakupki database.')
	parser.add_argument(choices=['all', 'inc'], dest='type', action='store')
	parser.add_argument('-n', '--notifications', dest='collections', action='append_const', const='notifications')
	args = parser.parse_args()
	if not args.collections:
		args.collections = ['notifications']

	client = MongoClient()
	db = client.zakupki
	for coll in args.collections:
		collection = db[coll]
		if args.type == 'all':
			collection.drop()
		ftp = conf[coll]['ftp']
		conf[coll]['etl'](ftp, collection, args.type)
	client.close()