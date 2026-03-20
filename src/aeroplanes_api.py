from abc import ABC, abstractmethod

from requests import get


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
        # URL для получения координат страны
        self.openstreetmap_url = 'https://nominatim.openstreetmap.org/search'
        # URL для получения данных о самолётах
        self.opensky_url = 'https://opensky-network.org/api/states/all?'
        # Здесь будет сохранён ответ от OpenSky
        self.aeroplanes = None

    def get_aeroplanes(self, country: str):
        """
        Получает список самолётов над указанной страной.

        1. Запрашивает координаты страны у Nominatim.
        2. Использует координаты для фильтрации самолётов через OpenSky.
        3. Сохраняет ответ в self.aeroplanes и возвращает его.
        """
        # --- 1. Запрос к Nominatim для получения границ страны ---
        # Заголовок с User-Agent обязателен, без него API может не отвечать
        headers_nominatim = {
            'User-Agent': 'test-app/1.0',
        }
        # Параметры запроса: страна, формат JSON, только первый результат
        params_nominatim = {
            'country': country,
            'format': 'json',
            'limit': 1,
        }

        # Отправляем GET-запрос к Nominatim
        response = get(url=self.openstreetmap_url,
                       params=params_nominatim, headers=headers_nominatim)  # type: ignore[arg-type]
        # Преобразуем ответ в JSON (список словарей)
        data = response.json()

        # Если страна не найдена, возвращаем None
        if not data:
            return None

        # Извлекаем boundingbox — координаты южной, северной, западной и восточной точек
        geo_coordinates = data[0].get('boundingbox')

        # --- 2. Запрос к OpenSky для получения самолётов в этом прямоугольнике ---
        # Параметры: минимальная и максимальная широта, минимальная и максимальная долгота
        params = {
            'lamin': geo_coordinates[0],
            'lamax': geo_coordinates[1],
            'lomin': geo_coordinates[2],
            'lomax': geo_coordinates[3],
        }

        # Отправляем GET-запрос к OpenSky
        response = get(url=self.opensky_url, params=params)  # type: ignore[arg-type]
        # Сохраняем ответ в атрибут экземпляра
        self.aeroplanes = response.json()
        # Возвращаем полученные данные
        return self.aeroplanes
