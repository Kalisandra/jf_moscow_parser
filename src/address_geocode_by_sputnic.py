from typing import Tuple

from loguru import logger

from .config import SPUTNIC_API_URL
from .utils import fetch_html


@logger.catch
def load_house_geocode(address: str) -> Tuple or None:
    """ функция получения координат дома через api sputnik.ru """
    payload = {'q': address}
    load_house_api_data = fetch_html(SPUTNIC_API_URL, payload=payload)
    address_data = load_house_api_data['result']['address']
    if len(address_data) == 1:
        house_geocode = address_data[0]['features'][0]['geometry']['geometries'][0]['coordinates']
        return (float(house_geocode[1]), float(house_geocode[0]))
    else:
        return None
