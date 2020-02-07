/* Файл генерации структуры библиотеки пользователей */

DROP SCHEMA IF EXISTS `user_library`;
CREATE SCHEMA `post_library`; # Создание схемы библиотеки постов


# Создание таблиц

# Указание субд работать со схемой библиотеки постов
USE `user_library`; 

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` ( /* таблица пользователей */
	`id` INT AUTO_INCREMENT NOT NULL UNIQUE, /* Порядковый номер записи в таблице */
	`uuid` NVARCHAR(36) NOT NULL UNIQUE, /* Уникальный идентификатор */
	`first_name` NVARCHAR(144) NULL, /* Имя пользователя */
	`last_name` NVARCHAR(144) NULL, /* Фамилия пользователя */
	PRIMARY KEY (`uuid`)); /* Указание на поле первичного ключа */

