from random import randint

MAX_NUMBER = 9
MIN_NUMBER = 1
QUONTITY_NUM = 4

_wish_number = []
_bulls_cows = {'bulls': 0, 'cows': 0}

def make_wish_num():
    global _wish_number
    _wish_number = []
    _wish_number.append(randint(MIN_NUMBER, MAX_NUMBER))
    for pos in range(1,QUONTITY_NUM):
        while True:
            ran_num = randint(0, MAX_NUMBER)
            if ran_num not in _wish_number:
                _wish_number.append(ran_num)
                break
    print(*_wish_number)


def check_num(user_num):
    _bulls_cows['bulls'], _bulls_cows['cows'] = 0, 0
    for pos,elem in enumerate(user_num):
        elem = int(elem)
        if elem == _wish_number[pos]:
            _bulls_cows['bulls'] += 1
        else:
            if elem in _wish_number:
                _bulls_cows['cows'] +=1

    return _bulls_cows

def check_input(user_num):
    if len(user_num) == QUONTITY_NUM:
        for elem in user_num:
            if elem in '0123456789':
                continue
            else:
                return False

        return True
    else:
        return False
