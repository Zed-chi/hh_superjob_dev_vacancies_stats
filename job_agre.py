import requests
from pprint import pprint

# ()->full_req
def get_full_jobs_json(lang, with_salary):
    vacs = get_hh_vac_json(lang, with_salary=with_salary)
#    print("vacs len - {}".format(len(vacs["items"])))
    pages = vacs["pages"]
    for page in range(1,pages):
        print("\tpage {} loading".format(page))
        vacs["items"]+= get_hh_vac_json(
            lang,
            with_salary=with_salary,
            page=page
        )["items"]
#        print("vacs len - {}".format(len(vacs["items"])))
    return vacs

# (str)->part_req
def get_hh_vac_json(search_word, with_salary=False, page=0):
    pay = {
        "text": "Программист " + search_word,
        "specialization": [1, 15, 12],
        "period": 30,
        "area": 1,
        "only_with_salary": with_salary,
        "currency": "RUR",
        "page": page,
        "per_page": 5,
    }
    api = "https://api.hh.ru/vacancies?"
    res = requests.get(api, params=pay)
    return res.json()

# ([salaries])->[avg]
def predict_rub_salary(salary_list, keep_none=False):
    avgs = []
    for salary in salary_list:
        if salary["currency"] and salary["currency"] != "RUR":
            if keep_none:
                avgs.append(None)
            else:
                continue
        elif salary["from"] and salary["to"]:
            avgs.append((int(salary["from"]) + int(salary["to"])) / 2)
        elif salary["from"]:
            avgs.append(int(salary["from"]) * 1.2)
        elif salary["to"]:
            avgs.append(int(salary["to"]) * 0.8)
        else:
            if not non:
                continue
            else:
                avgs.append(None)
    return avgs


def get_job_count(languges):
    jobs = {}
    for lang in languges:
        print("=>{} vacancies start processing".format(lang))
        vacancies = get_full_jobs_json(lang, with_salary=True)
        sals = get_lang_salaries(vacs=vacancies["items"])
        avgs = predict_rub_salary(sals, keep_none=False)
        jobs[lang] = {}
        jobs[lang]["average_salary"] = sum(avgs) // len(avgs)
        jobs[lang]["vacancies_processed"] = len(avgs)
        jobs[lang]["vacancies_found"] = vacancies["found"]
        print("<={} vacancies processed\n".format(lang))
    return jobs

# res -> [{"from", "to", "cur", "gros"}...]
def get_lang_salaries(lang=None, vacs=None):
    jobs = []
    if not vacs and lang:
        vacs = get_hh_vac_json(lang, salary=True)["items"]
    elif not vacs and not lang:
        return []
    for vac in vacs:
        obj = {}
        if not "salary" in vac:
            continue
        if vac["salary"] and vac["salary"]["from"]:
            obj["from"] = vac["salary"]["from"]
        else:
            obj["from"] = None
        if vac["salary"] and vac["salary"]["to"]:
            obj["to"] = vac["salary"]["to"]
        else:
            obj["to"] = None
        if vac["salary"] and vac["salary"]["currency"]:
            obj["currency"] = vac["salary"]["currency"]
        else:
            obj["currency"] = None
        if vac["salary"] and vac["salary"]["gross"]:
            obj["gross"] = vac["salary"]["gross"]
        else:
            obj["gross"] = None
        jobs.append(obj)
    return jobs


if __name__ == "__main__":
    langs = [
        "python", "java", "fortran", "c#",
        "c++", "rust", "coffeescript", "js",
        "erlang", "elixir", "haskell", "scala",
        "1c", "php", "ruby","go", "crystal"
    ]
    langs2 = [
        "python", "java", "fortran", "c#",
    ]
    founded_jobs = sorted(
            get_job_count(langs2).items(),
            key=lambda x: x[1]["vacancies_found"],
            reverse=True,
    )
    #    vacancies = get_full_jobs_json("python", True)["items"]
    #    sals = get_lang_salaries(vacs=vacancies)
    #    avgs = predict_rub_salary(sals, keep_none=False)
    #    print(avgs)
    print(get_job_count(langs2))
    