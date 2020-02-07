

from lib.db_lib import AddPost, AddAddress, AddImg, GetCommunity, GetCity, GetCountry, AddCommunity, CloseConnect, Connect
from lib.parspost_lib import WallItemSearch, AddressFromDescription
from lib.cfg_lib import GetParamm


if __name__ == "__main__":
	Connect(host=GetParamm('host'), user=GetParamm('user'), password=GetParamm('password'), db=GetParamm('db'))
	
	AddCommunity(countryTitle='Россия', cityTitle='Красноярск', communityURL='https://m.vk.com/public9751268')
	AddCommunity(countryTitle='Россия', cityTitle='Красноярск', communityURL='https://m.vk.com/public123114913')
	AddCommunity(countryTitle='Россия', cityTitle='Красноярск', communityURL='https://m.vk.com/public105543780')
	AddCommunity(countryTitle='Россия', cityTitle='Красноярск', communityURL='https://m.vk.com/public76867861')
	AddCommunity(countryTitle='Россия', cityTitle='Красноярск', communityURL='https://m.vk.com/public80318218')
	
	print ('start')
	for i in range(0,1):
		for community in GetCommunity():
			print(i,community['url'] )

			city = GetCity(uuid=community['uuid_city']) 
			country = GetCountry(uuid=city['uuid_country'])

			for wall_item in WallItemSearch(country=country['title'], city=city['title'], url_group=community['url'],offset=i*5):
#				print(wall_item['date'], wall_item['link_community'])


				post = AddPost(
					wall_item['link_community'],
					wall_item['description'], 
					wall_item['date'], 
					wall_item['price'], 
					wall_item['link'], 
					wall_item['telephones'])

				print(i,post['uuid'] ) # ,end=': ')
				
				if post['status'] == 2:
					
					for url in post['uuid']:
						AddImg(
							uuid_post=post['uuid'],
							_img_url=wall_item['img_urls'])

					address = AddressFromDescription(
						description=wall_item['description'], 
						country=country['title'], 
						city=city['title'])
					AddAddress(
						uuid_post=post['uuid'], 
						countryTitle=country['title'], 
						cityTitle=city['title'], 
						addressTitle=address['address'], 
						latitude=address['latitude'], 
						longitude=address['longitude'])

	CloseConnect()