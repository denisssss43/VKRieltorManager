import sys
sys.path.append('.')

from vk_parser.lib.cfg.cfg import *
from vk_parser.lib.post_parser import *
from vk_parser.lib.db_post import *



def __addCommunities(connection):
	if connection != None:
		AddCommunity(
			connector,
			countryTitle='Россия', 
			cityTitle='Красноярск', 
			communityURL='https://m.vk.com/public9751268')
		AddCommunity(
			connector,
			countryTitle='Россия', 
			cityTitle='Красноярск', 
			communityURL='https://m.vk.com/public123114913')
		AddCommunity(
			connector,
			countryTitle='Россия', 
			cityTitle='Красноярск', 
			communityURL='https://m.vk.com/public105543780')
		AddCommunity(
			connector,
			countryTitle='Россия', 
			cityTitle='Красноярск',
			communityURL='https://m.vk.com/public76867861')
		AddCommunity(
			connector,
			countryTitle='Россия', 
			cityTitle='Красноярск', 
			communityURL='https://m.vk.com/public80318218')
	pass
def __searchPosts(connection):
	if connection != None:
		for i in range(0,5):
			for community in GetCommunity():
				print(i, 'community -',community['url'])

				if community == None: continue
				city = GetCity(uuid=community['uuid_city'])

				if city == None: continue
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

	pass


if __name__ == "__main__":

	connector = Connect()

	__addCommunities(connector)

	# __searchPosts(connector)

	CloseConnect(connector)