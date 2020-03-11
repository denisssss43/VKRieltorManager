import db_main as db
import datetime

if __name__ == "__main__":
	print (datetime.datetime.now(), 'Connect')
	while(True):
		try:
			db.Connect()
			with db.connection.cursor() as cursor:
				cursor.execute("SELECT * FROM `dbo`.`v_post_description_address_null` LIMIT 1;")
				row = cursor.fetchone()
				while row:
					print(datetime.datetime.now(), row['uuid'], end=' ')
					cursor.execute(db.AddAddress(uuid_post=row['uuid'], address=db.AddressFromDescription(row['description'], country='Россия', city='Красноярск'), city='Красноярск'))
					db.connection.commit()
					print('готово')
					cursor.execute("SELECT * FROM `dbo`.`v_post_description_address_null` LIMIT 1;")
					row = cursor.fetchone()
			db.CloseConnect()
		except: pass
	print ('CloseConnect')