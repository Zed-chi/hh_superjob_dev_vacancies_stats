from hh_vacs import get_langs_stats as hh_stats
from superjob_vacs import get_langs_stats as sj_stats
from terminaltables import DoubleTable


def get_table_from_stats(stats):
    data = [
        (
            "Language", "Vacancies founded",
            "Vacancies Processed", "Average salary"
        ),
    ]
    for key in stats.keys():
        lang = [
            key,
            stats[key]["vacancies_found"],
            stats[key]["vacancies_processed"],
            stats[key]["avg_salary"],
        ]
        data.append(lang)
    return data


def main():
    langs = [
        "python", "java", "fortran", "c#",
        "c++", "rust", "coffeescript", "js",
        "erlang", "elixir", "haskell", "scala",
        "1c", "php", "ruby", "go", "crystal",
    ]
    period = 30
    hh_tbl = get_table_from_stats(hh_stats(langs, period))
    hhtable_instance = DoubleTable(
        hh_tbl,
        "|hh.ru programming vacancies statistics - Moskow|"
    )
    hhtable_instance.justify_columns[5] = "right"

    sj_tbl = get_table_from_stats(sj_stats(langs, period))
    sjtable_instance = DoubleTable(
        sj_tbl,
        "|Superjob programming vacancies statistics - Moskow|"
    )
    sjtable_instance.justify_columns[5] = "right"
    print(hhtable_instance.table)
    print()
    print(sjtable_instance.table)


if __name__ == "__main__":
    main()
