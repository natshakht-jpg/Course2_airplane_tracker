import json
from abc import ABC, abstractmethod
from typing import List

from src.aeroplane import Aeroplane


class BaseFileSaver(ABC):
    """Абстрактный класс для работы с файловым хранилищем данных о самолётах"""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавить информацию о самолёте в файл"""
        pass

    @abstractmethod
    def get_aeroplanes(self, **criteria) -> list[Aeroplane]:
        """Получить список самолётов по критериям (например, по стране регистрации)"""
        pass

    @abstractmethod
    def delete_aeroplane(self, icao24: str) -> None:
        """Удалить информацию о самолёте по его идентификатору"""
        pass


class JSONSaver(BaseFileSaver):
    """Класс для сохранения данных о самолётах в JSON-файл"""

    def __init__(self, filename: str = "aeroplanes.json"):
        """Инициализация с указанием имени файла (по умолчанию aeroplanes.json)"""
        self.__filename = filename

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавить информацию о самолёте в JSON-файл (без дубликатов по icao24)"""
        # Пытаемся прочитать существующие данные
        try:
            with open(self.__filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Если файла нет или он пустой/битый, начинаем с пустого списка
            data = []

        # Преобразуем список словарей в список объектов Aeroplane для проверки
        existing_planes = []
        for item in data:
            try:
                plane = Aeroplane(
                    icao24=item['icao24'],
                    callsign=item['callsign'],
                    origin_country=item['origin_country'],
                    velocity=item['velocity'],
                    baro_altitude=item['baro_altitude']
                )
                existing_planes.append(plane)
            except KeyError:
                # Если данные повреждены, пропускаем этот элемент
                continue

        # Проверяем дубликат по icao24
        for plane in existing_planes:
            if plane.icao24 == aeroplane.icao24:
                # print(f"Самолёт с icao24 {aeroplane.icao24} уже существует. Пропускаем.")
                return

        # Добавляем новый самолёт в список словарей для сохранения
        data.append({
            'icao24': aeroplane.icao24,
            'callsign': aeroplane.callsign,
            'origin_country': aeroplane.origin_country,
            'velocity': aeroplane.velocity,
            'baro_altitude': aeroplane.baro_altitude
        })

        # Записываем обновлённые данные обратно в файл
        with open(self.__filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_aeroplanes(self, **criteria) -> List[Aeroplane]:
        """
        Получить список самолётов по критериям.
        Пример: get_aeroplanes(origin_country="Russia") вернёт все самолёты РФ.
        """
        try:
            with open(self.__filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

            # Преобразуем словари в объекты
        result = []
        for item in data:
            try:
                plane = Aeroplane(
                    icao24=item['icao24'],
                    callsign=item['callsign'],
                    origin_country=item['origin_country'],
                    velocity=item['velocity'],
                    baro_altitude=item['baro_altitude']
                )
                # Проверяем, подходит ли под критерии
                match = True
                for key, value in criteria.items():
                    if getattr(plane, key, None) != value:
                        match = False
                        break
                if match:
                    result.append(plane)
            except KeyError:
                continue
        return result

    def delete_aeroplane(self, icao24: str) -> None:
        """Удалить информацию о самолёте по его идентификатору"""
        try:
            with open(self.__filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Файл не найден или пуст. Удалять нечего.")
            return

            # Фильтруем список, оставляя только те, у которых icao24 не совпадает
        new_data = [item for item in data if item.get('icao24') != icao24]

        if len(new_data) == len(data):
            print(f"Самолёт с icao24 {icao24} не найден.")
            return

        # Записываем обновлённый список обратно
        with open(self.__filename, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)
        print(f"Самолёт с icao24 {icao24} удалён.")
