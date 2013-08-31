from utils import *
from parse import *

def insert_notifications(file_names, db, ftp, region):
	for file_name in file_names:
		print(ts(), file_name)
		try:	
			zip_file = retr(ftp, file_name, retry=5)
			xml_file = unzip(zip_file)
			print(str(float(unzipped[1]) / 1024) + ' kB')
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
				tuples = ',\n'.join(['%s'] * len(rows))
				query = cur.mogrify('insert into notifications (rec_id, notification_number, notification_type, version_number, create_date, publish_date, placer_reg_num, order_name, href, print_form, max_price, folder_name)\nvalues {tuples}'.format(tuples=tuples), rows)
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

def insert_organizations(file_names, db, ftp):
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
		for event, xml in etree.iterparse(xml_file, tag='{http://zakupki.gov.ru/oos/types/1}organization'):
			if event == 'end':
				rows.append(parse_organization(xml))
				xml.clear()
		zip_file.close()
		xml_file.close()
		if len(rows) > 0:
			try:
				cur = db.cursor()
				tuples = ','.join(['%s'] * len(rows))
				query = cur.mogrify('''					
					select * into temp new from organizations limit(0);
					insert into new values {tuples};
					with upsert as (
						update organizations o
						set (reg_num, short_name, full_name, okato, zip, postal_address, email, phone, fax, last_name, first_name, middle_name, inn, actual)
							 = (n.reg_num, n.short_name, n.full_name, n.okato, n.zip, n.postal_address, n.email, n.phone, n.fax, n.last_name, n.first_name, n.middle_name, n.inn, n.actual)
						from new n
						where o.reg_num = n.reg_num
						returning n.*
					)
					insert into organizations
					select reg_num, short_name, full_name, okato, zip, postal_address, email, phone, fax, last_name, first_name, middle_name, inn, actual from new 
					except
					select reg_num, short_name, full_name, okato, zip, postal_address, email, phone, fax, last_name, first_name, middle_name, inn, actual from upsert;
					drop table new;
					'''.format(tuples=tuples), rows)
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
				