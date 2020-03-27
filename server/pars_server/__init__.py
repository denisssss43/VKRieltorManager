import server._lib.db_post as db_post
import server._lib.post_parser as post_parser
import threading

class ParserAsync(threading.Thread):
	def __init__(self): 
		super(ParserAsync, self).__init__(name="Parser", daemon=True)

	def __addCommunities(self):
		# print('__addCommunities')

		if self.connector != None:
			db_post.AddCommunity(
				self.connector,
				countryTitle='Россия', 
				cityTitle='Красноярск', 
				communityURL='https://m.vk.com/public9751268')
			db_post.AddCommunity(
				self.connector,
				countryTitle='Россия', 
				cityTitle='Красноярск', 
				communityURL='https://m.vk.com/public123114913')
			db_post.AddCommunity(
				self.connector,
				countryTitle='Россия', 
				cityTitle='Красноярск', 
				communityURL='https://m.vk.com/public105543780')
			db_post.AddCommunity(
				self.connector,
				countryTitle='Россия', 
				cityTitle='Красноярск',
				communityURL='https://m.vk.com/public76867861')
			db_post.AddCommunity(
				self.connector,
				countryTitle='Россия', 
				cityTitle='Красноярск', 
				communityURL='https://m.vk.com/public80318218')

	def __searchPosts(self):
		# print('__searchPosts')

		if self.connector != None:
			while True:
				for community in db_post.GetCommunity(self.connector):
					if community == None: continue
					
					city = db_post.GetCity(self.connector, uuid=community['uuid_city'])
					country = db_post.GetCountry(self.connector, uuid=city['uuid_country'])

					if city == None or country == None: continue

					for	i in range(20):

						for wall_item in post_parser.WallItemSearch(country=country['title'], city=city['title'], url_group=community['url'],offset=i*5):
							if wall_item['description'] == '': continue
							if wall_item['price'] < 3000.0: continue
							if len(wall_item['img_urls']) < 1: continue
							if len(wall_item['telephones']) < 1: continue

							post = db_post.AddPost(
								self.connector, 
								wall_item['link_community'],
								wall_item['description'], 
								wall_item['date'], 
								wall_item['price'], 
								wall_item['link'], 
								wall_item['telephones'])						

							if post['status'] == 2:
								
								for url in wall_item['img_urls']:
									db_post.AddImg(
										self.connector, 
										uuid_post=post['uuid'],
										_img_url=url)

								address = post_parser.AddressFromDescription( 
									description=wall_item['description'], 
									country=country['title'], 
									city=city['title'])

								db_post.AddAddress(
									self.connector, 
									uuid_post=post['uuid'], 
									countryTitle=country['title'], 
									cityTitle=city['title'], 
									addressTitle=address['address'], 
									latitude=address['latitude'], 
									longitude=address['longitude'])

	def run(self):
		# print('run Parser')

		self.connector = db_post.Connect()

		# self.__addCommunities()

		self.__searchPosts()

		db_post.CloseConnect(self.connector)