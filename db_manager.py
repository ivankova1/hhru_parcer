import psycopg2
from typing import List, Tuple

class DBManager:
    def __init__(self, db_name: str, user: str, password: str):
        self.connection = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host="localhost",
            port="5432"
        )
        self.cursor = self.connection.cursor()

    def create_database(self):
        """Создание таблиц в базе данных"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                company_id INTEGER REFERENCES companies(id),
                title VARCHAR(255) NOT NULL,
                salary INTEGER,
                url VARCHAR(255) NOT NULL
            );
        """)
        self.connection.commit()

    def insert_data(self, data: List[Tuple]):
        """Заполнение таблиц данными"""
        for company, vacancies in data.items():
            self.cursor.execute("INSERT INTO companies (name) VALUES (%s) RETURNING id;", (company,))
            company_id = self.cursor.fetchone()[0]

            for vacancy in vacancies:
                self.cursor.execute("""
                    INSERT INTO vacancies (company_id, title, salary, url)
                    VALUES (%s, %s, %s, %s);
                """, (company_id, vacancy["title"], vacancy["salary"], vacancy["url"]))

        self.connection.commit()

    def get_companies_and_vacancies_count(self) -> List[Tuple]:
        """Получение списка компаний и количества вакансий"""
        self.cursor.execute("""
            SELECT c.name, COUNT(v.id) 
            FROM companies c 
            LEFT JOIN vacancies v ON c.id = v.company_id 
            GROUP BY c.name;
        """)
        return self.cursor.fetchall()

    def get_all_vacancies(self) -> List[Tuple]:
        """Получение списка всех вакансий"""
        self.cursor.execute("""
            SELECT c.name, v.title, v.salary, v.url 
            FROM companies c 
            JOIN vacancies v ON c.id = v.company_id;
        """)
        return self.cursor.fetchall()

    def get_avg_salary(self) -> float:
        """Получение средней зарплаты"""
        self.cursor.execute("SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL;")
        return self.cursor.fetchone()[0] or 0

    def get_vacancies_with_higher_salary(self) -> List[Tuple]:
        """Получение вакансий с зарплатой выше средней"""
        avg_salary = self.get_avg_salary()
        self.cursor.execute("""
            SELECT title, salary 
            FROM vacancies 
            WHERE salary > %s;
        """, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple]:
        """Поиск вакансий по ключевому слову"""
        self.cursor.execute("""
            SELECT title, c.name 
            FROM vacancies v 
            JOIN companies c ON v.company_id = c.id 
            WHERE title ILIKE %s;
        """, (f"%{keyword}%",))
        return self.cursor.fetchall()

    def close_connection(self):
        """Закрытие соединения с базой данных"""
        self.connection.close()