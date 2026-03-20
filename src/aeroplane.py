class Aeroplane:
    """Класс для работы с информацией о самолетах"""

    __slots__ = ('__icao24', '__callsign', '__origin_country', '__velocity', '__baro_altitude')

    def __init__(self, icao24, callsign, origin_country, velocity, baro_altitude):
        # ---- Валидация ----
        # icao24: непустая строка
        if not icao24 or not isinstance(icao24, str):
            raise ValueError("icao24 должен быть непустой строкой")

        # callsign: строка (может быть пустой)
        if callsign is not None and not isinstance(callsign, str):
            raise ValueError("callsign должен быть строкой или None")
        # Или если None вообще недопустим:
        if not isinstance(callsign, str):
            raise ValueError("callsign должен быть строкой")

        # origin_country: непустая строка
        if not origin_country or not isinstance(origin_country, str):
            raise ValueError("origin_country должен быть непустой строкой")

        # velocity: число >= 0 (может быть None, если скорость неизвестна)
        if velocity is not None:
            if not isinstance(velocity, (int, float)) or velocity < 0:
                raise ValueError("velocity должен быть числом >= 0")

        # baro_altitude: число (может быть None, если высота неизвестна)
        if baro_altitude is not None:
            if not isinstance(baro_altitude, (int, float)):
                raise ValueError("baro_altitude должен быть числом")

        # ---- Присваивание ----
        self.__icao24 = icao24                # уникальный идентификатор
        self.__callsign = callsign            # позывной (может быть пустым)
        self.__origin_country = origin_country  # страна регистрации
        self.__velocity = velocity            # горизонтальная скорость (м/с)
        self.__baro_altitude = baro_altitude  # барометрическая высота (м)

    # ---- Геттеры ----
    @property
    def icao24(self):
        """Возвращает уникальный идентификатор борта"""
        return self.__icao24

    @property
    def callsign(self):
        """Возвращает позывной рейса"""
        return self.__callsign

    @property
    def origin_country(self):
        """Возвращает страну регистрации воздушного судна"""
        return self.__origin_country

    @property
    def velocity(self):
        """Возвращает горизонтальную скорость (м/с)"""
        return self.__velocity

    @property
    def baro_altitude(self):
        """Возвращает барометрическую высоту (м)"""
        return self.__baro_altitude

    # ---- Методы сравнения самолетов ----
    # Позволяют использовать операторы <, >, == для объектов Aeroplane.
    # Сравнение происходит сначала по скорости, а если она равна — по высоте.

    def __lt__(self, other):
        """Меньше (<): сравниваем по скорости, при равенстве — по высоте"""
        if self.__velocity != other.__velocity:
            return self.__velocity < other.__velocity
        return self.__baro_altitude < other.__baro_altitude

    def __gt__(self, other):
        """Больше (>): сравниваем по скорости, при равенстве — по высоте"""
        if self.__velocity != other.__velocity:
            return self.__velocity > other.__velocity
        return self.__baro_altitude > other.__baro_altitude

    def __eq__(self, other):
        """Равно (==): сравниваем и скорость, и высоту"""
        return self.__velocity == other.__velocity and self.__baro_altitude == other.__baro_altitude
