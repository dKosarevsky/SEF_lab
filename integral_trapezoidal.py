import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
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

        * sin(x)
        * cos^2(x) * ln^2(x+5)
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
    for interval in range(intervals):
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


def plot(func, a, b, zero):
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


def equation_1(x):
    """sin(x)"""
    return np.sin(x)


def equation_2(x):
    """cos^2(x) * ln^2(x+5)"""
    return np.cos(x) ** 2 * np.log(x + 5) ** 2


def equation_3(x):
    """x/2 - sin(x) + pi/6 - ((3**(1/2)) / 2)"""
    return x / 2 - np.sin(x) + np.pi / 6 - ((3 ** (1 / 2)) / 2)


def dichotomy(f, a, b, tol):
    niter = 0
    inc = []
    y = (a + b) / 2

    if f(a) * f(b) < 0:
        while abs(b - a) > tol:
            x = (a + b) / 2
            inc.append(abs(x - y))
            y = x
            niter += 1
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

        fx_eq_1 = trapezoidal_rule(equation_1, lower_limit, upper_limit, sub_intervals)
        st.write(f"Результат для {equation_1.__doc__} = {round(fx_eq_1, 5)}")

        fx_eq_2 = trapezoidal_rule(equation_2, lower_limit, upper_limit, sub_intervals)
        st.write(f"Результат для {equation_2.__doc__} = {round(fx_eq_2, 5)}")

    elif calc_type[:1] == "2":
        st.write(calc_type[3:])
        c1, c2, c3 = st.beta_columns(3)
        lower_limit = c1.number_input("Введите нижний предел:", value=.0)
        upper_limit = c2.number_input("Введите верхний предел:", value=1.57)
        precision = c3.number_input("Введите точность:", value=.1, format="%.8f")

        fx_eq_1 = precision_trapezoidal_rule(equation_1, lower_limit, upper_limit, precision)
        st.write(f"Результат для {equation_1.__doc__} = {round(fx_eq_1, 5)}")

        fx_eq_2 = precision_trapezoidal_rule(equation_2, lower_limit, upper_limit, precision)
        st.write(f"Результат для {equation_2.__doc__} = {round(fx_eq_2, 5)}")

    elif calc_type[:1] == "3":
        st.write(calc_type[3:])
        c1, c2, c3 = st.beta_columns(3)
        start_interval = c1.number_input("Начало интервала (a):", value=-5.0)
        end_interval = c2.number_input("Конец интервала (b):", value=12.5)
        epsilon = c3.number_input("Эпсилон (е):", min_value=.00000000001, value=.00001, format="%.8f")

        zero_1 = dichotomy(equation_1, start_interval, end_interval, epsilon)
        plot(equation_1, start_interval, end_interval, zero_1)

        zero_2 = dichotomy(equation_2, start_interval, end_interval, epsilon)
        plot(equation_2, start_interval, end_interval, zero_2)

        zero_3 = dichotomy(equation_3, start_interval, end_interval, epsilon)
        plot(equation_3, start_interval, end_interval, zero_3)


if __name__ == "__main__":
    main()
