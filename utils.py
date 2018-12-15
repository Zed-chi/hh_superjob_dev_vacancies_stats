def get_average_salary(sal_from, sal_to):
    if sal_from and sal_to:
        avg = (sal_from + sal_to) / 2
    elif sal_from:
        avg = (sal_from) * 1.2
    elif sal_to:
        avg = int(sal_to) * 0.8
    else:
        avg = None
    return avg