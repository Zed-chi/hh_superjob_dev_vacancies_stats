import requests
from pprint import pprint


def fetch_all_vacancies_pages(keyword=None, period=None):
    all_pages = fetch_vacancies_page(keyword=keyword, period=period)
    total_pages = all_pages["pages"]
    for page in range(1, total_pages):
        response = fetch_vacancies_page(
            keyword=keyword,
            period=period,
            page=page
        )
        all_pages["items"] += response["items"]
    return all_pages


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
    if "salary" not in vacancy or not vacancy["salary"]:
        return None
    if "currency" in vacancy["salary"] and \
    vacancy["salary"]["currency"] != "RUR":
        avg = None
    if "from" in vacancy["salary"]:
        sal_from = vacancy["salary"]["from"]
    else:
        sal_from = None
    sal_to = vacancy["salary"]["to"] if "to" in vacancy["salary"] else None
    if sal_from and sal_to:
        avg = (sal_from + sal_to) / 2
    elif sal_from:
        avg = (sal_from) * 1.2
    elif sal_to:
        avg = int(sal_to) * 0.8
    else:
        avg = None
    return avg


def get_job_stats(pages):
    vacs = pages["items"]
    job_salaries = tuple(
        filter(
            lambda x: x is not None,
            map(
                predict_rub_salary,
                vacs
            )
        )
    )
    if len(job_salaries) > 0:
        avg = sum(job_salaries) // len(job_salaries)
    else:
        avg = 0
    stats = {}
    stats["vacancies_found"] = pages["found"]
    stats["vacancies_processed"] = len(job_salaries)
    stats["avg_salary"] = avg
    return stats


def get_langs_stats(langs, period):
    stats = {}
    for lang in langs:
        lang_pages = fetch_all_vacancies_pages(
            keyword=lang,
            period=period
        )
        lang_stats = get_job_stats(lang_pages)
        stats[lang] = lang_stats
    return stats


if __name__ == "__main__":
    langs = [
        "python", "java", "fortran", "c#",
        "c++", "rust", "coffeescript", "js",
        "erlang", "elixir", "haskell", "scala",
        "1c", "php", "ruby", "go", "crystal",
    ]
    langs2 = [
        "python", "java", "fortran", "c#",
    ]
    period = 1
    pprint(get_langs_stats(langs2, period))
