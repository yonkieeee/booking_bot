import re
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from datetime import datetime

def find_symbol(s: str) -> bool:
    symbol = set('.,!@#$%^*()_+\'+=`~;"?/<>?\\/')
    return any(char in symbol for char in s)


def check_fullname(full_name: str) -> bool:

    cyrillic_pattern = re.compile(r'^[\u0400-\u04FF]+$')

    if find_symbol(full_name):
        return False
    count = 0
    if len(full_name.split()) == 2:
        for i in full_name.split():
            try:
                if not cyrillic_pattern.match(i):  # Перевірка на кирилицю
                    return False
                count += 1
                print(count)
            except LangDetectException:
                return False
        if count == 2:
            return True
    else:
        return False
    return False

def check_age_num(s: str) -> bool:
    if len(s) == 10 and s[2] == '.' and s[5] == '.':

        day = s[0:2]
        month = s[3:5]
        year = s[6:10]

        print(day, month, year)
        print(datetime.now().year)

        if day.isdigit() and month.isdigit() and year.isdigit():

            if year == "1488":
                return False

            if 1 <= int(day) <= 31 and 1 <= int(month) <= 12 and int(datetime.now().year) >= int(year):
                try:
                    datetime(int(year), int(month), int(day))
                    return True
                except ValueError:
                    return False


    return False