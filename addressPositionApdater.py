import db_main as db
import datetime
import copy 
import time

if __name__ == "__main__":
	while(True):
		try:
			print (datetime.datetime.now(), 'Connect')
			db.Connect()
			with db.connection.cursor() as cursor:
				cursor.execute("SELECT * FROM dbo.address WHERE latitude is null and longitude is null LIMIT 1;")
				adress = copy.deepcopy(cursor.fetchone())
				print(adress)
				if (adress != None):
					position = db.AddressPosition(adress['title'])

					cursor.execute("call dbo.add_address_position('"+adress['uuid']+"', "+position['latitude']+", "+position['longitude']+");")
					db.connection.commit()

					print(adress, position)
					db.CloseConnect()
				else:
					db.CloseConnect()
					time.sleep(10)
			print ('	CloseConnect')
		except expression as identifier:
			pass

'''
# importing the requests library 
import requests 
  
# api-endpoint 
URL = "http://maps.googleapis.com/maps/api/geocode/json"
  
# location given here 
location = "delhi technological university"
  
# defining a params dict for the parameters to be sent to the API 
PARAMS = {'address':location} 
  
# sending get request and saving the response as response object 
r = requests.get(url = URL, params = PARAMS) 
  
# extracting data in json format 
data = r.json() 
  
  
# extracting latitude, longitude and formatted address  
# of the first matching location 
latitude = data['results'][0]['geometry']['location']['lat'] 
longitude = data['results'][0]['geometry']['location']['lng'] 
formatted_address = data['results'][0]['formatted_address'] 
  
# printing the output 
print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
      %(latitude, longitude,formatted_address)) 
'''