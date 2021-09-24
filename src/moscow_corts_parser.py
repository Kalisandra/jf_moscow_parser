from typing import Dict

from shapely.geometry import Polygon

from .config import MOSCOW_COURTS_DATA
from .utils import fetch_html


def load_moscow_courts_row_data():
    """ функция загружает сырые данные мировых судебных участков города Москвы """
    moscow_courts_row_data = fetch_html(MOSCOW_COURTS_DATA)
    return (moscow_courts_row_data)


def load_courts_jf_polygons(collection) -> Dict:
    """ Функция забирает данные из базы о судебных учасках и возвращает словарь, в которм ключ - 
        id судебного учаска, значение - список полигонов территориальной подсудности """
    all_courts_data = collection.find({})
    all_courts_polygons = {}
    for court in all_courts_data:
        court_polygons = [Polygon(item) for item in court.get('polygonData') if len(item) > 2]
        all_courts_polygons[court['_id']] = court_polygons
    return all_courts_polygons
