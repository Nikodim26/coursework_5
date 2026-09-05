import json

from src.airplane import Airplane
from src.api_airplanes import ApiAeroplanes
from src.api_coord import ApiCoord
from src.utils import translate_text
from src.utils import write_file
from src.write_add_del import WriteAddDel


def working_with_the_user() -> None:
    """Предоставляет диалог с пользователем"""

    # Подготавливаем данные из API
    while True:
        country = input("Укажите страну, в пространстве которой идет поиск самолетов: ")
        api_coord = ApiCoord(country)
        coordinates = api_coord.coordinates
        if coordinates:
            break
        print("Нет сведений")

    api_aeroplanes = ApiAeroplanes(coordinates)

    write_file("aeroplanes.json", api_aeroplanes.list_info)

    # Начинаем работать с данными
    write_add_del = WriteAddDel("aeroplanes.json")  # Создаем рабочий объект

    # Удаляем данные
    response = input("Хотите удалить самолеты некоторых стран (да/нет)? [НЕТ]")

    if not (response == "" or response.lower() == "нет"):
        criterion = input("Введите данные через запятую (страна,страна ...): ").split(",")
        criterion = [translate_text(i) for i in criterion]

        write_add_del.remove_from_file(criterion)

    # Читаем данные
    criterion = []
    while True:
        country = input("Самолеты какой страны показать (все/страна)? [ВСЕ]: ")
        criterion.append(translate_text(country) if country != "" else "All")

        quantity = input("Какое количество самых быстрых самолетов показать (все/N)? [ВСЕ]: ")
        criterion.append(quantity if quantity != "" else "All")

        velocity = input("Укажите максимальную скорость (все/скорость,м/с)? [ВСЕ]: ")
        criterion.append("All" if velocity == "" else velocity)

        height = input('Укажите "потолок" (все/высота,м)? [ВСЕ]: ')
        criterion.append("All" if height == "" else height)

        airplanes = write_add_del.reading_by_criteria(criterion)

        if airplanes:
            print(json.dumps(airplanes, indent=4), "\n")
            break
        print("Нет сведений")

    # Добавляем данные
    response = input("Хотите добавить свой самолет в общий список (да/нет)? [ДА]")

    if response == "" or response.lower() == "да":
        characteristics = (
            input("Введите данные через запятую " "(номер,страна,скорость м/с,высота м): ").replace(" ", "").split(",")
        )

        characteristics = [(float(i) if i[0].isdigit() else i) for i in characteristics]

        write_add_del.write_file_add(Airplane(*characteristics))

    # Получаем из общего списка без удаленных специально
    response = input("Показать наиболее быстрый и высоколетящий самолет (да/нет)? [ДА]")

    if response == "" or response.lower() == "да":

        airplane_max = Airplane(" ", " ", 0, 0)
        airplanes_data = write_add_del.reading_by_criteria(["All", "All", "All", "All"])

        for dt in airplanes_data:
            airplane = Airplane(dt["ICAO24"], dt["Country"], dt["Velocity"], dt["Altitude"])
            if airplane > airplane_max:
                airplane_max = airplane

        print("Самый быстрый и высоколетящий самолет")
        print(airplane_max)

    response = input("Показать самолеты на земле (да/нет)? [ДА]")

    if response == "" or response.lower() == "да":
        print("Самолеты на земле")
        print(json.dumps(write_add_del.reading_by_criteria(["All", "All", 0, 0]), indent=4))


if __name__ == "__main__":
    working_with_the_user()
