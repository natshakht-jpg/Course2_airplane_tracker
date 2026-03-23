import os

from src.aeroplane import Aeroplane
from src.file_airinfo import JSONSaver


def test_add_and_get():
    filename = "test_aeroplanes.json"
    saver = JSONSaver(filename)
    plane = Aeroplane("test123", "TST", "Testland", 300.0, 9000.0)
    saver.add_aeroplane(plane)
    result = saver.get_aeroplanes(origin_country="Testland")
    assert len(result) == 1
    assert result[0].icao24 == "test123"
    os.remove(filename)


def test_no_duplicates():
    filename = "test_duplicates.json"
    saver = JSONSaver(filename)
    plane1 = Aeroplane("dup123", "DUP", "Dupville", 300.0, 9000.0)
    plane2 = Aeroplane("dup123", "DUP", "Dupville", 400.0, 9500.0)
    saver.add_aeroplane(plane1)
    saver.add_aeroplane(plane2)
    result = saver.get_aeroplanes()
    assert len(result) == 1
    os.remove(filename)


def test_get_aeroplanes_empty_file():
    filename = "test_empty.json"
    saver = JSONSaver(filename)
    result = saver.get_aeroplanes()
    assert result == []
    if os.path.exists(filename):
        os.remove(filename)


def test_get_aeroplanes_with_criteria():
    filename = "test_criteria.json"
    saver = JSONSaver(filename)
    plane1 = Aeroplane("c1", "C1", "Russia", 300.0, 9000.0)
    plane2 = Aeroplane("c2", "C2", "USA", 400.0, 10000.0)
    plane3 = Aeroplane("c3", "C3", "Russia", 350.0, 9500.0)
    saver.add_aeroplane(plane1)
    saver.add_aeroplane(plane2)
    saver.add_aeroplane(plane3)
    russian = saver.get_aeroplanes(origin_country="Russia")
    assert len(russian) == 2
    os.remove(filename)


def test_delete_nonexistent():
    filename = "test_delete_none.json"
    saver = JSONSaver(filename)
    plane = Aeroplane("d1", "D1", "Test", 100.0, 5000.0)
    saver.add_aeroplane(plane)
    saver.delete_aeroplane("nonexistent")
    result = saver.get_aeroplanes()
    assert len(result) == 1
    assert result[0].icao24 == "d1"
    os.remove(filename)


def test_add_corrupted_data():
    filename = "test_corrupted.json"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("это не json")
    saver = JSONSaver(filename)
    plane = Aeroplane("good", "G", "Test", 200.0, 6000.0)
    saver.add_aeroplane(plane)
    result = saver.get_aeroplanes()
    assert len(result) == 1
    assert result[0].icao24 == "good"
    os.remove(filename)


def test_get_from_missing_file():
    saver = JSONSaver("missing.json")
    result = saver.get_aeroplanes()
    assert result == []


def test_delete_from_missing_file():
    saver = JSONSaver("missing.json")
    saver.delete_aeroplane("any")


def test_json_saver_custom_filename():
    custom_name = "custom_data.json"
    saver = JSONSaver(custom_name)
    plane = Aeroplane("test", "TST", "Test", 100.0, 5000.0)
    saver.add_aeroplane(plane)
    assert os.path.exists(custom_name)
    os.remove(custom_name)


def test_add_aeroplane_duplicate_handling():
    """Тест обработки дубликатов при добавлении"""
    filename = "test_duplicate_add.json"
    saver = JSONSaver(filename)
    plane = Aeroplane("dup", "DUP", "Test", 100.0, 5000.0)
    saver.add_aeroplane(plane)
    # Попытка добавить тот же самолёт снова (должна быть заглушка или пропуск)
    saver.add_aeroplane(plane)  # проверим, что не упало
    result = saver.get_aeroplanes()
    assert len(result) == 1  # или как реализовано
    os.remove(filename)


def test_get_aeroplanes_with_empty_criteria():
    """Тест получения с пустыми критериями (должен вернуть все)"""
    filename = "test_empty_criteria.json"
    saver = JSONSaver(filename)
    plane1 = Aeroplane("p1", "P1", "A", 100.0, 5000.0)
    plane2 = Aeroplane("p2", "P2", "B", 200.0, 6000.0)
    saver.add_aeroplane(plane1)
    saver.add_aeroplane(plane2)
    result = saver.get_aeroplanes()  # без критериев
    assert len(result) == 2
    os.remove(filename)


def test_delete_aeroplane_multiple():
    """Тест удаления одного из нескольких самолётов"""
    filename = "test_delete_multiple.json"
    saver = JSONSaver(filename)
    plane1 = Aeroplane("d1", "D1", "Test", 100.0, 5000.0)
    plane2 = Aeroplane("d2", "D2", "Test", 200.0, 6000.0)
    saver.add_aeroplane(plane1)
    saver.add_aeroplane(plane2)
    saver.delete_aeroplane("d1")
    result = saver.get_aeroplanes()
    assert len(result) == 1
    assert result[0].icao24 == "d2"
    os.remove(filename)


def test_add_aeroplane_corrupted_file_again():
    """Тест добавления в битый JSON-файл (покрывает строки 55-57)"""
    filename = "corrupt_final.json"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("не json и не пусто")

    saver = JSONSaver(filename)
    plane = Aeroplane("final", "FIN", "Finaland", 400.0, 10000.0)
    saver.add_aeroplane(plane)  # должно перезаписать файл

    result = saver.get_aeroplanes()
    assert len(result) == 1
    assert result[0].icao24 == "final"
    os.remove(filename)


def test_delete_nonexistent_with_existing_file():
    """Тест удаления несуществующего самолёта из файла с данными (покрывает строки 108-109)"""
    filename = "test_delete_nonexistent.json"
    saver = JSONSaver(filename)
    plane = Aeroplane("exist", "EX", "Test", 100.0, 5000.0)
    saver.add_aeroplane(plane)

    # Пытаемся удалить несуществующий
    saver.delete_aeroplane("ghost")

    result = saver.get_aeroplanes()
    assert len(result) == 1
    assert result[0].icao24 == "exist"
    os.remove(filename)
