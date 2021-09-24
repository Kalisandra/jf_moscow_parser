""" файл содержит глобальные константы """
import os

import certifi
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

CLUSTER = MongoClient(
    os.getenv("DB_URL"),
    tlsCAFile=certifi.where()
)

MOSCOW_DATA_API_URL = 'https://apidata.mos.ru/v1/datasets/60562/'

MOSCOW_COURTS_DATA = 'https://mos-sud.ru/api/courts'

MOSCOW_OPEN_DATA_API_KEY = os.getenv("MOSCOW_OPEN_DATA_API_KEY")

API_1C_URL = 'http://91.218.251.89/ipb/hs/parser/load'


# конфигурации для направление данных в API
class ApiCourtData():
    """ конфигуратор данных для направления в 1С """
    def __init__(self, court_code, jf_data):
        self.court_code = court_code
        self.jf_data = jf_data

    def __call__(self):
        api_sending_data = {
            "Логин": os.getenv("1C_API_LOGIN"),
            "Пароль": os.getenv("1C_API_PASSWORD"),
            "ИдентификаторРесурса": "mos-sud.ru/territorial",
            "Данные": [
                {
                    "ПодсудностьСуда": {
                        "КодГАСРФ": self.court_code,
                        "ИнтервалыДомов": self.jf_data,
                    }
                }
            ]
        }
        return api_sending_data
