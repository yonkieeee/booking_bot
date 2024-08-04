def find_symbol(s: str) -> bool:
    symbol = set('.,!@#$%^*()_+\'+=`~;"?/<>?\\/')
    return any(char in symbol for char in s)


def check_age_num(s: str) -> bool:
    if s[2] == '.' and s[5] == '.':
        return True
