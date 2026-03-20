from src.aeroplanes_api import AeroplanesAPI


# ---- Вспомогательная функция для мока ----
def mock_nominatim_response(*args, **kwargs):
    """Заглушка для запроса к Nominatim"""

    class MockResponse:
        def json(self):
            return [{"boundingbox": ["40.0", "50.0", "-10.0", "10.0"]}]

        @property
        def status_code(self):
            return 200

    return MockResponse()


def mock_opensky_response(*args, **kwargs):
    """Заглушка для запроса к OpenSky"""

    class MockResponse:
        def json(self):
            return {"states": [
                ["abc123", "TEST", "Russia", None, None, 10.0, 20.0, 5000.0, False, 200.0,
                 None, None, None, None, None, None, 0]]}

        @property
        def status_code(self):
            return 200

    return MockResponse()


# ---- Тесты ----
def test_get_aeroplanes_returns_dict(monkeypatch):
    """Тест с подменой реального API на мок"""
    # Подменяем оба запроса
    monkeypatch.setattr("requests.get", mock_nominatim_response)

    api = AeroplanesAPI()
    result = api.get_aeroplanes("Spain")
    assert result is not None
    assert isinstance(result, dict)


def test_get_aeroplanes_nonexistent_country(monkeypatch):
    """Тест для несуществующей страны (Nominatim возвращает пустой список)"""

    def mock_empty(*args, **kwargs):
        class MockResponse:
            def json(self):
                return []  # пустой ответ = страна не найдена

            @property
            def status_code(self):
                return 200

        return MockResponse()

    monkeypatch.setattr("requests.get", mock_empty)
    api = AeroplanesAPI()
    result = api.get_aeroplanes("Атлантида")
    assert result is None


def test_api_attributes():
    """Тест атрибутов экземпляра API"""
    api = AeroplanesAPI()
    assert hasattr(api, 'openstreetmap_url')
    assert hasattr(api, 'opensky_url')
    assert hasattr(api, 'aeroplanes')
    assert api.aeroplanes is None


def test_aeroplanes_initial_none():
    """Тест: при создании экземпляра aeroplanes должен быть None"""
    api = AeroplanesAPI()
    assert api.aeroplanes is None
