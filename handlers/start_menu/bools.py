from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException


def find_symbol(s: str) -> bool:
    symbol = set('.,!@#$%^*()_+\'+=`~;"?/<>?\\/')
    return any(char in symbol for char in s)


def check_fullname(full_name: str) -> bool:
    if find_symbol(full_name):
        return False
    count = 0
    if len(full_name.split()) == 2:
        for i in full_name.split():
            try:
                lang = detect(i)

                print(i, lang)
                if lang not in ['uk', 'ru']:
                    return False
                else:
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

        if day.isdigit() and month.isdigit() and year.isdigit():
            return True

    return False
