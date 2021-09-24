# MOSCOW JF PARSER

## Описание проекта

Сервис парсинга территориальной подсудности мировых судов города Москвы основан на следующих этапах:

1. Парсинг полигонов территориальной подсудности мировых судов города Москвы по ссылке https://mos-sud.ru/api/courts и запись сериализованных данных в MongoDB;

2. Перебор всех записей адресов из базы открытых данных города Москвы https://apidata.mos.ru/v1/datasets/60562/, для получения координат здания. Далее происходит сопоставление полученных координат с полигонами территориальной подсудности судебных участков, находящихся в базе и при полном вхождении координат здания в полигон судебного участка, данные здания записываются в базу данных к соответствующему судебному участку;

3. После завершения перебора данных об адресах города Москвы, одним запросом получаем данные из MongoDB и в цикле for - in формируем json файлы с территориальной подсудностью и направляем их API 1С


## Переменные виртуального окружения
Для работы сервиса необходимо прописать следующие переменные виртуального окружения в файле .env,
находящимся в корне проекта:

1. DB_URL - url к базе данных MongoDb, содержащий логин и пароль

2. 1C_API_LOGIN - логин для направления данных в API 1C

3. 1C_API_PASSWORD - пароль к API 1C

4. MOSCOW_OPEN_DATA_API_KEY - ключ для получения данных из API открытых данных города Москвы