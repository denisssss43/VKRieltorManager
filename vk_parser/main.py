import sys
sys.path.append('.')

# print ('from vk_parser.lib.cfg.cfg import *')
# from vk_parser.lib.cfg.cfg import Config
import vk_parser.lib.db_post as db_post
import vk_parser.lib.post_parser as post_parser

def __addCommunities(connection):
	if connection != None:
		db_post.AddCommunity(
			connector,
			countryTitle='Россия', 
			cityTitle='Красноярск', 
			communityURL='https://m.vk.com/public9751268')
		db_post.AddCommunity(
			connector,
			countryTitle='Россия', 
			cityTitle='Красноярск', 
			communityURL='https://m.vk.com/public123114913')
		db_post.AddCommunity(
			connector,
			countryTitle='Россия', 
			cityTitle='Красноярск', 
			communityURL='https://m.vk.com/public105543780')
		db_post.AddCommunity(
			connector,
			countryTitle='Россия', 
			cityTitle='Красноярск',
			communityURL='https://m.vk.com/public76867861')
		db_post.AddCommunity(
			connector,
			countryTitle='Россия', 
			cityTitle='Красноярск', 
			communityURL='https://m.vk.com/public80318218')
	pass
def __searchPosts(connection):
	if connection != None:
		for i in range(0,5):
			for community in db_post.GetCommunity():
				print(i, 'community -',community['url'])

				if community == None: continue
				city = db_post.GetCity(uuid=community['uuid_city'])

				if city == None: continue
				country = db_post.GetCountry(uuid=city['uuid_country'])

				for wall_item in post_parser.WallItemSearch(country=country['title'], city=city['title'], url_group=community['url'],offset=i*5):

					post = db_post.AddPost(
						wall_item['link_community'],
						wall_item['description'], 
						wall_item['date'], 
						wall_item['price'], 
						wall_item['link'], 
						wall_item['telephones'])

					print(i,'post uuid:',post['uuid'],wall_item['img_urls'])
					
					if post['status'] == 2:
						
						for url in wall_item['img_urls']:
							db_post.AddImg(
								uuid_post=post['uuid'],
								_img_url=url)

						address = post_parser.AddressFromDescription(
							description=wall_item['description'], 
							country=country['title'], 
							city=city['title'])

						db_post.AddAddress(
							uuid_post=post['uuid'], 
							countryTitle=country['title'], 
							cityTitle=city['title'], 
							addressTitle=address['address'], 
							latitude=address['latitude'], 
							longitude=address['longitude'])

	pass


if __name__ == "__main__":
	
	connector = db_post.Connect()

	__addCommunities(connector)

	# __searchPosts(connector)

	db_post.CloseConnect(connector)