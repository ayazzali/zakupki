from utils import *

def extract(ftp, f):
	print ts(), f
	try:	
		zip_file = retr(ftp, f)
		xml_file = unzip(zip_file)
	except KeyboardInterrupt:
		traceback.print_exc()
		exit()
	except AttributeError:
		traceback.print_exc()
		exit()
	except:
		traceback.print_exc()
		continue
	return xml_file