from src.aeroplanes_api import AeroplanesAPI
from src.aeroplane import Aeroplane
from src.file_airinfo import JSONSaver

def user_interaction():
    api = AeroplanesAPI()
    saver = JSONSaver()

    print("=== Трекер самолётов ===")

    # 1. Ввод страны
    country = input("Введите название страны (например, Russia): ").strip()
    if not country:
        print("Страна не введена. Выход.")
        return

    # 2. Получаем данные от API
    print(f"Ищу самолёты над {country}...")
    data = api.get_aeroplanes(country)
    if not data or 'states' not in data:
        print("Не удалось получить данные от OpenSky.")
        return

    # 3. Преобразуем сырые данные в список объектов Aeroplane
    aeroplanes = []
    for state in data['states']:
        if state is None:
            continue
        try:
            # Порядок полей: https://openskynetwork.github.io/opensky-api/rest.html#response
            plane = Aeroplane(
                icao24=state[0],
                callsign=state[1].strip() if state[1] else "N/A",
                origin_country=state[2],
                velocity=state[9],
                baro_altitude=state[7]
            )
            aeroplanes.append(plane)
        except (IndexError, ValueError, TypeError):
            continue

    print(f"Найдено самолётов: {len(aeroplanes)}")

    # 4. Сохраняем в файл
    for plane in aeroplanes:
        saver.add_aeroplane(plane)

    # 5. Меню пользователя
    while True:
        print("\nВыберите действие:")
        print("1. Показать топ N самолётов по высоте")
        print("2. Показать самолёты по стране регистрации")
        print("3. Выход")
        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            try:
                n = int(input("Введите количество самолётов для топа: "))
                # Сортируем по высоте (от большей к меньшей)
                sorted_planes = sorted(aeroplanes, key=lambda pl: pl.baro_altitude or 0, reverse=True)
                top = sorted_planes[:n]
                print(f"\nТоп-{n} самолётов по высоте:")
                for i, p in enumerate(top, 1):
                    alt = p.baro_altitude if p.baro_altitude is not None else "N/A"
                    print(f"{i}. {p.callsign} ({p.origin_country}) – {alt} м")
            except ValueError:
                print("Ошибка: введите целое число.")

        elif choice == "2":
            country_filter = input("Введите страну регистрации (например, Russia): ").strip()
            filtered = [p for p in aeroplanes if p.origin_country.lower() == country_filter.lower()]
            print(f"\nНайдено самолётов из {country_filter}: {len(filtered)}")
            for p in filtered:
                alt = p.baro_altitude if p.baro_altitude is not None else "N/A"
                print(f"- {p.callsign} – {alt} м")

        elif choice == "3":
            print("Выход.")
            break
        else:
            print("Неверный выбор, попробуйте снова.")

if __name__ == "__main__":
    user_interaction()
    