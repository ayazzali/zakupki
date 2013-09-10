import argparse
from ftplib import FTP
from pymongo import MongoClient

from etl import *
from utils import *

'''
	This is configuration.
	
	For each possible document type it provides
	FTP connection to use and an ETL function to
	execute.

	ETL functions contain the higher-level logic
	that depends on FTP folder structure and
	documents type.

	These functions call lower-level functions
	such as extract() function that loads
	the file from FTP server, unzips it and
	returns a file-like object.

	That object is parsed with etree.iterparse
	(memory-efficient and fast), and for each
	document in XML file transform_*() is called
	that takes XML-etree object and returns the
	corresponding dict.

	All ETL functions are stored in etl.py,
	transform_*() functions are in transform.py,
	all the other are in utils.py.
'''
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
	# collect arguments
	parser = argparse.ArgumentParser(description='Update zakupki database.')
	'''
	 The first argument is for update type:
	 'all' means wipe database and load all data again,
	 'inc' means load data that is absent in the db.

	 The other arguments are one per collection in mongodb
	 or per document type on the source FTP server.
	'''
	parser.add_argument(choices=['all', 'inc'], dest='type', action='store')
	parser.add_argument('-n', '--notifications', dest='collections', action='append_const', const='notifications')
	parser.add_argument('-p', '--products', dest='collections', action='append_const', const='products')
	parser.add_argument('-c', '--contracts', dest='collections', action='append_const', const='contracts')
	args = parser.parse_args()
	if not args.collections: # if no collections provided, use all
		args.collections = ['contracts', 'products', 'notifications']

	print ts(), 'Starting {type} update'.format(type=args.type)
	print ts(), 'Connecting mongodb'
	client = MongoClient()

	db = client.zakupki
	
	# uncomment if mongodb uses authentication
	# db.authenticate('user', 'passwd')
	
	for coll in args.collections:
		print ts(), 'Updating {coll}'.format(coll=coll)
		collection = db[coll]
		if args.type == 'all':
			collection.drop()
		print ts(), 'Connecting FTP'
		ftp = conf[coll]['ftp']
		conf[coll]['etl'](ftp, collection, args.type)
	client.close()