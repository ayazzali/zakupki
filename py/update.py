import argparse
from ftplib import FTP
from pymongo import MongoClient

from etl import *
from utils import *

conf = {
	'notifications': {
		'etl': notifications_etl,
		'ftp': FTP('ftp.zakupki.gov.ru', 'free', 'free')
	},
	'products': {
		'etl': products_etl,
		'ftp': FTP('ftp.zakupki.gov.ru', 'anonymous')
	},
	'contracts': {
		'etl': contracts_etl,
		'ftp': FTP('ftp.zakupki.gov.ru', 'free', 'free')
	}
}

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Update zakupki database.')
	parser.add_argument(choices=['all', 'inc'], dest='type', action='store')
	parser.add_argument('-n', '--notifications', dest='collections', action='append_const', const='notifications')
	parser.add_argument('-p', '--products', dest='collections', action='append_const', const='products')
	parser.add_argument('-c', '--contracts', dest='collections', action='append_const', const='contracts')
	args = parser.parse_args()
	if not args.collections:
		args.collections = ['contracts', 'products', 'notifications']

	print ts(), 'Starting {type} update'.format(type=args.type)
	print ts(), 'Connecting mongodb'
	client = MongoClient()

	db = client.zakupki
	db.authenticate('roveo', 'Ml3o5CHb')
	for coll in args.collections:
		print ts(), 'Updating {coll}'.format(coll=coll)
		collection = db[coll]
		if args.type == 'all':
			collection.drop()
		print ts(), 'Connecting FTP'
		ftp = conf[coll]['ftp']
		conf[coll]['etl'](ftp, collection, args.type)
	client.close()