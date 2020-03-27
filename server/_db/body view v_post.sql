SELECT 
	post.uuid,
    
    city.uuid_country, 
    country.title AS title_country, 
    
    address.uuid_city, 
    city.title AS title_city, 
    
    post.uuid_address, 
    address.title AS title_address, 
    
    (SELECT url FROM post_library.img WHERE uuid = (SELECT uuid_img FROM post_library.img__post WHERE uuid_post = post.uuid LIMIT 1)) AS url_img
    
FROM post_library.post
INNER JOIN post_library.address ON post.uuid_address = address.uuid
INNER JOIN post_library.city ON address.uuid_city = city.uuid
INNER JOIN post_library.country ON city.uuid_country = country.uuid
