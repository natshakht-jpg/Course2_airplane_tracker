import pytest

from src.aeroplane import Aeroplane


def test_aeroplane_creation():
    plane = Aeroplane("abc123", "SU123", "Russia", 250.0, 10000.0)
    assert plane.icao24 == "abc123"
    assert plane.callsign == "SU123"
    assert plane.origin_country == "Russia"
    assert plane.velocity == 250.0
    assert plane.baro_altitude == 10000.0


def test_invalid_icao24():
    with pytest.raises(ValueError):
        Aeroplane("", "SU123", "Russia", 250.0, 10000.0)


def test_comparison():
    p1 = Aeroplane("a", "A1", "X", 100.0, 5000.0)
    p2 = Aeroplane("b", "B2", "Y", 200.0, 6000.0)
    assert p1 < p2
    assert p2 > p1
    assert p1 != p2


def test_invalid_callsign():
    """Тест: callsign должен быть строкой (если не пустой)"""
    # Должно работать с пустым callsign
    plane = Aeroplane("abc", "", "Russia", 100.0, 5000.0)
    assert plane.callsign == ""

    # Недопустимый тип
    with pytest.raises(ValueError):
        Aeroplane("abc", 123, "Russia", 100.0, 5000.0)


def test_invalid_velocity():
    """Тест: отрицательная скорость вызывает ошибку"""
    with pytest.raises(ValueError):
        Aeroplane("abc", "SU", "Russia", -10.0, 5000.0)


def test_invalid_altitude_type():
    """Тест: высота должна быть числом"""
    with pytest.raises(ValueError):
        Aeroplane("abc", "SU", "Russia", 100.0, "десять тысяч")


def test_callsign_none():
    """Тест: передача None в callsign вызывает ошибку"""
    with pytest.raises(ValueError):
        Aeroplane("abc", None, "Russia", 100.0, 5000.0)


def test_comparison_edge_cases():
    """Тест сравнения с одинаковыми скоростями, но разной высотой"""
    p1 = Aeroplane("a", "A", "X", 100.0, 5000.0)
    p2 = Aeroplane("b", "B", "Y", 100.0, 6000.0)
    assert p1 < p2  # одинаковые скорости, сравниваем по высоте
    assert p2 > p1


def test_invalid_origin_country():
    """Тест: страна регистрации должна быть строкой"""
    with pytest.raises(ValueError):
        Aeroplane("abc", "SU", 123, 100.0, 5000.0)  # country не строка
