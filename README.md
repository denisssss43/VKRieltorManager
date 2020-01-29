# VKRieltorManager
 Проект менеджер по автоматическому сбору информации с групп агригаторов предложений по сбору информации о недвижимости.

 запуск сервера MySql в контейнере докера
 Получение образа:
 > docker pull mysql/mysql-server:5.7

 развертка образа:
 > docker run -p 3306:3306 --name=mysqlvkrieltor -e MYSQL_ROOT_PASSWORD=MnM32RtQt -d mysql:5.7
 3306:3306 - первая цифра - внешний порт, вторая - внутренний
 --name - 
 MYSQL_ROOT_PASSWORD - 

 Получение пораметров подключения для MySQL Workbench:
 > docker inspect mysqlvkrieltor
 вывод:
 [
    {
        ...,
        "Config": {..., "Env": ["MYSQL_ROOT_PASSWORD=MnM32RtQt", ...], ...},
        "NetworkSettings": {..., "Networks": {"nat": {..., "IPAddress": "172.23.252.104", ...} } }
    }
 ]
 
 Параметры подключения к mysqlvkrieltor: 
 host: 172.23.252.104 - берем из значения "IPAddress"
 port: 3306 - значение внешнего порта (устонавливается в ручную)
 user: root - стандартное значение
 password: MnM32RtQt - берем из значения "MYSQL_ROOT_PASSWORD"
