# -*- coding: utf-8 -*-

# Есть файл с протоколом регистраций пользователей на сайте - registrations.txt
# Каждая строка содержит: ИМЯ ЕМЕЙЛ ВОЗРАСТ, разделенные пробелами
# Например:
# Василий test@test.ru 27
#
# Надо проверить данные из файла, для каждой строки:
# - присутсвуют все три поля
# - поле имени содержит только буквы
# - поле емейл содержит @ и .
# - поле возраст является числом от 10 до 99
#
# В результате проверки нужно сформировать два файла
# - registrations_good.log для правильных данных, записывать строки как есть
# - registrations_bad.log для ошибочных, записывать строку и вид ошибки.
#
# Для валидации строки данных написать метод, который может выкидывать исключения:
# - НЕ присутсвуют все три поля: ValueError
# - поле имени содержит НЕ только буквы: NotNameError (кастомное исключение)
# - поле емейл НЕ содержит @ и .(точку): NotEmailError (кастомное исключение)
# - поле возраст НЕ является числом от 10 до 99: ValueError
# Вызов метода обернуть в try-except.

class CustomError(Exception):
    pass


class NotNameError(CustomError):
    pass


class NotEmailError(CustomError):
    pass


def validation_line(line):
    if ' ' not in line or line.count(' ') < 2:
        raise ValueError('Не все поля данных присутствуют')
    name, email, age = line.split()
    if not name.isalpha():
        raise NotNameError('Имя содержит не только буквы')
    elif ('@' or '.') not in email:
        raise NotEmailError('Емайл не содержит символов @ или .')
    elif not age.isdigit():
        raise ValueError('Возраст не является числом или не соответсвует критерию от 10 до 99')
    elif not 10 < int(age) < 99:
        raise ValueError('Возраст не соответсвует критерию от 10 до 99')
    else:
        with open('registrations_good_log.txt', 'a', encoding='utf8') as fgr:
            fgr.write(line)


def rec_bed(line, exc):
    with open('registrations_bad_log.txt', 'a', encoding='utf8') as fbr:
            fbr.write(line.strip() + ' ' + str(exc) + '\n')


with open('registrations.txt', 'r', encoding='utf8') as fi:
    for line in fi:
        try:
            reg = validation_line(line)
        except ValueError as exc:
            rec_bed(line, exc)
        except NotEmailError as exc:
            rec_bed(line, exc)
        except NotNameError as exc:
            rec_bed(line, exc)




