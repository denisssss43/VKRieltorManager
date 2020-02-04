/* Файл вторичной настройки БД и ее структуры */

USE test; # Указание субд работать с определенной БД

# Создание хранимых процедур
DELIMITER $$
CREATE PROCEDURE sp_addPost( /* Процедура добавления сырого (Без адреса) поста в БД */
	_communityURL NVARCHAR(256), /* Ноименование сообщество в котором был найден пост */
	_description NVARCHAR(1024), /* Полное описание, указанное в посте (от редактированное) */
	_datetime DATETIME, /* Дата публикации записи */
	_price float, /* Цена предложения указанного в посте */
	_url NVARCHAR(256)) /* URL-ссылка на пост */
BEGIN
	declare _uuid_post nvarchar(36); /* Переменная для хранения uuid поста */
	declare _uuid_url nvarchar(36); /* Переменная для хранения uuid url-ссылки */
	declare _uuid_community nvarchar(36); /* Переменная для хранения uuid сообщества */

	set _uuid_post = ( /* Получение uuid для запиcи объявление */
		SELECT `post`.`uuid` 
		FROM `post` 
		WHERE `post`.`description` LIKE _description 
		OR _description LIKE `post`.`description`
		LIMIT 1);
		
	if _uuid_post IS NULL THEN /* Если запись не создана ранее */
		set _uuid_post = UUID(); /* Генерация нового uuid для поста */
		INSERT INTO `post` ( /* Добавление поста */
			`uuid`, 
			`description`,
			`price`, 
			`isHidden`, 
			`uuid_address`)
		VALUES (
			_uuid_post, 
			_description, 
			_price, 
			1, 
			NULL);	
	end if;

	set _uuid_community = ( /* Получение uuid записи сообщества */
		SELECT `community`.`uuid` 
		FROM `community` 
		WHERE `community`.`url` = _communityURL);

	if _uuid_community IS NULL THEN /* Если запись не создана ранее */
		set _uuid_community = UUID(); /* Генерация ного uuid для записи сообщества */
		INSERT INTO `community` ( /* Добавление записи сообщества */
			`uuid`, 
			`url`)
		VALUES (
			_uuid_community, 
			_communityURL);
	end if;

	set _uuid_url = ( /* Получение uuid записи url-адреса */
		SELECT `link`.`uuid` 
		FROM `link` 
		WHERE `link`.`url` = _url);

	if _uuid_url IS NULL THEN /* Если запись не создана ранее */
		set _uuid_url = UUID(); /* Генерация uuid для новой записи url-адреса */
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
			NULL);
	end if;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE sp_addTelephone( /* Процедура добавления телефонного номера */
	_uuid_post nvarchar(36), /* uuid поста к которому будет прикреплен номер телефона */
	_telephone nvarchar(16)) /* номер телефона */
BEGIN
	declare _uuid_telephone nvarchar(36); /* Переменная для хранения uuid телефона */
	declare _is_telephone__post TINYINT(1); /* Существует ли связь для текущего телефона и поста */
	
	set _uuid_telephone = ( /* Получение uuid записи телефонного номера */
		SELECT `telephone`.`uuid` 
		FROM `telephone` 
		WHERE `telephone`.`number` LIKE _telephone);
	
	IF _uuid_telephone IS NULL THEN	/* Если телефонный номер не был добавлен */
		set _uuid_telephone = UUID(); /* Генерация uuid для записи телефонного номера */
		INSERT INTO `telephone` ( /* Добавление записи телефонного номера */
			`uuid`, 
			`number`) 
		VALUES (
			_uuid_telephone, 
			_telephone);
	end IF;	
	
	set _is_telephone__post = ( /* Проверка наличия свизи добавляемого телефона и объявления */
		SELECT COUNT(*) 
		FROM `telephone__post` 
		WHERE `telephone__post`.`uuid_telephone` LIKE _uuid_telephone
		AND `telephone__post`.`uuid_post` LIKE _uuid_post
		LIMIT 1);

	IF _uuid_telephone__post = 0 THEN /* Если связь отсутствует */
		INSERT INTO `telephone__post` ( /* Добавление связи телефонного номера с постом */
			`uuid_telephone`, 
			`uuid_post`)
        VALUES (
			_uuid_telephone, 
			_uuid_post);
	end IF;	
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE sp_addAddress(
	_uuid_post nvarchar(36), /* uuid поста к которому будет прикреплен номер телефона */
	_countryTitle nvarchar(144), /* Наименование страны в которой актуален этот пост */
	_cityTitle nvarchar(144), /* Наименование города в котором актуален этот пост */
	_addressTitle NVARCHAR(128), /* Географический адресс, указанный в посте */
	_latitude FLOAT, /* Широта */
	_longitude FLOAT) /* Долгота */
BEGIN
	declare _uuid_country nvarchar(36); /* Переменная для хранения uuid страны */
	declare _uuid_city nvarchar(36); /* Переменная для хранения uuid города */
	declare _uuid_address nvarchar(36); /* Переменная для хранения uuid географического адреса */
	
	set _uuid_country = ( /* Получение uuid для запиcи города */
		SELECT `country`.`uuid` 
		FROM `country`
		WHERE `country`.`title` = _countryTitle
		LIMIT 1);
	IF _uuid_country IS NULL THEN /* Если страна не была ранее добавлена */
		IF _countryTitle IS NOT NULL THEN /* Если передано наименование страны */
			set _uuid_country = UUID(); /* Генерация нового uuid для записи города */
			INSERT INTO `country` ( /* Добавление записи города */
				`uuid`, 
				`title`)
			VALUES (
				_uuid_country, 
				_countryTitle);
		end if;
	end if;
	    
	set _uuid_city = ( /* Получение uuid для запиcи города */
		SELECT `city`.`uuid` 
		FROM `city`
		WHERE `city`.`title` = _cityTitle
		LIMIT 1);
	IF _uuid_city IS NULL THEN /* Если город не был ранее добавлен */
		IF _cityTitle IS NOT NULL THEN /* Если передано наименование города */
			set _uuid_city = UUID(); /* Генерация нового uuid для записи города */
			INSERT INTO `city` ( /* Добавление записи города */
				`uuid`,
				`uuid_country`, 
				`title`)
			VALUES (
				_uuid_city,
				_uuid_country, 
				_cityTitle);
		end if;
	end if;
	
	set _uuid_address = ( /* Получение uuid для запиcи адреcа */
		SELECT `address`.`uuid` 
		FROM `address` 
		WHERE `address`.`title` = _addressTitle
		LIMIT 1);
	IF _uuid_address IS NULL THEN /* Если адрес не был ранее добавлен */
		IF _addressTitle IS NOT NULL THEN /* Если переданно текстовое представление адреса */
			set _uuid_address = UUID(); /* Генерация нового uuid для */
			INSERT INTO `address` (
				`uuid`, 
				`title`,
				`uuid_city`) 
		VALUES (
				_uuid_address, 
				_addressTitle, 
				_uuid_city);
		end if;
	end if;
	
	UPDATE `post`
	SET `uuid_address` = _uuid_address
	WHERE `uuid` = _uuid_post;
END$$
DELIMITER ;

# Создание функций
DELIMITER $$
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
DELIMITER ;

DELIMITER $$
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
DELIMITER ;

DELIMITER $$
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
DELIMITER ;

DELIMITER $$
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
DELIMITER ;

DELIMITER $$
CREATE FUNCTION f_distance_between_addresses( /* Функция определения расстояния между двумя адресами */
	_uuid_address_from NVARCHAR(36), /* Параметр uuid начального адреса */
	_uuid_address_to NVARCHAR(36)) /* Параметр uuid конечного адреса */
	RETURNS FLOAT
BEGIN
	declare _w_from FLOAT; /* Переменная для широты начального адреса */
	declare _v_from FLOAT; /* Переменная для долготы начального адреса */
	
	declare _w_to FLOAT; /* Переменная для широты конечного адреса */
	declare _v_to FLOAT; /* Переменная для долготы конечного адреса */

	/* Получение радиан */
	set _w_from = (
		SELECT `address`.`latitude` 
		FROM `address` 
		WHERE `address`.`uuid` = _uuid_address_from 
		LIMIT 1) * PI() / 180;
	set _v_from = (
		SELECT `address`.`longitude` 
		FROM `address` 
		WHERE `address`.`uuid` = _uuid_address_from 
		LIMIT 1) * PI() / 180;
	set _w_to = (
		SELECT `address`.`latitude` 
		FROM `address` 
		WHERE `address`.`uuid` = _uuid_address_to 
		LIMIT 1) * PI() / 180;
	set _v_to = (
		SELECT `address`.`longitude` 
		FROM `address` 
		WHERE `address`.`uuid` = _uuid_address_to 
		LIMIT 1) * PI() / 180;

	/* Возврат расстояния */
	RETURN ACOS(SIN(_w_from)*SIN(_w_to) + COS(_w_from)*COS(_w_to)*COS(_w_to - _v_to));
END$$
DELIMITER ;