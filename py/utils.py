from datetime import datetime, date, timedelta
from tempfile import TemporaryFile
from zipfile import ZipFile, ZipInfo
import traceback
import re

def ns(): # XML namespace
	return {
		'exp': 'http://zakupki.gov.ru/oos/export/1',
		's': 'http://zakupki.gov.ru/oos/types/1',
		'int': 'http://zakupki.gov.ru/oos/integration/1'
	}

def ts(): # return timestamp
	return '[' + str(datetime.now()) + ']'

def nlst(ftp, mask, retry=3):
	try:
		return ftp.nlst(mask)
	except:
		if retry > 0:
			# print 'Retry NLST'
			return nlst(ftp, mask, retry-1)
		else:
			return None

def ftp_size(ftp, files):
	s = 0
	for f in files:
		s += ftp.size(f)
	return float(s)

def retr(ftp, path, retry=3): # retrieve file via FTP and return
	tmp = TemporaryFile()
	try:
		size = ftp.size(path)
		ftp.retrbinary('RETR ' + path, tmp.write)
	except:
		if retry > 0:
			tmp.close()
			return retr(ftp, path, retry-1) # recursively call retr until retry is 0 (retry times)
		else:
			tmp.close()
			return None
	if size != tmp.tell(): # check if downloaded file size != file size on ftp
		if retry > 0:
			tmp.close()
			return retr(ftp, path, retry-1)
		else:
			tmp.close()
			return None
	return tmp

def unzip(zip_file): # unzip a single file and return
	zf = ZipFile(zip_file)
	zip_info = zf.infolist()[0]
	unzipped = zf.open(zip_info)
	zf.close()
	return unzipped

def retrieve(xml, xpath, fun=lambda x: x):
	try:
		return fun(xml.xpath(xpath, namespaces=ns(), smart_strings=False)[0])
	except:
		return None

def parse_datetime(date):
	return datetime.strptime(date[:19], '%Y-%m-%dT%H:%M:%S')

def parse_date(date):
	return datetime.strptime(date, '%Y-%m-%d')

def extract(ftp, f):
	try:
		zip_file = retr(ftp, f, retry=10)
		xml_file = unzip(zip_file)
	except KeyboardInterrupt:
		traceback.print_exc()
		exit()
	except AttributeError:
		traceback.print_exc()
		exit()
	except:
		traceback.print_exc()
		return None
	return xml_file

def load(collection, document, upsert=False):
	if upsert:
		spec = {'_id': document['_id']}
		collection.update(spec, document, upsert=True, multi=False)
	else:
		collection.insert(document)
	last_error = collection.database.command({'getLastError': 1})
	if not last_error['ok']:
		print 'Error during insert or update!!'
		exit()

def inc_files(collection, ftp, folder_name):
	# get metadata
	meta = collection.database[collection.name + '_meta']
	cur = meta.find({'folder_name': folder_name})
	if cur.count() == 1:
		last_date = list(cur)[0]['max_date']
	else: # if no max_date in this region yet, set last_date to None
		last_date = None
		meta.insert({'folder_name': folder_name, 'max_date': datetime(2000, 1, 1)}) # and create meta max_date element
	# list all files for this region / collection
	all_files = []
	ftp.cwd('/{region}/{collection}'.format(region=folder_name, collection=collection.name))
	ls = nlst(ftp, '*.xml.zip')
	all_files.extend(['/{region}/{collection}/'.format(region=folder_name, collection=collection.name) + x for x in ls])
	ftp.cwd('daily')
	ls = nlst(ftp, '*.xml.zip')
	all_files.extend(['/{region}/{collection}/daily/'.format(region=folder_name, collection=collection.name) + x for x in ls])
	if not last_date: # if there is no metadata, return all files
		return all_files
	else:
		files = [] # list for filtered files
		pattern = '.*_(\d{8})_(\d{6})_(\d{8})_(\d{6})_.*\.xml.zip$'
		for f in all_files:
			str_date = re.match(pattern, f).group(1) # get 1st date from the filename
			file_date = datetime.strptime(str_date, '%Y%m%d')
			if file_date >= last_date: # if we need the file, add it to files list
				files.append(f)
		return files

def all_files(collection, ftp, folder_name): # list all files for this region / collection
	meta = collection.database[collection.name + '_meta']
	meta.insert({'folder_name': folder_name, 'max_date': datetime(2000, 1, 1)}) # meta max_date element
	files = []
	ftp.cwd('/{region}/{collection}'.format(region=folder_name, collection=collection.name))
	ls = nlst(ftp, '*.xml.zip')
	files.extend(['/{region}/{collection}/'.format(region=folder_name, collection=collection.name) + x for x in ls])
	ftp.cwd('daily')
	ls = nlst(ftp, '*.xml.zip')
	files.extend(['/{region}/{collection}/daily/'.format(region=folder_name, collection=collection.name) + x for x in ls])
	return files