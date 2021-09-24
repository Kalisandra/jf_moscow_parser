import time

from src.config import CLUSTER
from src.logger_settings import logger
from src.moscow_open_data_parser import load_dataset_count, load_address_data
from src.moscow_corts_parser import load_moscow_courts_row_data, load_courts_jf_polygons
from src.mongodb_func import load_courts_data_to_db, find_house_jf
from src.utils import send_jf_court_data_to_api

db = CLUSTER['jf_db']
collection = db["moscow_courts"]


if __name__ == '__main__':
    start_time = time.perf_counter()
    # загружаем данные о судебных участках в базу
    courts_row_data = load_moscow_courts_row_data()
    load_courts_data_to_db(collection, courts_row_data)

    # получаем данные о полигонах судебных участках
    all_courts_polygons = load_courts_jf_polygons(collection)

    # получаем данные о количестве записей адресов на портале открытых данных г. Москвы
    moscow_addresses = load_dataset_count()

    # цикл по получению данных из базы открытых данных Москвы, поиска входждения в полигон и записи данных в Mongodb
    skip = 0
    while skip <= moscow_addresses:
        logger.info(f"ведется сбор данных из базы открытых данных Москвы с {skip + 1} по {skip + 1000} запись")
        houses = load_address_data(skip=skip)
        if not houses:
            logger.error(f'Данные по записям из базы с {skip +1} по {skip + 1001} не получены, '
                         'запущена повторная попытка получения данных')
            continue
        else:
            for house in houses:
                find_house_jf(collection, house, all_courts_polygons)
            logger.info(f"завершен сбор данных из базы открытых данных Москвы с {skip + 1} по {skip + 1000} запись")
            skip += 1000  # прибавляем количество пропускаемых адрессов для дальнейшего запроса данных
    send_jf_court_data_to_api(collection)   # направление сформированных данных в API 1C
    logger.info(f'Время работы скрипта {time.perf_counter() - start_time}')
