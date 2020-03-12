import db_main as db
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import copy 

if __name__ == "__main__":
	

    # Тел.: 
    # Адрес:
    # Стоимость: 
    # Ссылка:
    # Описание:  dateTime

	t = datetime.datetime(year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day) 

	while(True):
		try:
			db.Connect()
			smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
			smtpObj.starttls()
			smtpObj.login('deniskarasev43@gmail.com','MnM32RtQt')

			print (datetime.datetime.now(), 'Connect')
			with db.connection.cursor() as cursor:
				cursor.execute("SELECT * FROM dbo.v_post WHERE dateTime > '"+str(t)+"' LIMIT 10;")
				posts = copy.deepcopy(cursor.fetchall())

				for row in posts[::-1]:
					string = ''

					cursor.execute("call dbo.post_telephones('"+row['uuid_post']+"');")
					telephones = copy.deepcopy(cursor.fetchall())
					
					string += '\nСтоимость: '+str(int(row['price']))
					string += '\nАдрес: '+str(row['address'])
					string += '\nНа карте: ' +'https://www.google.com/maps/place/'+str(row['address']).replace(' ', '+')
					# string += '\n<a href="'+'https://www.google.com/maps/place/'+str(row['address']).replace(' ', '+')+'">Показать на карте</a>'
					string += '\nДо работы (Вавилова 1 строение 39): '+str(db.TimeToPoint('Вавилова 1 строение 39',row['address'])) + ' мин.'
					# string += '\nСсылка: <a href="'+str(row['link'])+'">пост источника</a>'
					string += '\nИсточника: '+str(row['link'])
					
					string += '\n'
					string += 'Тел.: '
					for telephone in telephones:
						string += str(telephone['telephone']) + ' ' 

					string += '\n\nОписание: '+str(row['description'])

					t = row['dateTime']

					msg = MIMEMultipart()
					msg['From'] = "deniskarasev43@gmail.com"
					msg['To'] = "karasev.bpi1701@gmail.com"
					msg['Subject'] = "Подбор аренды жилья"
					msg.attach(MIMEText(string, 'plain'))

					if (string != ''): 
						print(msg.as_string())
						smtpObj.sendmail(msg['From'], msg['To'], msg.as_string())
			
			db.CloseConnect()
			smtpObj.quit()
			# print ('CloseConnect\n-------------\n')
		except: # expression as identifier: 
			# print (expression)
			# break
			pass
		time.sleep(5)