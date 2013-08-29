from utils import *
from parse import *

def insert_notifications(file_names, db, ftp, region):
	for file_name in file_names:
		print(ts(), file_name)
		try:	
			zip_file = retr(ftp, file_name, retry=5)
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
		rows = []
		for event, xml in etree.iterparse(xml_file, tag='{http://zakupki.gov.ru/oos/export/1}*'):
			if event == 'end' and xml.tag != '{http://zakupki.gov.ru/oos/export/1}export':
				rows.append(parse_notification(xml) + (region,))
				xml.clear()
		zip_file.close()
		xml_file.close()
		if len(rows) > 0:
			try:
				cur = db.cursor()
				query = cur.mogrify('insert into notifications (rec_id, notification_number, notification_type, version_number, create_date, publish_date, placer_reg_num, order_name, href, print_form, max_price, folder_name)\nvalues ' + ',\n'.join(['%s'] * len(rows)), rows)
				cur.execute(query)
				db.commit()
				cur.close()
			except KeyboardInterrupt:
				traceback.print_exc()
				exit()
			except AttributeError:
				traceback.print_exc()
				exit()
			except:
				traceback.print_exc()
				continue