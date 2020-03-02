/* Файл вторичной настройки БД и ее структуры */

# Создание хранимых процедур

# Указание субд работать со схемой библиотеки постов
USE `post_library`; 

DELIMITER $$
# DROP PROCEDURE IF EXISTS sp_addPost;
CREATE PROCEDURE sp_addPost( /* Процедура добавления сырого (Без адреса) поста в БД */
	_communityURL NVARCHAR(256), /* Ноименование сообщество в котором был найден пост */
	_description NVARCHAR(1024), /* Полное описание, указанное в посте (от редактированное) */
	_datetime DATETIME, /* Дата публикации записи */
	_price float, /* Цена предложения указанного в посте */
	_url NVARCHAR(256)) /* URL-ссылка на пост */
BEGIN
	DECLARE _uuid_post nvarchar(36); /* Переменная для хранения uuid поста */
	DECLARE _uuid_url nvarchar(36); /* Переменная для хранения uuid url-ссылки */
	DECLARE _uuid_community nvarchar(36); /* Переменная для хранения uuid сообщества */
	DECLARE _status int; /* Переменная статуса изменяемого поста */


	SET _uuid_post = ( /* Получение uuid для запиcи объявление */
		SELECT `post`.`uuid` 
		FROM `post` 
		WHERE `post`.`description` LIKE _description 
		OR _description LIKE `post`.`description`
		LIMIT 1);

	SET _status = (SELECT `status` FROM `post` WHERE `uuid` = _uuid_post); /* Указание статуса корректного поста */

	IF _price <= 0 THEN
		SET _status = 0;
	END IF;
		
	IF _uuid_post IS NULL THEN /* Если запись не создана ранее */
		SET _uuid_post = UUID(); /* Генерация нового uuid для поста */
		INSERT INTO `post` ( /* Добавление поста */
			`uuid`, 
			`description`,
			`price`, 
			`status`, 
			`uuid_address`)
		VALUES (
			_uuid_post, 
			_description, 
			_price, 
			_status, 
			NULL);	
	END IF;

	IF _status <> 1 AND _status <> 0 OR _status IS NULL THEN
		SET _status = 2;
		UPDATE `post` /* Обновление статуса для добавления телефонного номера */
		SET `status` = _status
		WHERE `uuid` = _uuid_post;
	END IF;

	SET _uuid_community = ( /* Получение uuid записи сообщества */
		SELECT `community`.`uuid` 
		FROM `community` 
		WHERE `community`.`url` = _communityURL);

	SET _uuid_url = ( /* Получение uuid записи url-адреса */
		SELECT `link`.`uuid` 
		FROM `link` 
		WHERE `link`.`url` = _url);

	IF _uuid_url IS NULL THEN /* Если запись не создана ранее */
		SET _uuid_url = UUID(); /* Генерация uuid для новой записи url-адреса */
		INSERT INTO `link` (
			`uuid`, 
			`url`,
			`datetime`, 
			`uuid_community`, 
			`uuid_post`)
		VALUES (
			_uuid_url, 
			_url, 
			_datetime, 
			_uuid_community, 
			_uuid_post);
	END IF;

	SELECT _uuid_post AS uuid, _status AS status; /* Возврат uuid поста */
END$$

DELIMITER $$
# DROP PROCEDURE IF EXISTS sp_addTelephone;
CREATE PROCEDURE sp_addTelephone( /* Процедура добавления телефонного номера */
	_uuid_post nvarchar(36), /* uuid поста к которому будет прикреплен номер телефона */
	_telephone nvarchar(16)) /* номер телефона */
BEGIN
	DECLARE _uuid_telephone nvarchar(36); /* Переменная для хранения uuid телефона */
	DECLARE _is_telephone__post TINYINT(1); /* Существует ли связь для текущего телефона и поста */
	
	SET _uuid_telephone = ( /* Получение uuid записи телефонного номера */
		SELECT `telephone`.`uuid` 
		FROM `telephone` 
		WHERE `telephone`.`number` LIKE _telephone);
	
	IF _uuid_telephone IS NULL THEN	/* Если телефонный номер не был добавлен */
		SET _uuid_telephone = UUID(); /* Генерация uuid для записи телефонного номера */
		INSERT INTO `telephone` ( /* Добавление записи телефонного номера */
			`uuid`, 
			`number`) 
		VALUES (
			_uuid_telephone, 
			_telephone);
	END IF;	
	
	SET _is_telephone__post = ( /* Проверка наличия свизи добавляемого телефона и объявления */
		SELECT COUNT(*) 
		FROM `telephone__post` 
		WHERE `telephone__post`.`uuid_telephone` LIKE _uuid_telephone
		AND `telephone__post`.`uuid_post` LIKE _uuid_post
		LIMIT 1);

	IF _is_telephone__post = 0 THEN /* Если связь отсутствует */
		INSERT INTO `telephone__post` ( /* Добавление связи телефонного номера с постом */
			`uuid_telephone`, 
			`uuid_post`)
        VALUES (
			_uuid_telephone, 
			_uuid_post);
	END IF;	
END$$

DELIMITER $$
# DROP PROCEDURE IF EXISTS sp_addAddress;
CREATE PROCEDURE sp_addAddress( /* Процедура добавления адреса */
	_uuid_post nvarchar(36), /* uuid поста к которому будет прикреплен адрес */
	_countryTitle nvarchar(144), /* Наименование страны в которой актуален этот пост */
	_cityTitle nvarchar(144), /* Наименование города в котором актуален этот пост */
	_addressTitle NVARCHAR(128), /* Географический адресс, указанный в посте */
	_latitude FLOAT, /* Широта */
	_longitude FLOAT) /* Долгота */
BEGIN
	DECLARE _uuid_country nvarchar(36); /* Переменная для хранения uuid страны */
	DECLARE _uuid_city nvarchar(36); /* Переменная для хранения uuid города */
	DECLARE _uuid_address nvarchar(36); /* Переменная для хранения uuid географического адреса */
	DECLARE _status int; /* Переменная статуса изменяемого поста */

	SET _status = 1; /* Указание статуса корректного поста */

	IF _addressTitle IS NULL THEN /* Если адрес не был указан */
		SET _status = 0; /* Указание статуса некорректного поста */
	END IF;
	
	SET _uuid_country = ( /* Получение uuid для запиcи города */
		SELECT `country`.`uuid` 
		FROM `country`
		WHERE `country`.`title` = _countryTitle
		LIMIT 1);
	IF _uuid_country IS NULL THEN /* Если страна не была ранее добавлена */
		IF _countryTitle IS NOT NULL THEN /* Если передано наименование страны */
			SET _uuid_country = UUID(); /* Генерация нового uuid для записи города */
			INSERT INTO `country` ( /* Добавление записи города */
				`uuid`, 
				`title`)
			VALUES (
				_uuid_country, 
				_countryTitle);
		END IF;
	END IF;
	    
	SET _uuid_city = ( /* Получение uuid для запиcи города */
		SELECT `city`.`uuid` 
		FROM `city`
		WHERE `city`.`title` = _cityTitle
		LIMIT 1);
	IF _uuid_city IS NULL THEN /* Если город не был ранее добавлен */
		IF _cityTitle IS NOT NULL THEN /* Если передано наименование города */
			SET _uuid_city = UUID(); /* Генерация нового uuid для записи города */
			INSERT INTO `city` ( /* Добавление записи города */
				`uuid`,
				`uuid_country`, 
				`title`)
			VALUES (
				_uuid_city,
				_uuid_country, 
				_cityTitle);
		END IF;
	END IF;
	
	SET _uuid_address = ( /* Получение uuid для запиcи адреcа */
		SELECT `address`.`uuid` 
		FROM `address` 
		WHERE `address`.`title` = _addressTitle
		LIMIT 1);
	IF _uuid_address IS NULL THEN /* Если адрес не был ранее добавлен */
		IF _addressTitle IS NOT NULL THEN /* Если переданно текстовое представление адреса */
			SET _uuid_address = UUID(); /* Генерация нового uuid для */
			INSERT INTO `address` (
				`uuid`, 
				`title`,
				`uuid_city`,
				`latitude`,
				`longitude`) 
			VALUES (
				_uuid_address, 
				_addressTitle, 
				_uuid_city, 
				_latitude, 
				_longitude);
		END IF;
	END IF;
	
	UPDATE `post`
	SET `uuid_address` = _uuid_address, `status` = _status
	WHERE `uuid` = _uuid_post;
END$$

DELIMITER $$
# DROP PROCEDURE IF EXISTS sp_addImg;
CREATE PROCEDURE sp_addImg( /* Процедура добавления изображений */
	_uuid_post nvarchar(36), /* uuid поста к которому будет прикреплен номер телефона */
	_img_url nvarchar(256)) /* URL-ссылка на изображение */
BEGIN
	DECLARE _uuid_img nvarchar(36); /* Переменная для хранения uuid телефона */
	DECLARE _is_img__post TINYINT(1); /* Существует ли связь для текущего телефона и поста */

	SET _uuid_img = ( /* Получение uuid записи URL-ссылки на изображение */
		SELECT `img`.`uuid` 
		FROM `img` 
		WHERE `img`.`url` LIKE _img_url
		LIMIT 1);
	
	IF _uuid_img IS NULL THEN	/* Если URL-ссылка на изображение не была добавлена */
		SET _uuid_img = UUID(); /* Генерация uuid для записи URL-ссылки на изображение */
		INSERT INTO `img` ( /* Добавление записи URL-ссылки на изображение */
			`uuid`, 
			`url`) 
		VALUES (
			_uuid_img, 
			_img_url);
	END IF;	
	
	SET _is_img__post = ( /* Проверка наличия свизи добавляемой изображения и объявления */
		SELECT COUNT(*) 
		FROM `img__post` 
		WHERE `img__post`.`uuid_img` LIKE _uuid_img
		AND `img__post`.`uuid_post` LIKE _uuid_post
		LIMIT 1);

	IF _is_img__post = 0 THEN /* Если связь отсутствует */
		INSERT INTO `img__post` ( /* Добавление связи изображений с постом */
			`uuid_img`, 
			`uuid_post`)
        VALUES (
			_uuid_img, 
			_uuid_post);
	END IF;	
END$$

DELIMITER $$
# DROP PROCEDURE IF EXISTS sp_addCommunity;
CREATE PROCEDURE sp_addCommunity( /* Процедура добавления группы */
	_countryTitle nvarchar(144), /* Наименование страны */
	_cityTitle nvarchar(144), /* Наименование города */
	_communityURL NVARCHAR(256)) /* Ссылка на сообщество */
BEGIN
	DECLARE _uuid_country nvarchar(36); /* Переменная для хранения uuid страны */
	DECLARE _uuid_city nvarchar(36); /* Переменная для хранения uuid города */
	DECLARE _uuid_community nvarchar(36); /* Переменная для хранения uuid сообщества */
	
	SET _uuid_country = ( /* Получение uuid для запиcи города */
		SELECT `country`.`uuid` 
		FROM `country`
		WHERE `country`.`title` = _countryTitle
		LIMIT 1);
	IF _uuid_country IS NULL THEN /* Если страна не была ранее добавлена */
		IF _countryTitle IS NOT NULL THEN /* Если передано наименование страны */
			SET _uuid_country = UUID(); /* Генерация нового uuid для записи города */
			INSERT INTO `country` ( /* Добавление записи города */
				`uuid`, 
				`title`)
			VALUES (
				_uuid_country, 
				_countryTitle);
		END IF;
	END IF;
	    
	SET _uuid_city = ( /* Получение uuid для запиcи города */
		SELECT `city`.`uuid` 
		FROM `city`
		WHERE `city`.`title` = _cityTitle
		LIMIT 1);
	IF _uuid_city IS NULL THEN /* Если город не был ранее добавлен */
		IF _cityTitle IS NOT NULL THEN /* Если передано наименование города */
			SET _uuid_city = UUID(); /* Генерация нового uuid для записи города */
			INSERT INTO `city` ( /* Добавление записи города */
				`uuid`,
				`uuid_country`, 
				`title`)
			VALUES (
				_uuid_city,
				_uuid_country, 
				_cityTitle);
		END IF;
	END IF;

	SET _uuid_community = ( /* Получение uuid записи сообщества */
		SELECT `community`.`uuid` 
		FROM `community` 
		WHERE `community`.`url` = _communityURL);

	IF _uuid_community IS NULL THEN /* Если запись не создана ранее */
		SET _uuid_community = UUID(); /* Генерация ного uuid для записи сообщества */
		INSERT INTO `community` ( /* Добавление записи сообщества */
			`uuid`, 
			`uuid_city`, 
			`url`)
		VALUES (
			_uuid_community, 
			_uuid_city, 
			_communityURL);
	END IF;

	SELECT _uuid_community AS uuid;
END$$


# Создание функций

# Указание субд работать со схемой библиотеки постов
USE `post_library`; 

DELIMITER $$
# DROP FUNCTION IF EXISTS f_address_uuidToText;
CREATE FUNCTION f_address_uuidToText( /* Функция конвертации uuid адреса в текстовое представление */
	_uuid_address NVARCHAR(36)) /* Параметр uuid адреса */
	RETURNS NVARCHAR(128) /* Тип возвращаемых данных */
BEGIN
	RETURN (
		SELECT `title` 
		FROM `address` 
		WHERE `address`.`uuid` LIKE _uuid_address
		LIMIT 1);
END$$

DELIMITER $$
# DROP FUNCTION IF EXISTS f_lastestPostDateTime;
CREATE FUNCTION f_lastestPostDateTime( /* Функция поиска последней даты для поста */
	_uuid_post NVARCHAR(36)) /* Параметр uuid поста */
	RETURNS datetime /* Тип возвращаемых данных */
BEGIN
	RETURN (
		SELECT `datetime` 
		FROM `link` 
		WHERE `link`.`uuid_post` LIKE _uuid_post 
		ORDER BY `datetime` DESC 
		LIMIT 1);
END$$

DELIMITER $$
# DROP FUNCTION IF EXISTS f_lastestPostURL;
CREATE FUNCTION f_lastestPostURL( /* Функция поиска последней url-ссылки для поста */
	_uuid_post NVARCHAR(36)) /* Параметр uuid поста */
	RETURNS NVARCHAR(256) /* Тип возвращаемых данных */
BEGIN
	RETURN (
		SELECT `url` 
		FROM `link` 
		WHERE `link`.`uuid_post` LIKE _uuid_post 
		ORDER BY `datetime` DESC 
		LIMIT 1);
END$$

DELIMITER $$
# DROP FUNCTION IF EXISTS f_URLToPostUUID;
CREATE FUNCTION f_URLToPostUUID( /* Функция поиска последней url-ссылки для поста */
	_url NVARCHAR(256)) /* Параметр uuid поста */
	RETURNS NVARCHAR(36) /* Тип возвращаемых данных */
BEGIN
	RETURN (
		SELECT `uuid_post` 
		FROM `link` 
		WHERE `link`.`url` LIKE _url 
		LIMIT 1);
END$$

DELIMITER $$
# DROP FUNCTION IF EXISTS f_distance_between_addresses;
CREATE FUNCTION f_distance_between_addresses( /* Функция определения расстояния между двумя адресами */
	_uuid_address_from NVARCHAR(36), /* Параметр uuid начального адреса */
	_uuid_address_to NVARCHAR(36)) /* Параметр uuid конечного адреса */
	RETURNS FLOAT
BEGIN
	DECLARE _w_from FLOAT; /* Переменная для широты начального адреса */
	DECLARE _v_from FLOAT; /* Переменная для долготы начального адреса */
	
	DECLARE _w_to FLOAT; /* Переменная для широты конечного адреса */
	DECLARE _v_to FLOAT; /* Переменная для долготы конечного адреса */

	/* Получение радиан */
	SET _w_from = (
		SELECT `address`.`latitude` 
		FROM `address` 
		WHERE `address`.`uuid` = _uuid_address_from 
		LIMIT 1) * PI() / 180;
	SET _v_from = (
		SELECT `address`.`longitude` 
		FROM `address` 
		WHERE `address`.`uuid` = _uuid_address_from 
		LIMIT 1) * PI() / 180;
	SET _w_to = (
		SELECT `address`.`latitude` 
		FROM `address` 
		WHERE `address`.`uuid` = _uuid_address_to 
		LIMIT 1) * PI() / 180;
	SET _v_to = (
		SELECT `address`.`longitude` 
		FROM `address` 
		WHERE `address`.`uuid` = _uuid_address_to 
		LIMIT 1) * PI() / 180;

	/* Возврат расстояния */
	RETURN ACOS(SIN(_w_from)*SIN(_w_to) + COS(_w_from)*COS(_w_to)*COS(_w_to - _v_to));
END$$