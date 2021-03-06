# -*- coding: utf-8 -*-

from termcolor import cprint
from random import randint

# Часть первая
#
# Создать модель жизни небольшой семьи.
#
# Каждый день участники жизни могут делать только одно действие.
# Все вместе они должны прожить год и не умереть.
#
# Муж может:
#   есть,
#   играть в WoT,
#   ходить на работу,
# Жена может:
#   есть,
#   покупать продукты,
#   покупать шубу,
#   убираться в доме,

# Все они живут в одном доме, дом характеризуется:
#   кол-во денег в тумбочке (в начале - 100)
#   кол-во еды в холодильнике (в начале - 50)
#   кол-во грязи (в начале - 0)
#
# У людей есть имя, степень сытости (в начале - 30) и степень счастья (в начале - 100).
#
# Любое действие, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Кушают взрослые максимум по 30 единиц еды, степень сытости растет на 1 пункт за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе чел умрет от голода.
#
# Деньги в тумбочку добавляет муж, после работы - 150 единиц за раз.
# Еда стоит 10 денег 10 единиц еды. Шуба стоит 350 единиц.
#
# Грязь добавляется каждый день по 5 пунктов, за одну уборку жена может убирать до 100 единиц грязи.
# Если в доме грязи больше 90 - у людей падает степень счастья каждый день на 10 пунктов,
# Степень счастья растет: у мужа от игры в WoT (на 20), у жены от покупки шубы (на 60, но шуба дорогая)
# Степень счастья не должна падать ниже 10, иначе чел умрает от депресии.
#
# Подвести итоги жизни за год: сколько было заработано денег, сколько сьедено еды, сколько куплено шуб.


class House:

    def __init__(self):
        self.money = 100
        self.food = 50
        self.dirt = 0

    def generate_dirt(self):
        self.dirt += 5

    def __str__(self):
        return 'В доме: денег - {}, еды - {}, уровень грязи - {}'.format(self.money, self.food, self.dirt)


class Man:

    def __init__(self, name):
        self.name = name
        self.foodness = 30
        self.happy = 100

    def __str__(self):
        return 'Меня зовут {}, моя сытость {}, мой уровень счастья {}'.format(self.name, self.foodness, self.happy)

    def eat(self, house=None, *args, **kwargs):
        self.foodness += 30
        house.food -= 30
        print('{} поел'.format(self.name))


class Husband(Man):

    def __init__(self, name):
        super().__init__(name=name)

    def __str__(self):
        return super().__str__()

    def act(self, house, child):
        if self.foodness <= 0:
            print('{} - умер от голода'.format(self.name))
            return
        elif self.happy <= 10:
            print('{} - умер от депрессии'.format(self.name))
            return
        setting = randint(1, 5)
        if self.foodness <= 20:
            self.eat(house=house)
        elif self.happy <= 15:
            self.gaming()
        elif house.money <= 400:
            self.work(house=house)
        elif child.foodness <= 15:
            child.eat(house=house, parent=self)
        elif setting == 1:
            self.eat(house=house)
        elif setting == 2:
            self.gaming()
        elif setting == 3:
            self.work(house=house)
        elif setting == 4:
            child.eat(house=house, parent=self)
        else:
            self.work(house=house)

    def eat(self, house=None, *args, **kwargs):
        super().eat(house=house)

    def work(self, house):
        self.foodness -= 10
        house.money += 150
        print('{} сходил на работу'.format(self.name))

    def gaming(self):
        self.happy += 20
        self.foodness -= 10
        print('{} поиграл в WoT'.format(self.name))


class Wife(Man):

    def __init__(self, name):
        super().__init__(name=name)

    def __str__(self):
        return super().__str__()

    def act(self, house, child=None):
        if self.foodness <= 0:
            print('{} - умерла от голода'.format(self.name))
            return
        elif self.happy <= 10:
            print('{} - умерла от депрессии'.format(self.name))
            return
        setting = randint(1, 7)
        if self.foodness <= 20:
            self.eat(house=house)
        elif self.happy <= 15:
            self.buy_fur_coat(house=house)
        elif child.foodness <= 15:
            child.eat(house=house, parent=self)
        elif house.dirt >= 85:
            self.clean_house(house=house)
        elif house.food <= 100:
            self.shopping(house=house)
        elif setting == 1:
            self.eat(house=house)
        elif setting == 2:
            self.buy_fur_coat(house=house)
        elif setting == 3:
            self.clean_house(house=house)
        elif setting == 4:
            self.shopping(house=house)
        elif setting == 5:
            child.eat(house=house, parent=self)
        else:
            self.shopping(house=house)

    def eat(self, house=None, *args, **kwargs):
        super().eat(house=house)

    def shopping(self, house):
        if house.money >= 200:
            self.foodness -= 10
            house.food += 200
            house.money -= 200
            print('{} сходила в магазин и купила еды'.format(self.name))
        else:
            print('Нет денег на продукты')

    def buy_fur_coat(self, house):
        if house.money >= 400:
            self.foodness -= 10
            house.money -= 350
            self.happy += 60
            print('{} купила себе шубу'.format(self.name))
        else:
            print('Нет денег на шубу')

    def clean_house(self, house):
        self.foodness -= 10
        house.dirt -= 100
        print('{} убралась в доме'.format(self.name))


class Child(Man):

    def __init__(self, name):
        super().__init__(name=name)

    def __str__(self):
        return super().__str__()

    def act(self, house, parent):
        if self.foodness <= 0:
            print('Ребенок {} умер от голода'.format(self.name))
            return
        dice = randint(1, 3)
        if dice == 1:
            self.eat(house=house, parent=parent)
        elif dice == 2:
            self.sleep()
        else:
            self.sleep()

    def eat(self, house=None, parent=None, *args, **kwargs):
        self.foodness += 10
        house.food -= 10
        parent.foodness -= 10
        print('Ребенка {} покормил(-а) {}'.format(self.name, parent.name))

    def sleep(self):
        self.foodness -= 10
        print('Ребенок {} поспал'.format(self.name))


home = House()
serge = Husband(name='Сережа')
masha = Wife(name='Маша')
baby = Child(name='Алекс')
parents = [serge, masha]

for day in range(1, 366):
    cprint('================== День {} =================='.format(day), color='red')
    serge.act(house=home, child=baby)
    masha.act(house=home, child=baby)
    baby.act(house=home, parent=parents[randint(0, 1)])
    home.generate_dirt()
    cprint(serge, color='cyan')
    cprint(masha, color='cyan')
    cprint(baby, color='red')
    cprint(home, color='yellow')

# TODO после реализации первой части - отдать на проверку учителю

# Часть вторая
#
# После подтверждения учителем первой части надо
# отщепить ветку develop и в ней начать добавлять котов в модель семьи
#
# Кот может:
#   есть,
#   спать,
#   драть обои
#
# Люди могут:
#   гладить кота (растет степень счастья на 5 пунктов)
#
# В доме добавляется:
#   еда для кота (в начале - 30)
#
# У кота есть имя и степень сытости (в начале - 30)
# Любое действие кота, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Еда для кота покупается за деньги: за 10 денег 10 еды.
# Кушает кот максимум по 10 единиц еды, степень сытости растет на 2 пункта за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе кот умрет от голода.
#
# Если кот дерет обои, то грязи становится больше на 5 пунктов


class Cat:

    def __init__(self):
        pass

    def act(self):
        pass

    def eat(self):
        pass

    def sleep(self):
        pass

    def soil(self):
        pass


# Часть вторая бис
#
# После реализации первой части надо в ветке мастер продолжить работу над семьей - добавить ребенка
#
# Ребенок может:
#   есть,
#   спать,
#
# отличия от взрослых - кушает максимум 10 единиц еды,
# степень счастья  - не меняется, всегда ==100 ;)

# TODO после реализации второй части - отдать на проверку учителем две ветки


# Часть третья
#
# после подтверждения учителем второй части (обоих веток)
# влить в мастер все коммиты из ветки develop и разрешить все конфликты
# отправить на проверку учителем.


# home = House()
# serge = Husband(name='Сережа')
# masha = Wife(name='Маша')
# kolya = Child(name='Коля')
# murzik = Cat(name='Мурзик')
#
# for day in range(365):
#     cprint('================== День {} =================='.format(day), color='red')
#     serge.act()
#     masha.act()
#     kolya.act()
#     murzik.act()
#     cprint(serge, color='cyan')
#     cprint(masha, color='cyan')
#     cprint(kolya, color='cyan')
#     cprint(murzik, color='cyan')


# Усложненное задание (делать по желанию)
#
# Сделать из семьи любителей котов - пусть котов будет 3, или даже 5-10.
# Коты должны выжить вместе с семьей!
#
# Определить максимальное число котов, которое может прокормить эта семья при значениях зарплаты от 50 до 400.
# Для сглаживание случайностей моделирование за год делать 3 раза, если 2 из 3х выжили - считаем что выжили.
#
# Дополнительно вносить некий хаос в жизнь семьи
# - N раз в год вдруг пропадает половина еды из холодильника (коты?)
# - K раз в год пропадает половина денег из тумбочки (муж? жена? коты?!?!)
# Промоделировать - как часто могут случаться фейлы что бы это не повлияло на жизнь героев?
#   (N от 1 до 5, K от 1 до 5 - нужно вычислит максимумы N и K при котором семья гарантированно выживает)
#
# в итоге должен получится приблизительно такой код экспериментов
# for food_incidents in range(6):
#   for money_incidents in range(6):
#       life = Simulation(money_incidents, food_incidents)
#       for salary in range(50, 401, 50):
#           max_cats = life.experiment(salary)
#           print(f'При зарплате {salary} максимально можно прокормить {max_cats} котов')
