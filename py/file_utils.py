from datetime import datetime, date, timedelta
from tempfile import TemporaryFile
from zipfile import ZipFile, ZipInfo

def ts(): # return timestamp
	return '[' + str(datetime.now()) + ']'

def retr(ftp_connection, path, retry=3): # retrieve file via FTP and return
	tmp = TemporaryFile()
	try:
		ftp_connection.retrbinary('RETR ' + path, tmp.write)
	except:
		if retry > 0:
			tmp.close()
			return retr(ftp_connection, path, retry-1) # recursively call retr until retry is 0 (retry times)
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
