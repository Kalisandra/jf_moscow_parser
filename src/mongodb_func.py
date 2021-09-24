import json
from typing import List, Dict

from src.logger_settings import logger
from shapely.geometry import Polygon


def load_courts_data_to_db(collection, courts_row_data: List) -> None:
    """ функция записи данных о судебных участках в базу данных, предварительно далив из нее все данные"""
    collection.delete_many({})
    for court in courts_row_data:
        if court.get('polygonData') and not collection.find_one({'_id': court.get('id')}):
            post_data = {
                "_id": court.get('id'),
                "code": court.get('code'),
                "fullName": court.get('fullName'),
                "polygonData": json.loads(court.get('polygonData')),
                "address": court.get("address"),
                "jf": [],
            }
            collection.insert_one(post_data)


def find_house_jf(collection, house: Dict, all_courts_polygons: Dict) -> None:
    """  функция определяет территориальную подсудность здания и записываеть данные в базу """
    house_jf_status = 0  # количество найденных совпадений с полигонами тер подсудности
    house_polygons = [Polygon(item) for item in house.get('geodata') if len(item) > 2]
    for id, court_polygons in all_courts_polygons.items():
        for polygon in court_polygons:
            if all(polygon.contains(item) for item in house_polygons):
                collection.update_one({'_id': id}, {'$addToSet': {
                    'jf': {
                        "Адрес": house.get('address'),
                        "Четность": 0,
                        "ДомаС": house.get('house'),
                        "ДомаПо": house.get('house'),
                    }
                }})
                house_jf_status += 1
    if house_jf_status == 0:
        logger.error(f"Данные тер подсуднсоти по адресу {house.get('address')}, {house.get('house')} "
                     "не опеределны")
    elif house_jf_status > 1:
        logger.debug(f"Адрес {house.get('address')}, {house.get('house')} входит подсудность "
                     "нескольких судебных участков. Требуется ручная проверка")
