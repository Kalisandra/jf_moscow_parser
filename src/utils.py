import json
import urllib3
from typing import Dict

import requests
import requests_random_user_agent  # автоматически подставляет случайный user-agents, нужен только импорт

from .config import API_1C_URL, ApiCourtData
from .logger_settings import logger


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@logger.catch
def fetch_html(url: str, payload: Dict = None):
    """ функция получения данных с html страницы """
    try:
        result = requests.get(url, params=payload, verify=False, timeout=600)
        if result.status_code == 200:
            logger.info(f'Данные по ссылке {url} получены')
            return result.json()
        else:
            logger.info(f'Ссылка {url} недоступна, status code {result.status_code}')
            return None
    except(requests.RequestException):
        logger.info(f'Страница не доступна url={result.text}, проверьте интернет соединение')
        return None


@logger.catch
def send_jf_court_data_to_api(collection):
    """функция направляет сформированные данные тер подсудности в API 1C"""
    all_courts_data = collection.find({})

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json_co; charset=UTF-8',
        'Accept-Encoding': 'deflate',
    }

    for court in all_courts_data:
        court_data = ApiCourtData(court['code'], court['jf'])
        data = json.dumps(court_data(), ensure_ascii=False).encode('utf-8')
        try:
            result = requests.post(API_1C_URL, headers=headers, data=data)
            if not result.json().get('ОписаниеОшибки'):
                logger.info(f'Данные из файла {court_data.court_code} успешно направлены')
            else:
                logger.error(f'При направлении данных возникла ошибка: {result.status_code}')
        except requests.RequestException as e:
            return logger.error(f'Отсутствует доступ к API: {e}')
