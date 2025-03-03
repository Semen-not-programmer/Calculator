import random
import doctest
from typing import Union
from typing import Any
import math
import datetime

SOURCE = '1.2_Скобки_сложно'

# Создать функции для основных действий: сложения, умножения, деления, вычитания
# Они должны быть рекурсивными - внутри могут содержаться другие функции
# Подавать в функцию выражение для написания и ответ (её решение)
# Реализовать функцию вывода

#TODO метод упрощения дробей
#TODO Метод сложения дробей
# TODO Метод случайного выбора частей с более простой сложностью
# TODO Метод генерации дроби в заданных пределах
# Todo Метод умножения дробей
# TODO Медот деления дробей
# TODO Метод проверки сложности умножения десятичных чисел
# TODO Метод проверки сложности деления десятичных чисел
# TODO Создать механизм раскрытия скобок для простого счёта дробей
#  показывать, где стоят

class Expression:
    """
    Класс, генерирующий случайные выражения без неизвестных
    diff_type_check - список уровней сложности
    CHARS - соответствие символов
    """
    numeric = ['0', '1', '2', '3', '4','5', '6', '7', '8', '9', '.', ',']
    operators = ['+', '-', '*', 'over']
    diff_type_check = ['N', 'Z', 'Q_dr', 'Q_de']
    chars = {'addition': '+',
              'subtraction': '-',
              'division': 'over',
              'multiplication': '*'}
    bracket_circle = ['(', ')']
    bracket_square = ['[', ']']
    bracket_shaped = ['{', '}']
    bracket_list = ['(', ')', '[', ']', '{', '}']


    def __init__(self,
                 length: int,
                 low_border: Union[int, float] = 3,
                 high_border: Union[int, float] = 25,
                 diff_type: str = 'N'):
        """
        Инизиализация входных данных
        parts - доли операций в выражении
        Пример:
        parts = {'addition': 1,     #доля операций сложения
         'subtraction': 1,          #доля операций вычитания
         'division': 0,             #доля операций деления
         'multiplication': 0}       #доля операций умножения

        low_border - нижняя граница диапазона
        high_border - верхняя граница диапазона
        diff_type - тип данных
            'N' - натуральные числа
            'Z' - целые числа
            'Q_dr' - рациональные числа (Z/N) как дробь
            'Q_de' - рациональные числа (x.xxx) как десячичное число
        self.task - текст выходного выражения
        self.answer - значение выходного выражения

        self.term_list - список экземпляров класса Term для составления из них выражения
        self.task_list - список текстовых значений членов выражения
        self.answer_list - список числовых значений членов выражения
        length - количество членов в выражении
        """

        self.check_type(low_border, 'low_border', (int, float))
        self.check_type(high_border, 'high_border', (int, float))
        if low_border > high_border:
            low_border, high_border = high_border, low_border
        self.high_border = high_border
        self.low_border = low_border

        self.check_type(diff_type, 'diff_type', str)
        if diff_type in __class__.diff_type_check:
            self.diff_type = diff_type
        else:
            raise ValueError(f"Значение diff_type {diff_type} не является "
                             f"допустимым "
                             f"{__class__.diff_type_check}")

        self.check_type(length, 'length', int)
        self.check_value_positive(length, 'length')
        self.length = length

        self.parts = {'addition': 1,  # доля операций сложения
                      'subtraction': 1,  # доля операций вычитания
                      'division': 0,  # доля операций деления
                      'multiplication': 0}  # доля операций умножения
        self.part_normation()

        self.task = None
        self.answer = None

        # заполнение списков текстов и значений
        self.term_list = [0] * self.length
        self.task_list = ['0'] * self.length
        self.answer_list = [0] * self.length

    @staticmethod
    def check_type(value: Any,
                   name: str,
                   type_check: Union[type, tuple[type]]) -> None:
        """
        Метод проверяет соответствие входных типов данных требуемым значениям
        value - входное значение
        name - имя переменной (для оформления)
        type_check - требуемый тип или кортеж требуемых типов
        """
        if not isinstance(value, type_check):
            raise TypeError(
                f'Переменная {name} может принимать только '
                f'значения типа {type_check}')

    @staticmethod
    def check_value_positive(value: Any,
                             name: str) -> None:
        """
        Метод проверяет, положительны ли значения входных данных
        value - входное значение
        name - имя переменной (для оформления)
        """
        if value < 0:
            raise TypeError(f'Переменная {name} может принимать только '
                            f'положительные значения')

    def part_change(self,
                    d_dict: dict) -> None:
        """
        Метод получает словарь параметров, которые необходимо изменить
        изначальное значение:
        parts = {'addition': 1,     #доля операций сложения
         'subtraction': 1,          #доля операций вычитания
         'division': 0,             #доля операций деления
         'multiplication': 0}       #доля операций умножения
         такой же формат для d_dict, предусмотрены пропуски и произвольный порядок
         d_dict - словарь изменяемых значений

        Пример:
        check = Expression(3)
        print(check.parts)
        {'addition': 0.5, 'subtraction': 0.5, 'division': 0.0, 'multiplication': 0.0}
        check.part_change({'multiplication': 4})
        print(check.parts)
        {'addition': 0.1, 'subtraction': 0.1, 'division': 0.0, 'multiplication': 0.8}
        """

        for name_change, value_change in d_dict.items():
            self.check_type(value_change, 'value_change', (int, float))
            if name_change in self.parts.keys():
                self.parts[name_change] = value_change
            else:
                raise ValueError(f"Имя {name_change} не является допустимым. Допустимые значения: {self.parts.keys()}")
        self.part_normation()


    def part_normation(self) -> None:
        """
        Метод нормирует доли операций в выражении, чтобы в сумме получилось
        количество членов
        """
        summ = sum(x for x in self.parts.values())
        for name, value in self.parts.items():
            self.parts[name] = random.choice(
                [math.ceil(value / summ * self.length),
                 math.floor(value / summ * self.length)])
        while sum(self.parts.values()) != self.length - 1: #В сумме должно количество членов в выражении минус один
            count = sum(self.parts.values()) - (self.length - 1)
            for name, value in self.parts.items():
                if random.randint(0, 1) and self.parts[name] != 0:
                    self.parts[name] = value - int(math.copysign(1, count))
                    #math.copysign(1, count) - функция sgn(count)
                    count -= math.copysign(1, count)
                    if not count:
                        break


    def generator(self):
        """
        Метод генерирует текст выражения и ответ, используя вспомогательный класс Term

        случайный выбор из доступных элементов parts
        случайная генерация скобки
        сборка выражения
        сборка ответа
        """
        for i in range(self.length):
            self.term_list[i] = Term(self.diff_type, self.low_border, self.high_border)
            self.term_list[i].generator()
            self.task_list[i] = self.term_list[i].task
            self.answer_list[i] = self.term_list[i].answer

        #заполнение текста операциями
        self.task = ''
        for i in range(self.length):
            self.task += self.task_list[i]
            if i != self.length - 1:
                #случайный выбор операции
                while True:
                    name = random.choice(list(self.parts.keys()))
                    if self.parts[name]:
                        self.parts[name] -= 1
                        self.task += __class__.chars[name]
                        break

        # проверка того, что есть аттрибут self.task (был вызван метод generator())
        if self.task:
            out = self.decoder(self.task)
        else:
            raise AttributeError('Не создано значение атрибута task')

        # Настройка вывода целого значения без формата хх.0 а в формате xx
        if out % 1 == 0:
            self.answer = int(out)
        else:
            self.answer = out


    def decoder(self,
                task: str) -> float:
        """
        Рекурсивный метод, который вычистяет численное значение выражения
        task - текст выражения, которое необходимо вычислить

        замена вычитаний на относительные значения
        9-8+17-24 -> 9+n8+17+n24

        рекурсивная функция подсчёта бинарных операторов
        9+n8+17+n24 разбивается на 9 и n8+17+n24
        n8+17+n24 разбивается на n8 и 17+n24
        17+n24 разбивается на 17 и n24
        подсчёт 17 как числа 17 и n24 как числа -24
        и так далее
        """
        print(task)

        #замена вычитаний на относительные  значения
        #9-8+17-24 -> 9+n8+17+n24
        for i in range(len(task)):
            if task[i] == '-' and task[i + 1] not in ['(', '{', '[']:
                if task[i - 1] not in self.operators:
                    task = task[: i] + '+n' + task[i + 1:]
                else:
                    task = task[: i] + 'n' + task[i + 1:]



        for var in self.bracket_list:
            if var in task:
                # получение индексов скобок
                low_index = 0
                up_index = len(task)
                bracket_first, bracket_second = self.bracket_finder(task, low_index, up_index)
                # счёт только того, что в скобках
                task = str(self.decoder(task[:bracket_first] + str(self.decoder(task[bracket_first + 1:bracket_second])) + task[bracket_second + 1:]))
                break

        # рекурсивная функция подсчёта бинарных операторов
        is_task = self.solwer(task)
        if not is_task:
            for operator in self.operators:
            # TODO порядок операторов по приоритетам действий
            # TODO флаг на нахождение внутри скобочки
                pos = task.find(operator)
                if pos == -1:
                    continue
                size = len(operator)
                var_left = task[:pos]
                var_right = task[pos + size:]
                is_var_left = self.solwer(var_left)
                is_var_right = self.solwer(var_right)
                break
            if is_var_left:
                var_left = is_var_left
            else:
                var_left = self.decoder(var_left)

            if is_var_right:
                var_right = is_var_right
            else:
                var_right = self.decoder(var_right)

            if operator == '+':
                return var_left + var_right
            elif operator == '-':
                return var_left - var_right
            if operator == 'over':
                return var_left / var_right
            if operator == '*':
                return var_left * var_right

        else:
            return is_task

    @classmethod
    def solwer(cls,
               task: str) -> Union[int, float, None]:
        """
        Метод расшифровывает значения из текстового выражения
        Возвращает значение числа, если это исключительно число
        Возвращает None, если в строке есть символы
        task - текст выражения, которое необходимо вычислить
        """
        #TODO добавить решения дробных чисел через /
        if len(task) < 1:
            return None
        sign = 1
        if task[0] == 'n' or task[0] == '-':
            sign = -1
            task = task[1:]
        for i in range(len(task)):
            if not task[i] in cls.numeric:
                return None
        return float(task) * sign

    def bracket_finder(self,
                       task: str,
                       low_index: int,
                       up_index: int) -> Union[tuple[Union[int, None]], None]:
        """
        Метод предназначен для поиска вхождений скобок наиболее глубоких
        :param task: текст выражения
        :param low_index: нижний индекс self.task, с которого начинается поиск скобки
        :param up_index: верхний индекс self.task, с которого начинается поиск скобки
        :return: возвращает кортеж (нижний индекс, верхний индекс) вхождения скобки
        """
        # индекс открывающей скобки
        bracket_first = None
        # индекс закрывающей скобки
        bracket_second = None
        # флаг на нахождение открывающей скобки
        flag = False
        for i in range(low_index, up_index):
            var = task[i]
            if var in self.bracket_list:
                if var is self.bracket_circle[0]:
                    bracket_first = i
                    flag = True
                elif var is self.bracket_circle[1]:
                    if flag:
                        bracket_second = i
                        break
                    else:
                        raise ValueError("В методе строка, начинающаяся с открывающей скобки")
                else:
                    pass
                    # TODO Сделать условия для остальных скобок
        # Проверка наличия всех скобок
        if bracket_first and bracket_second:
            return tuple([bracket_first, bracket_second])
        else:
            return None


#TODO Добавление скобок
#TODO Добавление вложенности (а надо?)

    def __str__(self):
        """
        Метод выводит выражение и ответ
        """
        out_dict = {
            'Выражение': f'{self.task}=?',
            'Ответ': self.answer
        }
        # настройка отступов в выводе
        indent = 12
        out_str = ''
        for name, value in out_dict.items():
            n = indent - len(name)
            out_str += name + ':' + ' ' * n + str(value) + '\n'
        return out_str

    def __del__(self) -> None:
        """
        Метод удаляет экземпляр класса Expression и все связанные экземпляры класса Term
        """
        del self.term_list
        if Term.index != 0:
            raise IndexError('Удалены не все элементы класса Term')


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------


class Term:
    """
    Класс, запоминающий члены выражения со всеми свойсивами
    index - порядковый номер выражения
    """
    index = 0
    def __init__(self,
                 diff_type: str,
                 low_border: Union[int, float] = 3,
                 high_border: Union[int, float] = 25):
        """
        Инизиализация входных данных
        diff_type - тип данных
            'N' - натуральные числа
            'Z' - целые числа
            'Q_dr' - рациональные числа (Z/N) как дробь
            'Q_de' - рациональные числа (x.xxx) как десячичное число
        low_border - нижняя граница диапазона
        high_border - верхняя граница диапазона
        self.task - текст выходного выражения
        self.answer - значение выходного выражения

        """
        self.diff_type = diff_type
        self.low_border = low_border
        self.high_border = high_border
        self.task = None
        self.answer = None
        self.index = __class__.index
        self.increase_index()

    def generator(self) -> None:
        """
        Метод генерирует текст и ответ выражения
        """
        if self.diff_type == 'N':
            var_1 = random.randint(self.low_border, self.high_border)
            self.task = str(var_1)
            self.answer = var_1
        # TODO подписать для остальных случаев

    @classmethod
    def increase_index(cls) -> None:
        """
        Метод увеличимает значение порядкового номера выражения
        """
        cls.index += 1

    def __del__(self) -> None:
        """
        Уничтожение экземпляра класса
        """
        __class__.index -= 1

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------


def export(value: str, prefix: str) -> None:
    """
    Модуль экспорта
    Принимает значение, которое нужно вставить value и тип префикса prefix
    prefix = 't' для вывода текста задания
    prefix = 'a' для вывода текста ответа
    """
    if prefix == 't':
        prefix_text = 'task'
    elif prefix == 'a':
        prefix_text = 'answer'
    else:
        prefix_text = prefix

    f = open(prefix_text + '_' + SOURCE + '.txt', 'a')
    f.write(value + '\n')
    f.close()


def get_result(length: int,
               low_border: Union[int, float] = 3,
               high_border: Union[int, float] = 25,
               diff_type: str = 'N',
               parts:dict[str, Union[int, float]] = None) -> None:
    """
    Функция создаёт класс выражения и выводит ответ в текстовый файл
    параметры те же, что и в классе Expresion
    low_border - нижняя граница диапазона
    high_border - верхняя граница диапазона
    diff_type - тип данных
        'N' - натуральные числа
        'Z' - целые числа
        'Q_dr' - рациональные числа (Z/N) как дробь
        'Q_de' - рациональные числа (x.xxx) как десячичное число
    length - количество членов в выражении


    """
    t = Expression(length, low_border, high_border, diff_type)
    if parts:
        t.part_change(parts)
    t.generator()
    print(t)

    # экспорт
    export(str(t.task) + '=?', 't')
    export(str(t.answer), 'a')


if __name__ == "__main__":
    time = '\n\n' + str(datetime.datetime.now())
    for i in ['t', 'a']:
        export(time, i)








# git commit -m ""




