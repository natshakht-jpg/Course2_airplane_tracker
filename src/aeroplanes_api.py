from abc import ABC, abstractmethod
from typing import Optional

from requests import get
from requests.exceptions import RequestException


class AbstractAeroplanesAPI(ABC):
    """Абстрактный класс для работы с API самолётов."""

    @abstractmethod
    def get_aeroplanes(self, country: str):
        """Получить список самолётов по названию страны."""
        pass


class AeroplanesAPI(AbstractAeroplanesAPI):
    """Класс для получения данных о самолётах через API Nominatim и OpenSky."""

    def __init__(self):
        """Инициализирует URL-адреса API и хранилище ответа."""
        self.__openstreetmap_url = 'https://nominatim.openstreetmap.org/search'
        self.__opensky_url = 'https://opensky-network.org/api/states/all?'
        self.__aeroplanes = None

    def _connect(self, url: str, params: Optional[dict] = None, headers: Optional[dict] = None):
        """
        Приватный метод для отправки GET-запроса с проверкой статуса.

        :param url: Адрес API
        :param params: Параметры запроса
        :param headers: Заголовки запроса
        :return: JSON-ответ или None при ошибке
        """
        try:
            response = get(url, params=params, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка API: статус {response.status_code} при запросе к {url}")
                return None
        except RequestException as e:
            print(f"Ошибка подключения: {e}")
            return None

    def get_aeroplanes(self, country: str):
        """
        Получает список самолётов над указанной страной.

        1. Запрашивает координаты страны у Nominatim.
        2. Использует координаты для фильтрации самолётов через OpenSky.
        3. Сохраняет ответ в self.__aeroplanes и возвращает его.
        """
        # ---- Шаг 1. Запрос к Nominatim для получения границ страны ----
        headers_nominatim = {'User-Agent': 'test-app/1.0'}
        params_nominatim = {
            'country': country,
            'format': 'json',
            'limit': 1,
        }

        data = self._connect(self.__openstreetmap_url, params=params_nominatim, headers=headers_nominatim)

        if not data:
            return None

        # Извлекаем boundingbox (юг, север, запад, восток)
        geo_coordinates = data[0].get('boundingbox')
        if not geo_coordinates or len(geo_coordinates) != 4:
            print("Ошибка: не удалось получить координаты страны")
            return None

        # ---- Шаг 2. Запрос к OpenSky для получения самолётов ----
        params_opensky = {
            'lamin': geo_coordinates[0],
            'lamax': geo_coordinates[1],
            'lomin': geo_coordinates[2],
            'lomax': geo_coordinates[3],
        }

        self.__aeroplanes = self._connect(self.__opensky_url, params=params_opensky)
        return self.__aeroplanes
