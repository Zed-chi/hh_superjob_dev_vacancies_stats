import requests
import os
import datetime
from dotenv import load_dotenv
from pprint import pprint
from utils import get_average_salary


def fetch_vacancies_page(
    keyword=None,
    secret=None,
    period=None,
    page=0
):
    vacancies_api = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": secret,
    }
    params = {
        "keyword": keyword,
        "town": 4,
        "date_published_from": period,
        "catalogues": 48,
        "count": 20,
        "page": page,
    }
    res = requests.get(vacancies_api, headers=headers, params=params)
    if res.ok:
        return res.json()
    else:
        print(res.text)
        return None


def get_token():
    auth_api = "https://api.superjob.ru/2.0/oauth2/password/"
    payload = {
        "login": os.getenv("sj_login"),
        "password": os.getenv("sj_pass"),
        "client_id": os.getenv("sj_id"),
        "client_secret": os.getenv("sj_secret"),
    }
    res = requests.get(auth_api, params=payload)
    if res.ok:
        return res.json()["access_token"]
    else:
        print(res.text)
        return None


def predict_rub_salary_for_SuperJob(vacancy):
    if "currency" in vacancy and vacancy["currency"] is not "rub":
        return None
    sal_from = vacancy.get("payment_from")
    sal_to = vacancy.get("payment_to")
    return get_average_salary(sal_from, sal_to)


def fetch_all_vacancies_pages(keyword=None, secret=None, period=None):
    vacancies = fetch_vacancies_page(
        keyword=keyword,
        secret=secret,
        period=period,
    )
    pages_count = int(vacancies["total"]) // 20
    for page in range(1, pages_count):
        response = fetch_vacancies_page(keyword, secret, period, page=page)
        vacancies["objects"] += response["objects"]
    return vacancies


def get_vacancies_stats(vacancies):
    job_salaries = tuple(
        filter(
            lambda x: x is not None,
            map(
                predict_rub_salary_for_SuperJob,
                vacancies["objects"]
            )
        )
    )
    if len(job_salaries) > 0:
        avg = sum(job_salaries) // len(job_salaries)
    else:
        avg = 0
    stats = {}
    stats["vacancies_found"] = vacancies["total"]
    stats["vacancies_processed"] = len(job_salaries)
    stats["avg_salary"] = avg
    return stats


def get_langs_stats(langs, period):
    load_dotenv()
    secret = os.getenv("sj_secret")
    period = (datetime.datetime.today() - datetime.timedelta(period)).timestamp()
    stats = {}
    for lang in langs:
        vacancies_by_lang = fetch_all_vacancies_pages(
            keyword=lang,
            secret=secret,
            period=period
        )
        vacancies_stats = get_vacancies_stats(vacancies_by_lang)
        stats[lang] = vacancies_stats
    return stats


def main():
    langs = [
        "python", "java", "fortran", "c#",
        "c++", "rust", "coffeescript", "js",
        "erlang", "elixir", "haskell", "scala",
        "1c", "php", "ruby", "go", "crystal",
    ]
    load_dotenv()
    key = os.getenv("sj_secret")
    period = 1
    lang_stats = get_langs_stats(langs, period)
    pprint(lang_stats)


if __name__ == "__main__":
    main()
