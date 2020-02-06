

from lib.db_lib import AddPost, AddAddress, GetCommunity, GetCity, GetCountry, AddCommunity, CloseConnect, Connect
from lib.parspost_lib import WallItemSearch, AddressFromDescription


if __name__ == "__main__":
	Connect()
	
	AddCommunity(countryTitle='Россия', cityTitle='Красноярск', communityURL='https://m.vk.com/public9751268')
	AddCommunity(countryTitle='Россия', cityTitle='Красноярск', communityURL='https://m.vk.com/public123114913')
	AddCommunity(countryTitle='Россия', cityTitle='Красноярск', communityURL='https://m.vk.com/public105543780')
	AddCommunity(countryTitle='Россия', cityTitle='Красноярск', communityURL='https://m.vk.com/public76867861')
	AddCommunity(countryTitle='Россия', cityTitle='Красноярск', communityURL='https://m.vk.com/public80318218')
	
	for i in range(18,500):
		for community in GetCommunity():

			city = GetCity(uuid=community['uuid_city']) 
			country = GetCountry(uuid=city['uuid_country'])

			for wall_item in WallItemSearch(country=country['title'], city=city['title'], url_group=community['url'],offset=i*5):
				print(i,end=': ')
				post = AddPost(
					wall_item['link_community'],
					wall_item['description'], 
					wall_item['date'], 
					wall_item['price'], 
					wall_item['link'], 
					wall_item['telephones'])

				if post['status'] == 2:
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