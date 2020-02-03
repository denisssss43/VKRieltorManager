-- Файл вторичной настройки БД и ее структуры

USE test; -- Указание субд работать с определенной БД

-- Создание хранимых процедур

CREATE PROCEDURE PROCEDURE `sp_addPost`( -- Процедура добавление сырого (Без адреса) поста в БД 
    `countryTitle` nvarchar(144), -- Наименование страны в которой актуален этот пост
    `cityTitle` nvarchar(144), -- Наименование города в котором актуален этот пост
	`url` NVARCHAR(256), -- URL-ссылка на пост
	`communityTitle` NVARCHAR(256), -- Ноименование сообщество в котором был найден пост
	`datetime` DATETIME,-- Дата публикации записи
    `description` NVARCHAR(512), -- Полное описание, указанное в посте (от редактированное)
    `price` float) -- Цена предложения указанного в посте

	-- NOTE: Так как функция предпологает сбор сырых данных (для ускорения сбора данных) этот параметр функции под вопросом
    -- address LONGTEXT, -- Географический адресс, указанный в посте 
BEGIN
	declare `_uuid_post` nvarchar(36); -- Переменная для хранения uuid поста
	declare `_uuid_country` nvarchar(36); -- Переменная для хранения uuid страны
	declare `_uuid_city` nvarchar(36); -- Переменная для хранения uuid города
	declare `_uuid_link` nvarchar(36); -- Переменная для хранения uuid url-ссылки
	declare `_uuid_community` nvarchar(36); -- Переменная для хранения uuid сообщества
	-- declare `_uuid_address` nvarchar(36); -- Переменная для хранения uuid географического адреса

    -- Получение uuid для запиcи объявление
    set `_uuid_post` = (
		SELECT `post`.`uuid` 
		FROM `post` 
        WHERE `post`.`description` LIKE `description` 
        OR `description` LIKE `post`.`description`
		LIMIT 1);

    if `_uuid_post` IS NULL THEN -- Если запись не создана ранее
		set `_uuid_post` = UUID(); -- Генерация нового uuid для поста

		set `_uuid_country` = ( -- Получение uuid для запиcи города
			SELECT `country`.`uuid` 
			FROM `country` 
            WHERE `country`.`title` = `countryTitle`
			LIMIT 1);

		IF `_uuid_country` IS NULL THEN -- Если страна не была ранее добавлена
			IF `countryTitle` IS NOT NULL THEN -- Если передано наименование страны
				set `_uuid_country` = UUID(); -- Генерация нового uuid для записи города
				INSERT INTO `country` ( -- Добавление записи города
					`uuid`, 
					`title`)
                VALUES (
					`_uuid_country`, 
					`countryTitle`);
			end if;
		end if;
		    
		set `_uuid_city` = ( -- Получение uuid для запиcи города
			SELECT `city`.`uuid` 
			FROM `city` 
            WHERE `city`.`title` = `cityTitle`
			LIMIT 1);

		IF `_uuid_city` IS NULL THEN -- Если город не был ранее добавлен
			IF `cityTitle` IS NOT NULL THEN -- Если передано наименование города
				set `_uuid_city` = UUID(); -- Генерация нового uuid для записи города
				INSERT INTO `city` ( -- Добавление записи города
					`uuid`,
					`uuid_country`, 
					`title`)
                VALUES (
					`_uuid_city`,
					`_uuid_country`, 
					`cityTitle`);
			end if;
		end if;


		-- NOTE: Так как функция предпологает сбор сырых данных (для ускорения сбора данных) этот блок под вопросом
		-- set `_uuid_address` = ( -- Получение uuid для запиcи адреcа
		-- 	SELECT `address`.`uuid` 
		-- 	FROM `address` 
        -- 	WHERE `address`.`title` = `address`
		-- 	LIMIT 1);
        -- IF `_uuid_address` IS NULL THEN -- Если адрес не был ранее добавлен
		-- 	IF `address` IS NOT NULL THEN -- Если переданно текстовое представление адреса
		-- 		set `_uuid_address` = UUID(); -- Генерация нового uuid для 
		-- 		INSERT INTO `address` (
		-- 			`uuid`, 
		-- 			`title`,
		-- 			`uuid_city`) 
        -- 	VALUES (
		-- 			`_uuid_address`, 
		-- 			`address`, 
		-- 			`_uuid_city`);
		-- 	end if;
		-- end if;
        
		INSERT INTO `dbo`.`post` (
			`uuid`, 
			`description`,
			`price`, 
			`isHidden`, 
			`uuid_address`)
		VALUES (
			`_uuid_post`, 
			`description`, 
			`price`, 
			1, 
			NULL);	
	end if;

	set `_uuid_community` = ( -- Получение uuid записи сообщества
		SELECT `community`.`uuid` 
		FROM `community` 
		WHERE `community`.`title` = `communityTitle`);

	if `_uuid_community` IS NULL THEN -- Если запись не создана ранее
		set `_uuid_community` = UUID(); -- Генерация ного uuid для записи сообщества
		INSERT INTO `community` ( -- Добавление записи сообщества 
			`uuid`, 
			`title`)
		VALUES (
			`_uuid_community`, 
			`communityTitle`);
	end if;

    set `_uuid_link` = ( -- Получение uuid записи url-адреса
		SELECT `link`.`uuid` 
		FROM `link` 
		WHERE `link`.`title` = `link`);

    if `_uuid_link` IS NULL THEN -- Если запись не создана ранее
		set `_uuid_link` = UUID(); -- Генерация uuid для новой записи url-адреса
		INSERT INTO `link` (
			`uuid`, 
			`title`,
			`datetime`, 
			`uuid_community`, 
			`uuid_post`)
		VALUES (
			`_uuid_link`, 
			`link`, 
			`datetime`, 
			`_uuid_community`, 
			`_uuid_post`);
	end if;
END

-- Создание функций

CREATE FUNCTION `f_address_uuidToText`( -- Функция конвертации uuid адреса в текстовое представление
	`uuid_address` NVARCHAR(36)) -- Параметр uuid адреса
	RETURNS NVARCHAR(128) CHARSET utf8 -- Тип возвращаемых данных
BEGIN
	RETURN (
		SELECT `title` 
		FROM `address` 
		WHERE `address`.`uuid` LIKE `uuid_address` 
		LIMIT 1);
END

CREATE FUNCTION `f_lastestPostDateTime`( -- Функция поиска последней даты для поста
	`uuid_post` NVARCHAR(36)) -- Параметр uuid поста
	RETURNS datetime -- Тип возвращаемых данных
BEGIN
	RETURN (
		SELECT `datetime` 
		FROM `link` 
		WHERE `link`.`uuid_post` LIKE `uuid_post` 
		ORDER BY `datetime` DESC 
		LIMIT 1);
END

CREATE FUNCTION `f_lastestPostURL`( -- Функция поиска последней url-ссылки для поста
	`uuid_post` NVARCHAR(36)) -- Параметр uuid поста
	RETURNS NVARCHAR(256) CHARSET utf8 -- Тип возвращаемых данных
BEGIN
	RETURN (
		SELECT `title` 
		FROM `link` 
		WHERE `link`.`uuid_post` LIKE `uuid_post` 
		ORDER BY `datetime` DESC 
		LIMIT 1);
END