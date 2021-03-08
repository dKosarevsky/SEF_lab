import streamlit as st
import numpy as np

from PIL import Image


def header():
    st.set_page_config(initial_sidebar_state="collapsed")
    image = Image.open('logo.png')
    st.image(image, width=100)
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
        * точки пересечения выбранной пользователем функции с осью абсцисс на заданном интервале методом дихотомии. 

        Выбранную для проверки функцию передавать как отдельный параметр подпрограмм вычисления значений функции, интеграла, корня. 

        Для проверки использовать следующие функции:

        * sin(x)
        * cos^2(x) * ln^2(x+5)
    """)


def trapezoidal_rule(func, low_limit: float, up_limit: float, sub_ints: int) -> float:
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
    sum1 = func(low_limit) + func(up_limit)  # find the f(a) and f(b)
    for i in range(1, sub_ints):
        sum_xi += func(low_limit + i * h)
    fx = (h / 2) * (sum1 + 2 * sum_xi)

    return round(fx, 5)


def rectangle_rule(func, a, b, sub_ints, frac):
    """Обобщённое правило прямоугольников."""
    dx = 1.0 * (b - a) / sub_ints
    sum_ = 0.0
    x_start = a + frac * dx  # 0 <= frac <= 1 задаёт долю смещения точки,
    # в которой вычисляется функция,
    # от левого края отрезка dx
    for i in range(sub_ints):
        sum_ += func(x_start + i * dx)

    return sum_ * dx


def midpoint_rectangle_rule(func, a, b, sub_ints):
    """Правило прямоугольников со средней точкой"""
    return rectangle_rule(func, a, b, sub_ints, 0.5)


def precision_trapezoidal_rule(func, a, b, precision=1e-8, start_sub_ints=1):
    """Правило трапеций
       precision - желаемая относительная точность вычислений
       start_sub_ints - начальное число отрезков разбиения"""
    sub_ints = start_sub_ints
    dx = 1.0 * (b - a) / sub_ints
    ans = 0.5 * (func(a) + func(b))
    for i in range(1, sub_ints):
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


def equation_1(x):
    """
        sin(x)
    """
    return np.sin(x)


def equation_2(x):
    """
        cos^2(x) * ln^2(x+5)
    """
    return np.cos(x) ** 2 * np.log(x + 5) ** 2


def main():
    header()

    if st.checkbox("Показать ТЗ"):
        show_tz()

    integrate_type = st.radio(
        "Выберите метод получения вычисления интеграла", (
            "Метод трапеций с заданным шагом",
            "Метод трапеций с заданной точностью",
            "Метод точки пересечения функции с осью абсцисс на заданном интервале методом дихотомии"
        )
    )
    if integrate_type == "Метод трапеций с заданным шагом":
        upper_limit = st.number_input("Введите верхний предел:", value=15.0)
        lower_limit = st.number_input("Введите нижний предел:", value=7.0)
        sub_intervals = st.number_input("Введите количество шагов:", value=3)

        fx_eq_1 = trapezoidal_rule(equation_1, lower_limit, upper_limit, sub_intervals)
        fx_eq_2 = trapezoidal_rule(equation_2, lower_limit, upper_limit, sub_intervals)
        st.write(f"Результат для {equation_1.__doc__} равен {fx_eq_1}")
        st.write(f"Результат для {equation_2.__doc__} равен {fx_eq_2}")

    elif integrate_type == "Метод трапеций с заданной точностью":
        upper_limit = st.number_input("Введите верхний предел:", value=15.0)
        lower_limit = st.number_input("Введите нижний предел:", value=7.0)
        precision = st.number_input("Введите желаемую точность:", value=1.2)

        fx_eq_1 = precision_trapezoidal_rule(equation_1, lower_limit, upper_limit, precision)
        fx_eq_2 = precision_trapezoidal_rule(equation_2, lower_limit, upper_limit, precision)
        st.write(f"Результат для {equation_1.__doc__} равен {fx_eq_1}")
        st.write(f"Результат для {equation_2.__doc__} равен {fx_eq_2}")

    else:
        st.markdown("Ведутся работы ... :construction_worker:")

    # st.button("Очистить результаты")


if __name__ == "__main__":
    main()
