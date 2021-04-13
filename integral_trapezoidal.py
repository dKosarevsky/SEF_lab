import streamlit as st
import numpy as np
import pandas as pd
import base64
import plotly.graph_objects as go


def header():
    st.set_page_config(initial_sidebar_state="collapsed")
    st.sidebar.image('logo.png', width=300)
    author = """
        ---
        made by [Kosarevsky Dmitry](https://github.com/dKosarevsky) 
        for Software Engineering Fundamentals [lab#1](https://github.com/dKosarevsky/SEF_lab_001)
        in [BMSTU](https://bmstu.ru)
    """
    st.title("МГТУ им. Баумана. Кафедра ИУ7")
    st.header("Основы программной инженерии.\nЛабораторная работа №1")
    st.write("Вычисление определенного интеграла методами трапеций")
    st.write("Преподаватель: Солодовников В.И.")
    st.write("Студент: Косаревский Д.П.")
    st.write("")
    st.write("---")
    st.sidebar.markdown(author)


def show_tz():
    st.markdown("""
        Вариант 7.

        Написать программу для приближенного вычисления определенного интеграла методами:
        * трапеций с заданным шагом, 
        * трапеций с заданной точностью, 
        
        Вычисления точки пересечения выбранной пользователем функции с осью абсцисс на заданном интервале методом дихотомии. 

        Выбранную для проверки функцию передавать как отдельный параметр подпрограмм вычисления значений функции, интеграла, корня. 

        Для проверки использовать следующие функции:

        * `sin(x)`
        * `cos^2(x) * ln^2(x+5)`
        
        ---
        
        Лабораторная работа № 4
        
        К заданию из Лабораторной работы №1 (ЛР1) добавить возможность выбора третьей функции в виде полинома восьмой степени: 
        
        `a1 * x^8 + a2 * x^7 + a3 * x^6 + a4 * x^5 + a5 * x^4 + a6 * x^3 + a7 * x^2 + a8 * x + a9`
        
        Для всех трех функций из ЛР1 реализовать следующий функционал (расширить функционал программы из ЛР1): 
         * Запись в файл значений функции и значений аргумента на выбранном интервале и с заданным шагом (значения интервала и размер шага задаются пользователем);
         * Чтение из файла значений функции и аргумента;
         * Вывод на экран значений из файла в виде таблицы;
         * Построение графика по значениям из файла.

        ---
    """)


def trapezoidal_rule(func, low_limit: float, up_limit: float, intervals: float) -> float:
    """
        Правило трапеций для численной аппроксимации интегральной заданной функции
    :param func: математическая функция
    :param low_limit: нижний предел интегрирования
    :param up_limit: верхний предел интегрирования
    :param intervals: число отрезков, на которые разбивается
    :return: результат вычислений
    """
    area = .5 * (func(low_limit) + func(up_limit))
    x = low_limit + intervals
    while x <= up_limit - intervals:
        area += func(x)
        x += intervals
    return intervals * area


def precision_trapezoidal_rule(func, low_lim: float, up_lim: float, max_err: float = .1, intervals: int = 1) -> float:
    """
        Правило трапеций с заданной точностью
    :param func: математическая функция
    :param low_lim: нижний предел интегрирования
    :param up_lim: верхний предел интегрирования
    :param max_err: заданная точность
    :param intervals: число отрезков, на которые разбивается
    :return: результат вычислений
    """
    dx = (up_lim - low_lim) / intervals
    total = 0

    # выполняем интеграцию
    x = low_lim
    for _ in range(intervals):
        # добавляем область трапеции для этого среза
        total += slice_area(func, x, x + dx, max_err)

        # переходим к следующему срезу
        x += dx

    return round(total, 5)


def slice_area(function, x1, x2, max_error):
    # вычисляем функцию в конечных и средних точках
    y1 = function(x1)
    y2 = function(x2)
    xm = (x1 + x2) / 2
    ym = function(xm)

    # рассчитываем площади срезов и самого большого участка
    large = (x2 - x1) * (y1 + y2) / 2
    first = (xm - x1) * (y1 + ym) / 2
    second = (x2 - xm) * (y2 + ym) / 2
    both = first + second

    # рассчитываем ошибку
    error = (both - large) / large

    # сравниваем ошибку с допустимым значением ошибки (точности)
    if abs(error) < max_error:
        return both

    # если ошибка больше допустимого значения - делим ее на две части (два среза)
    return slice_area(function, x1, xm, max_error) + slice_area(function, xm, x2, max_error)


def plot(func, a, b, zero=None):
    """ отрисовка графика """
    x = np.arange(a, b, 0.001)
    y = [func(i) for i in x]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines',
    ))
    if zero:
        fig.add_trace(go.Scatter(
            x=[zero],
            y=[0],
            marker=dict(
                size=10,
                line=dict(
                    width=2
                )
            ),
            showlegend=False
        ))
    fig.update_layout(
        title_text=f"Функция {func.__doc__}",
        xaxis_title='x',
        yaxis_title='f(x)',
        showlegend=False
    )
    st.write(fig)
    st.markdown("---")


def equation_1(x):
    """sin(x)"""
    return np.sin(x)


def equation_2(x):
    """cos^2(x) * ln^2(x+5)"""
    return np.cos(x) ** 2 * np.log(x + 5) ** 2


def equation_3(x, a1=1, a2=2, a3=3, a4=4, a5=5, a6=6, a7=7, a8=8, a9=9):
    """a1 * x^8 + a2 * x^7 + a3 * x^6 + a4 * x^5 + a5 * x^4 + a6 * x^3 + a7 * x^2 + a8 * x + a9"""
    return a1 * x ** 8 + a2 * x ** 7 + a3 * x ** 6 + a4 * x ** 5 + a5 * x ** 4 + a6 * x ** 3 + a7 * x ** 2 + a8 * x + a9


def equation_4(x):
    """x/2 - sin(x) + π/6 - ((3^(1/2)) / 2)"""
    return x / 2 - np.sin(x) + np.pi / 6 - ((3 ** (1 / 2)) / 2)


def dichotomy(f, a, b, tol):
    inc = []
    y = (a + b) / 2

    if f(a) * f(b) < 0:
        while abs(b - a) > tol:
            x = (a + b) / 2
            inc.append(abs(x - y))
            y = x
            if f(a) * f(x) <= 0:
                b = x
            else:
                a = x
        zero = (a + b) / 2
        st.write(f"Функция {f.__doc__} пересекает ось абсцисс в точке [{round(zero, 2)}, 0]")
        return zero
    elif f(a) * f(b) > 0:
        st.error(f"Невозможно применить метод дихотомии для функции {f.__doc__} на интервале [{a}, {b}]")

    else:
        if f(a) == 0:
            st.write(f"Нуль функции {f.__doc__} на [{a}, {b}] над точкой [{round(a, 2)}, 0]")
            return a
        else:
            st.write(f"Нуль функции {f.__doc__} на [{a}, {b}] b = [{round(b, 2)}, 0]")
            return b


def save_file(df, filename):
    csv = df.to_csv()
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Скачать .csv файл</a>'
    st.markdown(href, unsafe_allow_html=True)


def trapezoidal_main(equation, start, end, intervals):
    result = trapezoidal_rule(equation, start, end, intervals)
    st.write(f"Результат для {equation.__doc__} = {round(result, 5)}")

    df = pd.DataFrame({
        "Функция": [equation.__doc__, ],
        "Нижний предел": [start, ],
        "Верхний предел": [end, ],
        "Шаг": [intervals, ],
    }).T

    save_file(df, "trapezoidal")


def trapezoidal_p_main(equation, start, end, p):
    result = precision_trapezoidal_rule(equation, start, end, p)
    st.write(f"Результат для {equation.__doc__} = {round(result, 5)}")

    df = pd.DataFrame({
        "Функция": [equation.__doc__, ],
        "Нижний предел": [start, ],
        "Верхний предел": [end, ],
        "Точность": [p, ],
    }).T

    save_file(df, "trapezoidal_precision")


def dichotomy_and_plot(equation, start, end, eps):
    zero = dichotomy(equation, start, end, eps)
    plot(equation, start, end, zero)

    df = pd.DataFrame({
        "Функция": [equation.__doc__, ],
        "Начало интервала": [start, ],
        "Конец интервала": [end, ],
        "Эпсилон": [eps, ],
    }).T

    save_file(df, "dichotomy")


def poly_values():
    values = st.radio("Значения полинома", ('a. По-умолчанию', 'b. Ввести вручную'))
    if values[:1] == "b":
        st.write("Введите значения полинома:")
        c1, c2, c3 = st.beta_columns(3)
        c4, c5, c6 = st.beta_columns(3)
        c7, c8, c9 = st.beta_columns(3)
        a1 = c1.number_input("a1:")
        a2 = c2.number_input("a2:")
        a3 = c3.number_input("a3:")
        a4 = c4.number_input("a4:")
        a5 = c5.number_input("a5:")
        a6 = c6.number_input("a6:")
        a7 = c7.number_input("a7:")
        a8 = c8.number_input("a8:")
        a9 = c9.number_input("a9:")

        return a1, a2, a3, a4, a5, a6, a7, a8, a9


def upload_and_print(dichotomy_=False):
    data_file = st.file_uploader(
        "Загрузите файл со значениями функции и аргумента:",
        type=["csv", ]
    )
    if data_file and data_file.name[-3:] == "csv":
        data_file = pd.read_csv(data_file)

    ch1, ch2 = st.beta_columns(2)
    table_ = ch1.checkbox("Показать таблицу")
    plot_ = ch2.checkbox("Показать график")

    if table_:
        st.write(data_file)

    func_str = data_file.iloc[0, 1]
    start = float(data_file.iloc[1, 1])
    end = float(data_file.iloc[2, 1])

    if dichotomy_:
        epsilon = float(data_file.iloc[3, 1])

    if plot_:
        try:
            if func_str == equation_1.__doc__:
                if dichotomy_:
                    dichotomy_and_plot(equation_1, start, end, epsilon)
                else:
                    plot(equation_1, start, end)
            elif func_str == equation_2.__doc__:
                if dichotomy_:
                    dichotomy_and_plot(equation_2, start, end, epsilon)
                else:
                    plot(equation_2, start, end)
            elif func_str == equation_3.__doc__:
                if dichotomy_:
                    dichotomy_and_plot(equation_3, start, end, epsilon)
                else:
                    plot(equation_3, start, end)
            elif func_str == equation_4.__doc__:
                if dichotomy_:
                    dichotomy_and_plot(equation_4, start, end, epsilon)
                else:
                    plot(equation_4, start, end)
            else:
                st.info("Такую функцию мы пока не умеем рисовать, но обязательно научимся.")
        except IndexError:
            st.warning("Содержимое файла не соответствует формату, проверьте данные.")


def main():
    header()

    if st.checkbox("Показать ТЗ"):
        show_tz()

    calc_type = st.radio(
        "Выберите необходимое вычисление", (
            "1. Приближенное вычисление определенного интеграла методом трапеций с заданным шагом",
            "2. Приближенное вычисление определенного интеграла методом трапеций с заданной точностью",
            "3. Вычисление точки пересечения функции с осью абсцисс на заданном интервале методом дихотомии"
        )
    )

    st.markdown("---")

    if calc_type[:1] == "1":
        st.write(calc_type[3:])
        c1, c2, c3 = st.beta_columns(3)
        lower_limit = c1.number_input("Введите нижний предел:", value=.0)
        upper_limit = c2.number_input("Введите верхний предел:", value=1.57)
        sub_intervals = c3.number_input("Введите шаг:", min_value=.00000000001, value=.01, format="%.8f")

        st.markdown("---")
        trapezoid = st.radio("Выберите функцию", (
            f"1. {equation_1.__doc__}",
            f"2. {equation_2.__doc__}",
            f"3. {equation_3.__doc__}",
            f"0. Загрузить из файла",
        ))
        if trapezoid[:1] == "1":
            trapezoidal_main(equation_1, lower_limit, upper_limit, sub_intervals)

        elif trapezoid[:1] == "2":
            trapezoidal_main(equation_2, lower_limit, upper_limit, sub_intervals)

        elif trapezoid[:1] == "3":
            p_values = poly_values()

            if p_values:
                equation_3.__defaults__ = p_values

            trapezoidal_main(equation_3, lower_limit, upper_limit, sub_intervals)

        elif trapezoid[:1] == "0":
            upload_and_print()

    elif calc_type[:1] == "2":
        st.write(calc_type[3:])
        c1, c2, c3 = st.beta_columns(3)
        lower_limit = c1.number_input("Введите нижний предел:", value=.0)
        upper_limit = c2.number_input("Введите верхний предел:", value=1.57)
        precision = c3.number_input("Введите точность:", value=.1, format="%.8f")

        trapezoid_p = st.radio("Выберите функцию", (
            f"1. {equation_1.__doc__}",
            f"2. {equation_2.__doc__}",
            f"3. {equation_3.__doc__}",
            f"0. Загрузить из файла",
        ))
        if trapezoid_p[:1] == "1":
            trapezoidal_p_main(equation_1, lower_limit, upper_limit, precision)

        elif trapezoid_p[:1] == "2":
            trapezoidal_p_main(equation_2, lower_limit, upper_limit, precision)

        elif trapezoid_p[:1] == "3":
            p_values = poly_values()

            if p_values:
                equation_3.__defaults__ = p_values

            trapezoidal_p_main(equation_3, lower_limit, upper_limit, precision)

        elif trapezoid_p[:1] == "0":
            upload_and_print()

    elif calc_type[:1] == "3":
        st.write(calc_type[3:])
        c1, c2, c3 = st.beta_columns(3)
        start_interval = c1.number_input("Начало интервала (a):", value=-5.0)
        end_interval = c2.number_input("Конец интервала (b):", value=12.5)
        epsilon = c3.number_input("Эпсилон (е):", min_value=.00000000001, value=.00001, format="%.8f")

        st.markdown("---")
        func_to_plot = st.radio("Выберите функцию", (
            f"1. {equation_1.__doc__}",
            f"2. {equation_2.__doc__}",
            f"3. {equation_3.__doc__}",
            f"4. {equation_4.__doc__}",
            f"0. Загрузить из файла",
        ))
        if func_to_plot[:1] == "1":
            dichotomy_and_plot(equation_1, start_interval, end_interval, epsilon)

        elif func_to_plot[:1] == "2":
            dichotomy_and_plot(equation_2, start_interval, end_interval, epsilon)

        elif func_to_plot[:1] == "3":
            p_values = poly_values()

            if p_values:
                equation_3.__defaults__ = p_values

            dichotomy_and_plot(equation_3, start_interval, end_interval, epsilon)

        elif func_to_plot[:1] == "4":
            dichotomy_and_plot(equation_4, start_interval, end_interval, epsilon)

        elif func_to_plot[:1] == "0":
            upload_and_print(dichotomy_=True)


if __name__ == "__main__":
    main()
