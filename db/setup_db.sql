/* Файл генерации структуры БД */

CREATE SCHEMA `test`; # Создание БД
USE `test`; # Указание субд работать с определенной БД

# Создание таблиц

CREATE TABLE `country` ( /* таблица стран */
	`id` INT AUTO_INCREMENT NOT NULL UNIQUE, /* Порядковый номер записи в таблице */
	`uuid` NVARCHAR(36) NOT NULL UNIQUE, /* Уникальный идентификатор */
	`title` NVARCHAR(144) NULL UNIQUE, /* Название */
	PRIMARY KEY (`uuid`)); /* Указание на поле первичного ключа */

CREATE TABLE `city` ( /* таблица городов */
	`id` INT AUTO_INCREMENT NOT NULL UNIQUE, /* Порядковый номер записи в таблице */
	`uuid` NVARCHAR(36) NOT NULL UNIQUE, /* Уникальный идентификатор */
	`uuid_country` NVARCHAR(36) NULL, /* Ссылка на запись в таблице стран */
	`title` NVARCHAR(144) NULL UNIQUE, /* Название */
	PRIMARY KEY (`uuid`)); /* Указание на поле первичного ключа */

CREATE TABLE `address` ( /* таблица адреcов */
	`id` INT AUTO_INCREMENT NOT NULL UNIQUE, /* Порядковый номер записи в таблице */
	`uuid` NVARCHAR(36) NOT NULL UNIQUE, /* Уникальный идентификатор */
	`uuid_city` NVARCHAR(36) NULL, /* Ссылка на запись в таблице городов */
	`title` NVARCHAR(128) NULL, /* Полный адресс в текстовом формате без указания города и страны */
	`latitude` FLOAT NULL DEFAULT 0, /* Широта */
	`longitude` FLOAT NULL DEFAULT 0, /* Долгота */
	PRIMARY KEY (`uuid`)); /* Указание на поле первичного ключа */
CREATE TABLE `post` ( /* таблица объявлений */
	`id` INT AUTO_INCREMENT NOT NULL UNIQUE, /* Порядковый номер записи в таблице */
	`uuid` NVARCHAR(36) NOT NULL UNIQUE, /* Уникальный идентификатор */
	`uuid_address` NVARCHAR(36) NULL, /* Ссылка на географический адресс объявления */
	`description` NVARCHAR(1024) NULL, /* Описание объявление */
	`price` FLOAT NULL, /* Стоимость, указанная в объявлении */
	`status` TINYINT(1) NULL DEFAULT 1, /* Статус обработки поста (
		0-не корректный пост, 
		1-полностью обработан, 
		2-ожидает добавление адреса */
	PRIMARY KEY (`uuid`)); /* Указание на поле первичного ключа */

CREATE TABLE `community` ( /* таблица cообщеcтв */
	`id` INT AUTO_INCREMENT NOT NULL UNIQUE, /* Порядковый номер записи в таблице */
	`uuid` NVARCHAR(36) NOT NULL UNIQUE, /* Уникальный идентификатор */
	`url` NVARCHAR(256) NULL, /* URL-адрес сообщества */
	PRIMARY KEY (`uuid`)); /* Указание на поле первичного ключа */

CREATE TABLE `link` ( /* таблица ccылок на поcт */
	`id` INT AUTO_INCREMENT NOT NULL UNIQUE, /* Порядковый номер записи в таблице */
	`uuid` NVARCHAR(36) NOT NULL UNIQUE, /* Уникальный идентификатор */
	`uuid_post` NVARCHAR(36) NULL, /* Ссылка на запись поста (объявления) в таблице постов */
	`uuid_community` NVARCHAR(36) NULL, /* Ссылка на запись в таблице сообществ */
	`url` NVARCHAR(256) NULL, /* URL-cсылка на пост */
	`datetime` DATETIME NULL, /* Дата добавления объявление по этой ссылке */
	PRIMARY KEY (`uuid`)); /* Указание на поле первичного ключа */

CREATE TABLE `telephone` ( /* таблица телефонов */
	`id` INT AUTO_INCREMENT NOT NULL UNIQUE, /* Порядковый номер записи в таблице */
	`uuid` NVARCHAR(36) NOT NULL UNIQUE, /* Уникальный идентификатор */
	`number` NVARCHAR(16) NULL UNIQUE, /* Номер телефона */
	PRIMARY KEY (`uuid`)); /* Указание на поле первичного ключа */

CREATE TABLE `telephone__post` ( /* таблица cвязи телефонов и объявлений */
	`id` INT AUTO_INCREMENT NOT NULL UNIQUE, /* Порядковый номер записи в таблице */
	`uuid_telephone` NVARCHAR(36) NOT NULL, /* Ссылка на запись в таблице телефонов */
	`uuid_post` NVARCHAR(36) NOT NULL, /* Ссылка на запись в таблице объявлений */
	PRIMARY KEY (`uuid_telephone`, `uuid_post`)); /* Указание на поля составного первичного ключа */
--

# Создание внешних ключей

# Внешние ключи для таблицы url-ссылок
ALTER TABLE `link` ADD CONSTRAINT `link__community` /* Связь таблиц url-ссылок и сообществ */
	FOREIGN KEY (`uuid_community`) /* Поле со ссылкой */
	REFERENCES `community` (`uuid`) /* Поле на которое ссылается */
	ON DELETE NO ACTION /* Действия при удалении */
	ON UPDATE NO ACTION; /* Действяи при обновлении */
ALTER TABLE `link` ADD CONSTRAINT `link__post` /* Связь таблиц url-ссылок и объявлений */
	FOREIGN KEY (`uuid_post`) /* Поле со ссылкой */
	REFERENCES `post` (`uuid`) /* Поле на которое ссылается */
	ON DELETE NO ACTION /* Действие при удалении */
	ON UPDATE NO ACTION; /* ДЕйствие при обновлении */

# Внешние ключи для таблицы географических адресов
ALTER TABLE `address` ADD CONSTRAINT `address__city` /* Связь таблиц географических адресов и городов */
	FOREIGN KEY (`uuid_city`) /* Поле со ссылкой */
	REFERENCES `city` (`uuid`) /* Поле на которое ссылается */
	ON DELETE NO ACTION /* Действие при удалении */
	ON UPDATE NO ACTION; /* ДЕйствие при обновлении */

# Внешние ключи для таблицы объявлений
ALTER TABLE `post` ADD CONSTRAINT `post__address` /* Связь таблиц объявлений и географических адресов */
	FOREIGN KEY (`uuid_address`) /* Поле со ссылкой */
	REFERENCES `address` (`uuid`) /* Поле на которое ссылается */
	ON DELETE NO ACTION /* Действие при удалении */
	ON UPDATE NO ACTION; /* ДЕйствие при обновлении */
# Внешние ключи для таблицы связей телефонных_номеров_и_объявлений */
ALTER TABLE `telephone__post` ADD CONSTRAINT `telephone__post__telephone` /* Связь таблиц связей телефонных_номеров_и_объявлений и телефонных номеров */
	FOREIGN KEY (`uuid_telephone`) /* Поле со ссылкой */
	REFERENCES `telephone` (`uuid`) /* Поле на которое ссылается */
	ON DELETE NO ACTION /* Действие при удалении */
	ON UPDATE NO ACTION; /* ДЕйствие при обновлении */
ALTER TABLE `telephone__post` ADD CONSTRAINT `telephone__post__post` /* Связь таблиц связей телефонных_номеров_и_объявлений и объявлений */
	FOREIGN KEY (`uuid_post`) /* Поле со ссылкой */
	REFERENCES `post` (`uuid`) /* Поле на которое ссылается */
	ON DELETE NO ACTION /* Действие при удалении */
	ON UPDATE NO ACTION; /* ДЕйствие при обновлении */
--


# Создание таблиц

/*
NOTE: Необходимо проработать аспект использавания хэштэгов в системе
NOTE: на текущем этапе эти таблицы отсутствует
CREATE TABLE `hashtag` ( /* таблица хэштэгов
	`uuid` NVARCHAR(36) NOT NULL UNIQUE, /* Уникальный идентификатор
	`title` NVARCHAR(144) NULL UNIQUE, /* Наименование хэштэга
	PRIMARY KEY (`uuid`)); /* Указанеи на поле первичного ключа
CREATE TABLE `hashtag__post` ( /* таблица cвязей хэштэгов и поcтов
	`uuid_hashtag` NVARCHAR(36) NULL, /* Ссылка на запись в таблице хэштэгов
	`uuid_post` NVARCHAR(36) NULL, /* ссылка на запись в таблице объявлений
	PRIMARY KEY (`uuid_hashtag`, `uuid_post`)); /* Указание на поля составного первичного ключа

NOTE: Необходимо проработать аспект использавания комментариев в системе
NOTE: на текущем этапе эта таблица отсутствует
CREATE TABLE comment ( /* таблица комментариев
	uuid NVARCHAR(36) NOT NULL UNIQUE,
	text LONGTEXT NOT NULL,
	uuid_foreign NVARCHAR(36) NOT NULL,
	PRIMARY KEY (uuid)); /* ccылка на запиcи в БД
	
NOTE: Необходимо проработать аспект использавания оценок в системе
NOTE: на текущем этапе эта таблица отсутствует
CREATE TABLE rating ( /* таблица оценок
	uuid NVARCHAR(36) NOT NULL UNIQUE,
	value FLOAT NOT NULL,
	uuid_foreign NVARCHAR(36) NOT NULL,
	PRIMARY KEY (uuid)); /* ccылка на запиcи в БД
*/

# Создание внешних ключей

/*
NOTE: Необходимо проработать аспект использавания хэштегов в системе
NOTE: на текущем этапе эти связи отсутствует
# Внешние ключи для таблицы связей хэштегов_и_объявлений
ALTER TABLE `hashtag__post` ADD CONSTRAINT `hashtag__post__hashtag` # Связь таблиц связей хэштегов_и_объявлений и хэштегов
	FOREIGN KEY (`uuid_hashtag`) # Поле со ссылкой 
	REFERENCES `hashtag` (`uuid`) # Поле на которое ссылается
	ON DELETE NO ACTION # Действие при удалении
	ON UPDATE NO ACTION; # ДЕйствие при обновлении
ALTER TABLE `hashtag__post` ADD CONSTRAINT `hashtag__post__post` # Связь таблиц связей хэштегов_и_объявлений и объявлений
	FOREIGN KEY (`uuid_post`) # Поле со ссылкой 
	REFERENCES `post` (`uuid`) # Поле на которое ссылается
	ON DELETE NO ACTION # Действие при удалении
	ON UPDATE NO ACTION; # ДЕйствие при обновлении

NOTE: Необходимо проработать аспект использавания комментариев в системе
NOTE: на текущем этапе эти связи отсутствует
ALTER TABLE comment ADD CONSTRAINT comment__city 
    FOREIGN KEY (uuid_foreign) 
    REFERENCES city (uuid) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION; 
ALTER TABLE comment ADD CONSTRAINT comment__address 
    FOREIGN KEY (uuid_foreign) 
    REFERENCES address (uuid) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION; 
ALTER TABLE comment ADD CONSTRAINT comment__telephone 
    FOREIGN KEY (uuid_foreign) 
    REFERENCES telephone (uuid) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION; 
ALTER TABLE comment ADD CONSTRAINT comment__hashtag 
    FOREIGN KEY (uuid_foreign) 
    REFERENCES hashtag (uuid) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION; 
ALTER TABLE comment ADD CONSTRAINT comment__link
    FOREIGN KEY (uuid_foreign) 
    REFERENCES link (uuid) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION;    
ALTER TABLE comment ADD CONSTRAINT comment__community
    FOREIGN KEY (uuid_foreign) 
    REFERENCES community (uuid) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION;    
ALTER TABLE comment ADD CONSTRAINT comment__post
    FOREIGN KEY (uuid_foreign) 
    REFERENCES post (uuid) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION;

NOTE: Необходимо проработать аспект использавания рейтингов в системе
NOTE: на текущем этапе эти связи отсутствует
ALTER TABLE rating ADD CONSTRAINT rating__city
    FOREIGN KEY (uuid_foreign) 
    REFERENCES city (uuid) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION;
ALTER TABLE rating ADD CONSTRAINT rating__address
    FOREIGN KEY (uuid_foreign) 
    REFERENCES address (uuid) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION;
ALTER TABLE rating ADD CONSTRAINT rating__telephone
    FOREIGN KEY (uuid_foreign) 
    REFERENCES telephone (uuid) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION;
ALTER TABLE rating ADD CONSTRAINT rating__hashtag
    FOREIGN KEY (uuid_foreign) 
    REFERENCES hashtag (uuid) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION;
ALTER TABLE rating ADD CONSTRAINT rating__link
    FOREIGN KEY (uuid_foreign) 
    REFERENCES link (uuid) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION;
ALTER TABLE rating ADD CONSTRAINT rating__community
    FOREIGN KEY (uuid_foreign) 
    REFERENCES community (uuid) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION;
ALTER TABLE rating ADD CONSTRAINT rating__post
    FOREIGN KEY (uuid_foreign) 
    REFERENCES post (uuid) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION;
ALTER TABLE rating ADD CONSTRAINT rating__comment
    FOREIGN KEY (uuid_foreign) 
    REFERENCES comment (uuid) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION;
*/