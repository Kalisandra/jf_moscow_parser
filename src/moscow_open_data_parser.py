from typing import Dict, List

from .config import MOSCOW_DATA_API_URL, MOSCOW_OPEN_DATA_API_KEY
from .logger_settings import logger
from .utils import fetch_html


@logger.catch
def load_dataset_count() -> int:
    """ функция загружает количество записей в базе адресов открытых данных Москвы """
    payload = {'api_key': MOSCOW_OPEN_DATA_API_KEY}
    url = f'{MOSCOW_DATA_API_URL}count'
    return fetch_html(url, payload=payload)


@logger.catch
def load_address_data(top: int = 1000, skip: int = 0) -> List:
    """ функция загружает данные об адресах из базы открытых данных Москвы
        top - количество загружаемых адресов (макс - 1000 штук),
        skip - колчество пропускаемых адресов от начала датасета"""
    cleaned_data = []
    payload = {
        '$top': top,
        '$skip': skip,
        'api_key': MOSCOW_OPEN_DATA_API_KEY,
    }
    url = f"{MOSCOW_DATA_API_URL}rows"
    moscow_addresses_open_data = fetch_html(url, payload=payload)
    if moscow_addresses_open_data:
        for address_open_data in moscow_addresses_open_data:
            # формируем данные об адресе до улицы
            address = _aggregate_addreess_data(address_open_data)
            # формируем данные о номере дома
            house = _aggregate_house_number_data(address_open_data)
            if not address_open_data['Cells'].get('geoData'):
                logger.error(f" Адрес {address}, {house} не имеет геоданных")
                continue
            else:
                geodata = _aggregate_house_geodate(address_open_data)

                address_clean_data = {
                    'global_id': address_open_data.get('global_id'),
                    'address': address,
                    'house': house,
                    'geodata_type': address_open_data['Cells'].get('geoData').get('type'),
                    'geodata': geodata
                }
                cleaned_data.append(address_clean_data)
    return cleaned_data


@logger.catch
def _aggregate_house_geodate(address_open_data: Dict) -> List:
    """ функция объединяет геоданные здания исходя из полученного формата данных """
    geodata = []
    coordinates = address_open_data['Cells'].get('geoData').get('coordinates')
    # здание простой формы
    if len(coordinates) == 1:
        for item in coordinates:
            geodata.append([(point[1], point[0]) for point in item])
    # здание сложной формы
    elif len(coordinates) > 1:
        for build in coordinates:
            # если здание имеет пристройки со своим пологином координат
            if type(build[0][0]) == list:
                for item in build:
                    geodata.append([(point[1], point[0]) for point in item])
            # здание имеет сложную форму без пристроек
            else:
                geodata.append([(point[1], point[0]) for point in build])
    else:
        logger.error(f" Адрес {address_open_data['Cells'].get('ADDRESS')} не имеет геоданных")
    return geodata


@logger.catch
def _aggregate_addreess_data(address_open_data: Dict) -> str:
    address = [
        address_open_data['Cells'].get('P1'),
        address_open_data['Cells'].get('P3'),
        address_open_data['Cells'].get('P4'),
        address_open_data['Cells'].get('P6'),
        address_open_data['Cells'].get('P7'),
        address_open_data['Cells'].get('P90'),
        address_open_data['Cells'].get('P91'),
    ]
    return ', '.join(item for item in address if item)


@logger.catch
def _aggregate_house_number_data(address_open_data: Dict) -> str:
    house = [
        address_open_data['Cells'].get('L1_TYPE'),
        address_open_data['Cells'].get('L1_VALUE'),
        address_open_data['Cells'].get('L2_TYPE'),
        address_open_data['Cells'].get('L2_VALUE'),
        address_open_data['Cells'].get('L3_TYPE'),
        address_open_data['Cells'].get('L3_VALUE'),
    ]
    return ' '.join(item for item in house if item)
