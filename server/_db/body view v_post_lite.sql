SELECT 
	post.description,
	post.price,
    
    (SELECT number FROM post_library.telephone WHERE uuid = (SELECT uuid_telephone FROM post_library.telephone__post WHERE uuid_post = post.uuid LIMIT 1)) AS url_img,
	
    country.title AS title_country, 
    
    city.title AS title_city, 
    
    address.title AS title_address, 
    address.latitude, 
    address.longitude, 
    
    (SELECT url FROM post_library.img WHERE uuid = (SELECT uuid_img FROM post_library.img__post WHERE uuid_post = post.uuid LIMIT 1)) AS url_img
    
FROM post_library.post
INNER JOIN post_library.address ON post.uuid_address = address.uuid
INNER JOIN post_library.city ON address.uuid_city = city.uuid
INNER JOIN post_library.country ON city.uuid_country = country.uuid
