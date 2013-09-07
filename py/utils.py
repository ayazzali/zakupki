from datetime import datetime, date, timedelta
from tempfile import TemporaryFile
from zipfile import ZipFile, ZipInfo
import traceback

def ns():
	return {'exp': 'http://zakupki.gov.ru/oos/export/1', 's': 'http://zakupki.gov.ru/oos/types/1', 'int': 'http://zakupki.gov.ru/oos/integration/1'} # XML namespace

def ts(): # return timestamp
	return '[' + str(datetime.now()) + ']'

def nlst(ftp, mask, retry=3):
	try:
		return ftp.nlst(mask)
	except:
		if retry > 0:
			return nlst(ftp, mask, retry-1)
		else:
			return None


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
	if size != tmp.tell():
		if retry > 0:
			tmp.close()
			return retr(ftp, path, retry-1)
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

def parse_date(date):
	return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')

def extract(ftp, f):
	print ts(), f
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

def load(collection, documents):
	for document in documents:
		collection.insert(document)