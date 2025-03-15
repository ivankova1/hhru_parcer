from db_manager import DBManager
from api_handler import HHAPIHandler
import config

def main():
    # Создание экземпляров классов
    api_handler = HHAPIHandler()
    db_manager = DBManager(config.DB_NAME, config.DB_USER, config.DB_PASSWORD)

    # Получение данных о компаниях и их вакансиях через API
    companies_ids = [15478, 3529, 660, 11229, 78638, 1538, 3043, 1740, 1130413, 4072]
    companies_data = api_handler.get_companies_and_vacancies(companies_ids)

    # Загрузка данных в базу данных
    db_manager.create_database()
    db_manager.insert_data(companies_data)

    # Интерфейс взаимодействия с пользователем
    while True:
        print("\nВыберите действие:")
        print("1. Список всех компаний и количество вакансий у каждой")
        print("2. Список всех вакансий с деталями")
        print("3. Средняя зарплата по вакансиям")
        print("4. Вакансии с зарплатой выше средней")
        print("5. Поиск вакансий по ключевому слову")
        print("0. Выход")

        choice = input("Введите номер действия: ")

        if choice == "1":
            result = db_manager.get_companies_and_vacancies_count()
            for row in result:
                print(f"Компания: {row[0]}, Вакансий: {row[1]}")

        elif choice == "2":
            result = db_manager.get_all_vacancies()
            for row in result:
                print(f"Компания: {row[0]}, Вакансия: {row[1]}, Зарплата: {row[2]}, Ссылка: {row[3]}")

        elif choice == "3":
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата: {avg_salary}")

        elif choice == "4":
            result = db_manager.get_vacancies_with_higher_salary()
            for row in result:
                print(f"Вакансия: {row[0]}, Зарплата: {row[1]}")

        elif choice == "5":
            keyword = input("Введите ключевое слово: ")
            result = db_manager.get_vacancies_with_keyword(keyword)
            for row in result:
                print(f"Вакансия: {row[0]}, Компания: {row[1]}")

        elif choice == "0":
            print("Выход из программы.")
            break

if __name__ == "__main__":
    main()