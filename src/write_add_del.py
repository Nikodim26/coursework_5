import json

from src.airplane import Airplane
from src.working_with_files import WorkingWithFiles


class WriteAddDel(WorkingWithFiles):
    """Класс для объекта, оперирующего с данными в файле"""

    def __init__(self, file: str) -> None:
        super().__init__(file)

    def reading_by_criteria(self, criteria: list) -> list:
        """Получает информацию о самолетах по критериям"""

        try:
            with open(self.path_file, "r", encoding="utf-8") as f:
                data = json.load(f)

                result = data if criteria[0] == "All" else [dt for dt in data if dt["Country"] == criteria[0]]

                result = sorted(result, key=lambda x: x["Velocity"], reverse=True)

                if criteria[1] != "All" and len(result) > int(criteria[1]):
                    result = result[: int(criteria[1])]

                if criteria[2] != "All":
                    result = [
                        dt
                        for dt in result
                        if dt["Altitude"] <= int(criteria[2]) and dt["Velocity"] <= int(criteria[2])
                    ]

                return result

        except Exception:
            print("Ошибка чтения файла данных")

        return []

    def write_file_add(self, airplane: Airplane) -> None:
        """Добавляет информацию о новом самолете в файл"""

        try:
            airplane_ = {
                "ICAO24": airplane.ICAO24,
                "Country": airplane.Country_of_registration,
                "Velocity": airplane.velocity,
                "Altitude": airplane.geo_altitude,
            }

            with open(self.path_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if airplane_ not in data:
                data.append(airplane_)
            else:
                raise ValueError("Есть уже такой самолет")

            with open(self.path_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print("Добавлена информация о новом самолете\n")

        except ValueError as e:
            print(e)

        except Exception as e:
            print(e)

    def remove_from_file(self, criteria: list) -> None:
        """Удаляет данные о самолетах определенных стран регистрации"""

        with open(self.path_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        data = [dt for dt in data if not dt["Country"] in criteria]

        with open(self.path_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
