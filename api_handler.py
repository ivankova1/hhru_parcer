import requests
from typing import Dict, List

class HHAPIHandler:
    BASE_URL = "https://api.hh.ru"

    def get_companies_and_vacancies(self, company_ids: List[int]) -> Dict[str, List[Dict]]:
        """Получение данных о компаниях и их вакансиях"""
        companies_data = {}

        for company_id in company_ids:
            # Получаем информацию о компании
            company_url = f"{self.BASE_URL}/employers/{company_id}"
            response = requests.get(company_url)
            if response.status_code == 200:
                company_name = response.json().get("name")

                # Получаем список вакансий компании
                vacancies_url = f"{self.BASE_URL}/vacancies?employer_id={company_id}"
                vacancies_response = requests.get(vacancies_url)
                if vacancies_response.status_code == 200:
                    vacancies = [
                        {
                            "title": vac.get("name"),
                            "salary": vac.get("salary", {}).get("from") if vac.get("salary") else None,
                            "url": vac.get("alternate_url")
                        }
                        for vac in vacancies_response.json().get("items", [])
                    ]
                    companies_data[company_name] = vacancies

        return companies_data