from datetime import date


def date_validate(value):
    print(value)
    try:
        date.fromisoformat(str(value))
    except:
        raise TypeError("некорректная дата")
