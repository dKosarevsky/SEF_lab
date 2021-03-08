import streamlit as st
import pandas as pd
import numpy as np
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




def main():
    header()

    # random_type = st.radio(
    #     "Выберите метод получения чисел",
    #     ("Алгоритмическая генерация", "Пользовательский ввод", "Пуассон", "Квантовая генерация")
    # )

    # st.button("Сгенерировать")
    if st.checkbox("Показать ТЗ"):
        st.markdown("""
            Вариант 7.
            
            Написать программу для приближенного вычисления определенного интеграла методами трапеций с заданным шагом, трапеций с заданной точностью, а также точки пересечения выбранной пользователем функции с осью абсцисс на заданном интервале методом дихотомии. Выбранную для проверки функцию передавать как отдельный параметр подпрограмм вычисления значений функции, интеграла, корня. 
            
            Для проверки использовать следующие функции:
            
            * sin(x)
            * cos^2(x) * ln^2(x+5)
        """)


if __name__ == "__main__":
    main()
