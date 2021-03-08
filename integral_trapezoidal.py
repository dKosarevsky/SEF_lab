import streamlit as st
import pandas as pd
import numpy as np
from scipy.integrate import trapz, simps
import math
import sys

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


def trapezoidal_rule(func, low_limit, up_limit, sub_ints):
    sum_xi = 0.0
    h = (up_limit - low_limit) / sub_ints  # finding midpoint, (b-a)/n
    sum1 = func(low_limit) + func(up_limit)  # find the f(a) and f(b)
    for i in range(1, int(sub_ints)):
        sum_xi += func(low_limit + i * h)
    fx = (h / 2) * (sum1 + 2 * sum_xi)

    return round(fx, 5)


def equation_1(x):
    """
        sin(x)
    """
    return np.sin(x)


def equation_2(x):
    """
        cos^2(x) * ln^2(x+5)
    """
    return np.cos(x)**2 * np.log(x + 5)**2


# def integrate_with_scipy(x, y):
#     """""""""
#         finding the area under the curve
#         http://pageperso.lif.univ-mrs.fr/~francois.denis/IAAM1/scipy-html-1.0.0/generated/scipy.integrate.trapz.html
#
#         data = pd.read_table("SampleData2.txt",sep="\s+")
#         x = data["x"].values
#         y = data["y"].values
#         plt.plot(x,y)
#     """""""""
#     st.write("area under graph with trapezoidal", trapz(y, x))
#     st.write("area under graph simpson", simps(y, x))


def main():
    header()

    if st.checkbox("Показать ТЗ"):
        show_tz()

    integrate_type = st.radio(
        "Выберите метод получения чисел", (
            "Метод трапеций с заданным шагом",
            "Метод трапеций с заданной точностью",
            "Метод точки пересечения функции с осью абсцисс на заданном интервале методом дихотомии"
        )
    )
    if integrate_type == "Метод трапеций с заданным шагом":
        lower_limit = st.number_input("Input the lower limit:", value=7.0)
        upper_limit = st.number_input("Input the upper limit:", value=15.0)
        sub_intervals = st.number_input("Input the number of sub-intervals:", value=3)

        fx_eq_1 = trapezoidal_rule(equation_1, lower_limit, upper_limit, sub_intervals)
        fx_eq_2 = trapezoidal_rule(equation_2, lower_limit, upper_limit, sub_intervals)

        st.write(f"Результат для {equation_1.__doc__} равен {fx_eq_1}")
        st.write(f"Результат для {equation_2.__doc__} равен {fx_eq_2}")

    st.button("Очистить результаты")


if __name__ == "__main__":
    main()
