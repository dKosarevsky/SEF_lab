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


def plot(func, a, b, zero):
    """ отрисовка графика """
    x = np.arange(a, b, 0.001)
    y = [func(i) for i in x]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(x, y)
    if zero:
        ax.scatter(zero, 0)
    ax.axhline(0, color='black')
    ax.set_title(f"Функция {func.__doc__}")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$f(x)$")
    ax.grid(True)

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
        res = f(zero)
        err = abs(a - b)
        st.write(f"Функция {f.__doc__} пересекает ось абсцисс в точке [{round(zero, 2)}, 0]")
        # st.write(f"Остальная часть функции в нулевой точке: f (zero) = {res}")
        # st.write(f"Количество итераций: niter = {niter}")
        # st.write(f"Вектор, содержащий остатки на каждой итерации: inc = {inc}")
        # st.write(f"Длина последнего интервала: err = {err}")
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
    if calc_type[:1] == "1":
        st.write(calc_type[3:])
        c1, c2, c3 = st.beta_columns(3)
        lower_limit = c1.number_input("Введите нижний предел:", value=1.)
        upper_limit = c2.number_input("Введите верхний предел:", value=1.57)
        sub_intervals = c3.number_input("Введите шаг:", min_value=.1, value=.1)

        fx_eq_1 = trapezoidal_rule(equation_1, lower_limit, upper_limit, sub_intervals)
        st.write(f"Результат для {equation_1.__doc__} = {fx_eq_1}")

        fx_eq_2 = trapezoidal_rule(equation_2, lower_limit, upper_limit, sub_intervals)
        st.write(f"Результат для {equation_2.__doc__} = {fx_eq_2}")

    elif calc_type[:1] == "2":
        st.write(calc_type[3:])
        c1, c2, c3 = st.beta_columns(3)
        lower_limit = c1.number_input("Введите нижний предел:", value=.0)
        upper_limit = c2.number_input("Введите верхний предел:", value=1.57)
        precision = c3.number_input("Введите точность:", value=1.2)

        fx_eq_1 = precision_trapezoidal_rule(equation_1, lower_limit, upper_limit, precision)
        st.write(f"Результат для {equation_1.__doc__} = {fx_eq_1}")

        fx_eq_2 = precision_trapezoidal_rule(equation_2, lower_limit, upper_limit, precision)
        st.write(f"Результат для {equation_2.__doc__} = {fx_eq_2}")

    elif calc_type[:1] == "3":
        st.write(calc_type[3:])
        c1, c2, c3 = st.beta_columns(3)
        start_interval = c1.number_input("Начало интервала (a):", value=-5.0)
        end_interval = c2.number_input("Конец интервала (b):", value=12.5)
        epsilon = c3.number_input("Эпсилон (е):", min_value=.00000000000000000001, value=.00001)
        st.write(f"Значение Эпсилон = {epsilon}")

        zero_1 = dichotomy(equation_1, start_interval, end_interval, epsilon)
        plot(equation_1, start_interval, end_interval, zero_1)

        zero_2 = dichotomy(equation_2, start_interval, end_interval, epsilon)
        plot(equation_2, start_interval, end_interval, zero_2)

        zero_3 = dichotomy(equation_3, start_interval, end_interval, epsilon)
        plot(equation_3, start_interval, end_interval, zero_3)


if __name__ == "__main__":
    main()
