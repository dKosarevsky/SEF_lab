import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


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


def trapezoidal_rule(func, low_limit: float, up_limit: float, sub_ints: float) -> float:
    """
        Правило трапеций для численной аппроксимации интегральной заданной функции
    :param func: математическая функция
    :param low_limit: нижний предел
    :param up_limit: верхний предел
    :param sub_ints: число отрезков, на которые разбивается
    :return: результат вычислений
    """
    sum_xi = 0.0
    h = (up_limit - low_limit) / sub_ints  # finding midpoint, (b-a)/n
    sum_ = func(low_limit) + func(up_limit)  # find the f(a) and f(b)
    for i in range(1, int(sub_ints)):
        sum_xi += func(low_limit + i * h)
    fx = (h / 2) * (sum_ + 2 * sum_xi)

    return round(fx, 5)


def rectangle_rule(func, a, b, sub_ints, frac):
    """Обобщённое правило прямоугольников."""
    dx = 1.0 * (b - a) / sub_ints
    sum_ = 0.0
    x_start = a + frac * dx  # 0 <= frac <= 1 задаёт долю смещения точки,
    # в которой вычисляется функция,
    # от левого края отрезка dx
    for i in range(int(sub_ints)):
        sum_ += func(x_start + i * dx)

    return sum_ * dx


def midpoint_rectangle_rule(func, a, b, sub_ints):
    """Правило прямоугольников со средней точкой"""
    return rectangle_rule(func, a, b, sub_ints, 0.5)


def precision_trapezoidal_rule(func, a: float, b: float, precision: float = 1e-8, start_sub_ints: float = 1.) -> float:
    """
        Правило трапеций
    :param func: математическая функция
    :param a: нижний предел
    :param b: верхний предел
    :param precision - желаемая относительная точность вычислений
    :param start_sub_ints - начальное число отрезков разбиения
    :return: результат вычислений
    """
    sub_ints = start_sub_ints
    dx = 1.0 * (b - a) / sub_ints
    ans = 0.5 * (func(a) + func(b))
    for i in range(1, int(sub_ints)):
        ans += func(a + i * dx)

    ans *= dx
    err_est = max(1, abs(ans))
    while err_est > abs(precision * ans):
        old_ans = ans
        ans = 0.5 * (ans + midpoint_rectangle_rule(func, a, b, sub_ints))  # новые точки для уточнения интеграла
        # добавляются ровно в середины предыдущих отрезков
        sub_ints *= 2
        err_est = abs(ans - old_ans)

    return round(ans, 5)


def dichotomy_one(func, a, b, accuracy=0.0001, epsilon=0.0000001):
    while b - a > accuracy:
        x = (b + a) / 2 - epsilon
        y = (b + a) / 2 + epsilon
        if func(x) > func(y):
            a = x
        else:
            b = y
    return [round(a, 5), round(b, 5)]


def plot(func, a, b, res):
    """ отрисовка графика """
    x = np.arange(a, b, 0.001)
    y = [func(i) for i in x]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(x, y)
    ax.scatter(res[0], func(res[0]))
    ax.scatter(res[1], func(res[1]))
    ax.axhline(0, color='black')
    ax.set_title(f"Функция {func.__doc__}")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$f(x)$")

    st.write(fig)


def equation_1(x):
    """sin(x)"""
    return np.sin(x)


def equation_2(x):
    """cos^2(x) * ln^2(x+5)"""
    return np.cos(x) ** 2 * np.log(x + 5) ** 2


def equation_3(x):
    """(2 * x + 1) / sqrt(x + 1 / 16)"""
    return (2 * x + 1) / np.sqrt(x + 1 / 16)


def main():
    header()

    if st.checkbox("Показать ТЗ"):
        show_tz()

    integrate_type = st.radio(
        "Выберите необходимое вычисление", (
            "1. Приближенное вычисление определенного интеграла методом трапеций с заданным шагом",
            "2. Приближенное вычисление определенного интеграла методом трапеций с заданной точностью",
            "3. Вычисление точки пересечения функции с осью абсцисс на заданном интервале методом дихотомии"
        )
    )
    if integrate_type[:1] == "1":
        c1, c2, c3 = st.beta_columns(3)
        lower_limit = c1.number_input("Введите нижний предел:", value=.0)
        upper_limit = c2.number_input("Введите верхний предел:", value=1.57)
        sub_intervals = c3.number_input("Введите шаг:", min_value=.1, value=.1)

        fx_eq_1 = trapezoidal_rule(equation_1, lower_limit, upper_limit, sub_intervals)
        fx_eq_2 = trapezoidal_rule(equation_2, lower_limit, upper_limit, sub_intervals)
        fx_eq_3 = trapezoidal_rule(equation_3, lower_limit, upper_limit, sub_intervals)
        st.write(f"Результат для {equation_1.__doc__} = {fx_eq_1}")
        st.write(f"Результат для {equation_2.__doc__} = {fx_eq_2}")
        st.write(f"Результат для {equation_3.__doc__} = {fx_eq_3}")

    elif integrate_type[:1] == "2":
        c1, c2, c3 = st.beta_columns(3)
        lower_limit = c1.number_input("Введите нижний предел:", value=.0)
        upper_limit = c2.number_input("Введите верхний предел:", value=1.57)
        precision = c3.number_input("Введите точность:", value=1.2)

        fx_eq_1 = precision_trapezoidal_rule(equation_1, lower_limit, upper_limit, precision)
        fx_eq_2 = precision_trapezoidal_rule(equation_2, lower_limit, upper_limit, precision)
        fx_eq_3 = precision_trapezoidal_rule(equation_3, lower_limit, upper_limit, precision)
        st.write(f"Результат для {equation_1.__doc__} = {fx_eq_1}")
        st.write(f"Результат для {equation_2.__doc__} = {fx_eq_2}")
        st.write(f"Результат для {equation_3.__doc__} = {fx_eq_3}")

    elif integrate_type[:1] == "3":
        st.markdown(":construction_worker: Ведутся технические работы ...")

        c1, c2, c3 = st.beta_columns(3)
        lower_limit = c1.number_input("Введите нижний предел:", value=.0)
        upper_limit = c2.number_input("Введите верхний предел:", value=1.57)

        res_1 = dichotomy_one(equation_1, lower_limit, upper_limit)
        st.write(f"Интервальная оценка минимума для {equation_1.__doc__} = {res_1}")
        plot(equation_1, lower_limit, upper_limit, res_1)

        res_2 = dichotomy_one(equation_2, lower_limit, upper_limit)
        st.write(f"Интервальная оценка минимума для {equation_2.__doc__} = {res_2}")
        plot(equation_2, lower_limit, upper_limit, res_2)

    # st.button("Очистить результаты")


if __name__ == "__main__":
    main()
