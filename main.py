

from lib.db_lib import AddPost, AddAddress, AddImg, GetCommunity, GetCity, GetCountry, AddCommunity, CloseConnect, Connect
from lib.parspost_lib import WallItemSearch, AddressFromDescription
from lib.cfg import *

if __name__ == "__main__":

	Connect(
		host=post_library_host, 
		user=post_library_user, 
		password=, 
		db=GetParam('post_library_db'))

	
	AddCommunity(
		countryTitle='Россия', 
		cityTitle='Красноярск', 
		communityURL='https://m.vk.com/public9751268')

	AddCommunity(
		countryTitle='Россия', 
		cityTitle='Красноярск', 
		communityURL='https://m.vk.com/public123114913')
	
	AddCommunity(
		countryTitle='Россия', 
		cityTitle='Красноярск', 
		communityURL='https://m.vk.com/public105543780')
	
	AddCommunity(
		countryTitle='Россия', 
		cityTitle='Красноярск',
		communityURL='https://m.vk.com/public76867861')
	
	AddCommunity(
		countryTitle='Россия', 
		cityTitle='Красноярск', 
		communityURL='https://m.vk.com/public80318218')
	
	
	for i in range(0,1):
		for community in GetCommunity():
			print(i, 'community -',community['url'])

			city = GetCity(uuid=community['uuid_city']) 
			country = GetCountry(uuid=city['uuid_country'])

			for wall_item in WallItemSearch(country=country['title'], city=city['title'], url_group=community['url'],offset=i*5):

				post = AddPost(
					wall_item['link_community'],
					wall_item['description'], 
					wall_item['date'], 
					wall_item['price'], 
					wall_item['link'], 
					wall_item['telephones'])

				print(i,'post uuid:',post['uuid'],wall_item['img_urls'])
				
				if post['status'] == 2:
					
					for url in wall_item['img_urls']:
						AddImg(
							uuid_post=post['uuid'],
							_img_url=url)

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