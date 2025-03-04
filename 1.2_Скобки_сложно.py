import random
import doctest
from typing import Union
from typing import Any
import math
import datetime

SOURCE = '1.2_Скобки_сложно'
count_all = 0
count_BracketError = 0
count_UnboundLocalError = 0
count_ValueError = 0


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


class BracketError(Exception):
    """
    Ошибка для обработки исключений в генерации скобок
    """
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"Ошибка со скобками, {self.message}"
        else:
            return "Ошибка со скобками"


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
                 diff_type: str = 'N',
                 brackets: int = 1) -> None:
        """
        Инизиализация входных данных
        parts - доли операций в выражении
        Пример:
        parts = {'addition': 1,     #доля операций сложения
         'subtraction': 1,          #доля операций вычитания
         'division': 0,             #доля операций деления
         'multiplication': 0}        #доля операций умножения

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
        if diff_type in self.diff_type_check:
            self.diff_type = diff_type
        else:
            raise ValueError(f"Значение diff_type {diff_type} не является "
                             f"допустимым "
                             f"{self.diff_type_check}")

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

        # задание количеств скобок
        self.check_type(brackets, 'brackets', int)
        self.check_value_positive(brackets, 'brackets')
        self.brackets_start = brackets
        self.brackets_first = brackets
        self.brackets_second = brackets

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
        # длина выражения оператора
        length = 0
        for i in range(self.length):
            self.term_list[i] = Term(self.diff_type, self.low_border, self.high_border)
            self.term_list[i].generator()
            self.task_list[i] = self.term_list[i].task
            self.answer_list[i] = self.term_list[i].answer

        # заполнение текста операциями
        self.task = ''
        for i in range(self.length):
            # случайное добавление скобки
            self.add_bracket(length)
            # вставка символа
            self.task += self.task_list[i]
            if i != self.length - 1:
                # случайный выбор операции
                while True:
                    name = random.choice(list(self.parts.keys()))
                    if self.parts[name]:
                        self.parts[name] -= 1
                        # длина выражения оператора
                        length = len(self.chars[name])
                        self.task += self.chars[name]

                        # случайное добавление скобки
                        self.add_bracket(length)
                        break
        # добавление закрывающих скобок, если они остались, в конец
        if self.brackets_first < self.brackets_second:
            self.task += self.bracket_circle[1] * (self.brackets_second - self.brackets_first)
        # добавление открывающих скобок, если они остались, в начало
        elif self.brackets_first > self.brackets_second:
            self.task = self.bracket_circle[0] * (self.brackets_first - self.brackets_second) + self.task

        global SOURCE
        log = open('log_' + SOURCE + '.txt', 'a')
        log.write(self.task)
        log.close()

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

    def add_bracket(self,
                    length: int) -> None:
        """
        Метод для случайной вставки скобок в выражение
        :param length: длина оператора, перед которым ставится скобка
        :return: None
        """
        if not random.randint(0, 2):
            #если выпало 50% и если счётчик скобок не кончился
            if random.randint(0, 1) and self.brackets_first:
                # добавление открывающей скобки после знака
                self.task += self.bracket_circle[0]
                self.brackets_first -= 1
            # если счётчик скобок не кончился и если первая скобка открывающая
            elif self.brackets_second and self.brackets_start != self.brackets_first:
                # добавление закрывающей скобки перед знаком
                self.task = self.task[:-length] + self.bracket_circle[1] + self.task[-length:]
                self.brackets_second -= 1

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

        #замена вычитаний на относительные  значения
        #9-8+17-24 -> 9+n8+17+n24
        for i in range(len(task) - 1):
            # если минус не перед скобкой
            if task[i] == '-' and task[i + 1] not in ['(', '{', '[']:
                if task[i - 1] not in self.operators:
                    # если два минуса подряд 13--5
                    if task[i + 1] == '-':
                        task = task[: i] + '+' + task[i + 2:]
                    # если относительное число 13-5
                    else:
                        task = task[: i] + '+n' + task[i + 1:]
                # если минус после операции 13*-5
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
        is_task = self.solver(task)
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
                is_var_left = self.solver(var_left)
                is_var_right = self.solver(var_right)
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
    def solver(cls,
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
                       up_index: int) -> Union[tuple[int], None]:
        """
        Метод предназначен для поиска вхождений скобок наиболее глубоких
        :param task: текст выражения
        :param low_index: нижний индекс self.task, с которого начинается поиск скобки
        :param up_index: верхний индекс self.task, с которого начинается поиск скобки
        :return: возвращает кортеж (нижний индекс, верхний индекс) вхождения скобки
        """
        # индекс открывающей скобки
        bracket_first = -1
        # индекс закрывающей скобки
        bracket_second = -1
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
                        raise BracketError("В методе строка, начинающаяся с открывающей скобки")
                else:
                    pass
                    # TODO Сделать условия для остальных скобок
        # Проверка наличия всех скобок
        if bracket_first != -1 and bracket_second != -1:
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
        self.index = self.index
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
        Метод увеличивает значение порядкового номера выражения
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
    elif prefix == 'l':
        prefix_text = 'log'
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
    global count_all
    global count_BracketError
    global count_UnboundLocalError
    global count_ValueError

    flag = True
    while flag:
        count_all += 1
        try:
            t = Expression(length, low_border, high_border, diff_type)
            if parts:
                t.part_change(parts)
            t.generator()
            # print(t)
        except BracketError as e:
            # print('Ошибка в скобках')
            export('\nОшибка в скобках' + str(e), 'l')
            count_BracketError += 1
        except UnboundLocalError as e:
            # print('UnboundLocalError')
            export('\nUnboundLocalError' + str(e), 'l')
            count_UnboundLocalError += 1
        except ValueError as e:
            # print('ValueError')
            export('\nValueError' + str(e), 'l')
            count_ValueError += 1
        else:
            flag = False
    # экспорт
    export(str(t.task) + '=?', 't')
    export(str(t.answer), 'a')
    export('\n' + str(t) + '\n\n', 'l')


def red_text(var: str):
    """
    :param var: текст, который нужно перекрасить
    :return: str, вывод красного текста
    """
    return "\033[31m{}".format(var)
    # 033[ - обозначение того, что дальше идет какой - то управляющий цветом код
    # 31m - красный цвет


def checking(task_source: str,
             answer_source: str) -> str:
    """
    Функция проверки правильности счёта программ
    :param task_source: источник файла с заданиями
    :param answer_source: источник файла с ответами
    :return: None если успешно. Текст, когда ответ не сходится
    """
    task_f = open(task_source, 'r')
    answer_f = open(answer_source, 'r')

    # пропуск записи времени
    while True:
        task_line = task_f.readline()
        answer_line = answer_f.readline()
        if task_line[0] == '~' and answer_line[0] == '~':
            break

    out_str = ''

    while True:
        task_line = task_f.readline()[:-3].strip()
        answer_line = answer_f.readline().strip()
        if task_line == '' or task_line[0] == '~':
            break
        answer_from_task = eval(task_line)
        if str(answer_from_task) != answer_line:
            out_str += f'{task_line} != {answer_line}\n ответ: {answer_from_task}'
            print(f'Задание: {task_line}')
            print(f'Ответ: {answer_line}')
            print(f'Ответ проги: {answer_from_task}')
            print()

    task_f.close()
    answer_f.close()

    if out_str:
        return red_text(out_str)
    else:
        return "Проверка не выявила проблем"



if __name__ == "__main__":
    # очистка
    f = open('log_' + SOURCE + '.txt', 'w')
    f.close()
    f = open('task_' + SOURCE + '.txt', 'w')
    f.close()
    f = open('answer_' + SOURCE + '.txt', 'w')
    f.close()

    time = '\n\n~' + str(datetime.datetime.now())
    for i in ['t', 'a', 'l']:
        export(time, i)

    for i in range(50):
        get_result(5)
        get_result(6)
        get_result(7)
        get_result(8)
    indent = 20
    print(f"Процент неправильных ответов по BracketError: {' ' * (indent - 12)}{(count_BracketError / count_all * 100):.2f}")
    print(f"Процент неправильных ответов по UnboundLocalError: {' ' * (indent - 17)}{(count_UnboundLocalError / count_all * 100):.2f}")
    print(f"Процент неправильных ответов по ValueError: {' ' * (indent - 10)}{(count_ValueError / count_all * 100):.2f}")

    # проверка на правильность
    print(checking('task_' + SOURCE + '.txt', 'answer_' + SOURCE + '.txt'))


# решить проблему - не решает пример
# (((16-23-10)+6)-10+20)+11
# UnboundLocalErrorlocal variable 'is_var_left' referenced before assignment

# git add ./1.2_Скобки_сложно.py
# git commit -m "Реализована генерация примеров со скобками и проверка истинности ответов"




