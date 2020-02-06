/* Файл генерации структуры БД */

DROP SCHEMA IF EXISTS `test`;
CREATE SCHEMA `test`; # Создание БД
USE `test`; # Указание субд работать с определенной БД

# Создание таблиц
DROP TABLE IF EXISTS `country`;
CREATE TABLE `country` ( /* таблица стран */
	`id` INT AUTO_INCREMENT NOT NULL UNIQUE, /* Порядковый номер записи в таблице */
	`uuid` NVARCHAR(36) NOT NULL UNIQUE, /* Уникальный идентификатор */
	`title` NVARCHAR(144) NULL UNIQUE, /* Название */
	PRIMARY KEY (`uuid`)); /* Указание на поле первичного ключа */

DROP TABLE IF EXISTS `city`;
CREATE TABLE `city` ( /* таблица городов */
	`id` INT AUTO_INCREMENT NOT NULL UNIQUE, /* Порядковый номер записи в таблице */
	`uuid` NVARCHAR(36) NOT NULL UNIQUE, /* Уникальный идентификатор */
	`uuid_country` NVARCHAR(36) NULL, /* Ссылка на запись в таблице стран */
	`title` NVARCHAR(144) NULL UNIQUE, /* Название */
	PRIMARY KEY (`uuid`)); /* Указание на поле первичного ключа */

DROP TABLE IF EXISTS `address`;
CREATE TABLE `address` ( /* таблица адреcов */
	`id` INT AUTO_INCREMENT NOT NULL UNIQUE, /* Порядковый номер записи в таблице */
	`uuid` NVARCHAR(36) NOT NULL UNIQUE, /* Уникальный идентификатор */
	`uuid_city` NVARCHAR(36) NULL, /* Ссылка на запись в таблице городов */
	`title` NVARCHAR(128) NULL, /* Полный адресс в текстовом формате без указания города и страны */
	`latitude` FLOAT NULL DEFAULT 0, /* Широта */
	`longitude` FLOAT NULL DEFAULT 0, /* Долгота */
	PRIMARY KEY (`uuid`)); /* Указание на поле первичного ключа */

DROP TABLE IF EXISTS `post`;
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

DROP TABLE IF EXISTS `community`;
CREATE TABLE `community` ( /* таблица cообщеcтв */
	`id` INT AUTO_INCREMENT NOT NULL UNIQUE, /* Порядковый номер записи в таблице */
	`uuid` NVARCHAR(36) NOT NULL UNIQUE, /* Уникальный идентификатор */
	`uuid_city` NVARCHAR(36) NULL, /* Ссылка на запись в таблице городов */
	`url` NVARCHAR(256) NULL, /* URL-адрес сообщества */
	PRIMARY KEY (`uuid`)); /* Указание на поле первичного ключа */

DROP TABLE IF EXISTS `link`;
CREATE TABLE `link` ( /* таблица ccылок на поcт */
	`id` INT AUTO_INCREMENT NOT NULL UNIQUE, /* Порядковый номер записи в таблице */
	`uuid` NVARCHAR(36) NOT NULL UNIQUE, /* Уникальный идентификатор */
	`uuid_post` NVARCHAR(36) NULL, /* Ссылка на запись поста (объявления) в таблице постов */
	`uuid_community` NVARCHAR(36) NULL, /* Ссылка на запись в таблице сообществ */
	`url` NVARCHAR(256) NULL, /* URL-cсылка на пост */
	`datetime` DATETIME NULL, /* Дата добавления объявление по этой ссылке */
	PRIMARY KEY (`uuid`)); /* Указание на поле первичного ключа */

DROP TABLE IF EXISTS `telephone`;
CREATE TABLE `telephone` ( /* таблица телефонов */
	`id` INT AUTO_INCREMENT NOT NULL UNIQUE, /* Порядковый номер записи в таблице */
	`uuid` NVARCHAR(36) NOT NULL UNIQUE, /* Уникальный идентификатор */
	`number` NVARCHAR(16) NULL UNIQUE, /* Номер телефона */
	PRIMARY KEY (`uuid`)); /* Указание на поле первичного ключа */

DROP TABLE IF EXISTS `telephone__post`;
CREATE TABLE `telephone__post` ( /* таблица cвязи телефонов и объявлений */
	`uuid_telephone` NVARCHAR(36) NOT NULL, /* Ссылка на запись в таблице телефонов */
	`uuid_post` NVARCHAR(36) NOT NULL, /* Ссылка на запись в таблице объявлений */
	PRIMARY KEY (`uuid_telephone`, `uuid_post`)); /* Указание на поля составного первичного ключа */
DROP TABLE IF EXISTS `img`;
CREATE TABLE `img` ( /* таблица ссылок на изображения */
	`id` INT AUTO_INCREMENT NOT NULL UNIQUE, /* Порядковый номер записи в таблице */
	`uuid` NVARCHAR(36) NOT NULL UNIQUE, /* Уникальный идентификатор */
	`url` NVARCHAR(256) NULL UNIQUE, /* URL-ссылка на изображение */
	PRIMARY KEY (`uuid`)); /* Указание на поле первичного ключа */

DROP TABLE IF EXISTS `img__post`;
CREATE TABLE `img__post` ( /* таблица cвязи картинок и объявлений */
	`uuid_img` NVARCHAR(36) NOT NULL, /* Ссылка на запись в таблице изображений */
	`uuid_post` NVARCHAR(36) NOT NULL, /* Ссылка на запись в таблице объявлений */
	PRIMARY KEY (`uuid_img`, `uuid_post`)); /* Указание на поля составного первичного ключа */
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
# Внешние ключи для таблицы связей изображений_и_объявлений */
ALTER TABLE `img__post` ADD CONSTRAINT `img__post__img` /* Связь таблиц связей изображений_и_объявлений и телефонных номеров */
	FOREIGN KEY (`uuid_img`) /* Поле со ссылкой */
	REFERENCES `img` (`uuid`) /* Поле на которое ссылается */
	ON DELETE NO ACTION /* Действие при удалении */
	ON UPDATE NO ACTION; /* ДЕйствие при обновлении */
ALTER TABLE `img__post` ADD CONSTRAINT `img__post__post` /* Связь таблиц связей изображений_и_объявлений и объявлений */
	FOREIGN KEY (`uuid_post`) /* Поле со ссылкой */
	REFERENCES `post` (`uuid`) /* Поле на которое ссылается */
	ON DELETE NO ACTION /* Действие при удалении */
	ON UPDATE NO ACTION; /* ДЕйствие при обновлении */
--