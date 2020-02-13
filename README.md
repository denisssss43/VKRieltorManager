# VKRieltorManager
 Проект менеджер по автоматическому сбору информации с групп агригаторов информации о недвижимости.

## Запуск сервера MySql в контейнере докера
 
### Получение образа:
```bash 
docker pull mysql/mysql-server:5.7 
```

### Развертка образа:
```bash
docker run -p 3306:3306 --name=mysqlvkrieltor -e MYSQL_ROOT_PASSWORD=MnM32RtQt -d mysql:5.7
```

```3306:3306``` - первая цифра - внешний порт, вторая - внутренний;

```--name``` - наименование будущего контейнера;

```MYSQL_ROOT_PASSWORD``` - пароль root пользователя (если не указать будет сгенерирован случайно).
 

### Получение пораметров подключения для MySQL Workbench:
```bash
docker inspect mysqlvkrieltor
``` 

#### вывод:
```JSON
...,
"Name": "/mysqlvkrieltor",
...
"Config": {
	...,
	"Env": [
		"MYSQL_ROOT_PASSWORD=MnM32RtQt",
		...
	],
	...
},
"NetworkSettings": {
	...,
	"Networks": {
		"nat": {
			...,
			"IPAddress": "172.23.252.104",
			...
		}
	}
}
```
 
### Параметры подключения к mysqlvkrieltor: 
```host: 172.23.252.104``` - берем из значения "IPAddress"; 

```port: 3306``` - значение внешнего порта (устанавливается в ручную); 

```user: root``` - стандартное значение; 

```password: MnM32RtQt``` - берем из значения "MYSQL_ROOT_PASSWORD".
