import requests
from pprint import pprint
from utils import get_average_salary


def fetch_all_vacancies_pages(keyword=None, period=None):
    vacancies = fetch_vacancies_page(keyword=keyword, period=period)
    pages_count = vacancies["pages"]
    for page in range(1, pages_count):
        response = fetch_vacancies_page(
            keyword=keyword,
            period=period,
            page=page
        )
        vacancies["items"] += response["items"]
    return vacancies


def fetch_vacancies_page(
    keyword=None,
    period=1,
    page=0
):
    vacancies_api = "https://api.hh.ru/vacancies?"
    params = {
        "text": keyword,
        "specialization": [1, 15, 12],
        "period": period,
        "area": 1,
        "currency": "RUR",
        "page": page,
        "per_page": 20,
    }
    res = requests.get(vacancies_api, params=params)
    return res.json()


def predict_rub_salary(vacancy):
    salary = vacancy.get("salary")
    if not salary:
        return None
    if "currency" in salary and salary["currency"] != "RUR":
        return None
    sal_from = salary.get("from")
    sal_to = salary.get("to")
    return get_average_salary(sal_from, sal_to)


def get_vacancies_stats(vacancies):
    job_salaries = tuple(
        filter(
            lambda x: x is not None,
            map(
                predict_rub_salary,
                vacancies["items"]
            )
        )
    )
    if len(job_salaries) > 0:
        avg = sum(job_salaries) // len(job_salaries)
    else:
        avg = 0
    stats = {}
    stats["vacancies_found"] = vacancies["found"]
    stats["vacancies_processed"] = len(job_salaries)
    stats["avg_salary"] = avg
    return stats


def get_langs_stats(langs, period):
    stats = {}
    for lang in langs:
        vacancies_by_lang = fetch_all_vacancies_pages(
            keyword=lang,
            period=period
        )
        vacancies_stats = get_vacancies_stats(vacancies_by_lang)
        stats[lang] = vacancies_stats
    return stats


if __name__ == "__main__":
    langs = [
        "python", "java", "fortran", "c#",
        "c++", "rust", "coffeescript", "js",
        "erlang", "elixir", "haskell", "scala",
        "1c", "php", "ruby", "go", "crystal",
    ]
    langs2 = [
        "python",
    ]
    period = 1
    pprint(get_langs_stats(langs2, period))
