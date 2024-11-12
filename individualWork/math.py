import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTabWidget, QMessageBox, QShortcut
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from sympy import symbols, solve, sympify
from PyQt5.QtCore import QSettings, QRegExp
from PyQt5.QtGui import QIntValidator, QRegExpValidator, QKeySequence
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class MathApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Математическое приложение")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.quad_tab = QWidget()
        self.graph_tab = QWidget()
        self.intersection_tab = QWidget()
        self.convert_tab = QWidget()

        self.tabs.addTab(self.quad_tab, "Квадратное уравнение")
        self.tabs.addTab(self.graph_tab, "График функции")
        self.tabs.addTab(self.intersection_tab, "Пересечение функций")
        self.tabs.addTab(self.convert_tab, "Перевод систем счисления")

        self.setup_quad_tab()
        self.setup_graph_tab()
        self.setup_intersection_tab()
        self.setup_convert_tab()

        self.settings = QSettings('MathApp', 'Settings')
        self.load_settings()

        self.statusBar = self.statusBar()
        self.statusBar.showMessage('Готов к работе')

        # Добавляем горячие клавиши
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)
        QShortcut(QKeySequence("Ctrl+W"), self, self.clear_quad_inputs)
        QShortcut(QKeySequence("Ctrl+1"), self, lambda: self.tabs.setCurrentIndex(0))
        QShortcut(QKeySequence("Ctrl+2"), self, lambda: self.tabs.setCurrentIndex(1))
        QShortcut(QKeySequence("Ctrl+3"), self, lambda: self.tabs.setCurrentIndex(2))
        QShortcut(QKeySequence("Ctrl+4"), self, lambda: self.tabs.setCurrentIndex(3))

    def setup_quad_tab(self):
        layout = QVBoxLayout()

        self.a_input = QLineEdit()
        self.a_input.setPlaceholderText("Введите коэффициент a")
        self.a_input.setStatusTip('Введите коэффициент при x²')
        self.b_input = QLineEdit()
        self.b_input.setPlaceholderText("Введите коэффициент b")
        self.b_input.setStatusTip('Введите коэффициент при x')
        self.c_input = QLineEdit()
        self.c_input.setPlaceholderText("Введите коэффициент c")
        self.c_input.setStatusTip('Введите свободный член')

        solve_button = QPushButton("Решить")
        solve_button.clicked.connect(self.solve_quadratic)

        clear_button = QPushButton("Очистить")
        clear_button.clicked.connect(self.clear_quad_inputs)

        self.quad_result = QLabel("")

        layout.addWidget(self.a_input)
        layout.addWidget(self.b_input)
        layout.addWidget(self.c_input)
        layout.addWidget(solve_button)
        layout.addWidget(clear_button)
        layout.addWidget(self.quad_result)

        self.quad_tab.setLayout(layout)

    def clear_quad_inputs(self):
        self.a_input.clear()
        self.b_input.clear()
        self.c_input.clear()
        self.quad_result.clear()    

    def setup_graph_tab(self):
        layout = QVBoxLayout()

        self.func_input = QLineEdit()
        self.func_input.setPlaceholderText("Введите функцию (например, x**2 + 2*x + 1)")

        plot_button = QPushButton("Построить график")
        plot_button.clicked.connect(self.plot_function)

        self.graph_canvas = FigureCanvas(plt.figure())
        # Создаем панель инструментов один раз при инициализации
        self.toolbar = NavigationToolbar(self.graph_canvas, self)

        layout.addWidget(self.func_input)
        layout.addWidget(plot_button)
        layout.addWidget(self.toolbar)  # Добавляем панель инструментов
        layout.addWidget(self.graph_canvas)

        self.graph_tab.setLayout(layout)

    def setup_intersection_tab(self):
        layout = QVBoxLayout()

        self.func1_input = QLineEdit()
        self.func1_input.setPlaceholderText("Введите функцию 1")
        self.func2_input = QLineEdit()
        self.func2_input.setPlaceholderText("Введите функцию 2")

        intersection_button = QPushButton("Найти пересечение")
        intersection_button.clicked.connect(self.find_intersection)

        self.intersection_result = QLabel("")

        # Создаем отдельный холст для вкладки пересечения
        self.intersection_canvas = FigureCanvas(plt.figure())

        layout.addWidget(self.func1_input)
        layout.addWidget(self.func2_input)
        layout.addWidget(intersection_button)
        layout.addWidget(self.intersection_result)
        layout.addWidget(self.intersection_canvas)

        self.intersection_tab.setLayout(layout)

    def setup_convert_tab(self):
        layout = QVBoxLayout()

        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText("Введите число")
        self.from_base_input = QLineEdit()
        self.from_base_input.setPlaceholderText("Из системы с основанием")
        self.to_base_input = QLineEdit()
        self.to_base_input.setPlaceholderText("В систему с основанием")
        # Разрешаем только цифры и буквы A-F
        self.number_input.setValidator(QRegExpValidator(QRegExp("[0-9A-Fa-f]+")))
        # Разрешаем только числа от 2 до 16
        self.from_base_input.setValidator(QIntValidator(2, 16))
        self.to_base_input.setValidator(QIntValidator(2, 16))

        convert_button = QPushButton("Конвертировать")
        convert_button.clicked.connect(self.convert_base)

        self.convert_result = QLabel("")

        layout.addWidget(self.number_input)
        layout.addWidget(self.from_base_input)
        layout.addWidget(self.to_base_input)
        layout.addWidget(convert_button)
        layout.addWidget(self.convert_result)

        self.convert_tab.setLayout(layout)

    def solve_quadratic(self):
        try:
            a = float(self.a_input.text())
            b = float(self.b_input.text())
            c = float(self.c_input.text())
            discriminant = b**2 - 4*a*c

            if discriminant > 0:
                x1 = (-b + np.sqrt(discriminant)) / (2*a)
                x2 = (-b - np.sqrt(discriminant)) / (2*a)
                self.quad_result.setText(f"Корни: x1 = {x1:.2f}, x2 = {x2:.2f}")
            elif discriminant == 0:
                x = -b / (2*a)
                self.quad_result.setText(f"Один корень: x = {x:.2f}")
            else:
                self.quad_result.setText("Нет действительных корней")
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Введите корректные числовые значения")

    def plot_function(self):
        try:
            func_str = self.func_input.text()
            x = symbols('x')
            func = sympify(func_str)

            x_vals = np.linspace(-10, 10, 1000)
            y_vals = [func.subs(x, val) for val in x_vals]

            # Очищаем фигуру полностью перед построением нового графика
            self.graph_canvas.figure.clear()
            
            # Создаем новые оси с фиксированным размером
            ax = self.graph_canvas.figure.add_subplot(111)
            ax.plot(x_vals, y_vals)
            ax.axhline(0, color='black', linewidth=0.5)
            ax.axvline(0, color='black', linewidth=0.5)
            ax.grid(True)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title(f"График функции: {func_str}")
            
            # Устанавливаем фиксированные отступы
            self.graph_canvas.figure.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
            
            self.graph_canvas.draw()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось построить график: {e}")

    def find_intersection(self):
        try:
            func1_str = self.func1_input.text()
            func2_str = self.func2_input.text()
            
            # Заменяем текстовую запись 3x на 3*x
            func1_str = func1_str.replace('x', '*x')
            func2_str = func2_str.replace('x', '*x')

            x = symbols('x')
            func1 = sympify(func1_str)
            func2 = sympify(func2_str)
            intersections = solve(func1 - func2)
            
            # Фильтруем только действительные корни
            real_intersections = [point for point in intersections if point.is_real]

            x_vals = np.linspace(-10, 10, 1000)
            y1_vals = [float(func1.subs(x, val)) for val in x_vals]
            y2_vals = [float(func2.subs(x, val)) for val in x_vals]

            ax = self.intersection_canvas.figure.subplots()
            ax.clear()
            ax.plot(x_vals, y1_vals, label=func1_str)
            ax.plot(x_vals, y2_vals, label=func2_str)
            ax.axhline(0, color='black', linewidth=0.5)
            ax.axvline(0, color='black', linewidth=0.5)
            ax.grid(True)
            ax.legend()
            
            if real_intersections:
                for point in real_intersections:
                    point_float = float(point)
                    y_val = float(func1.subs(x, point_float))
                    ax.plot(point_float, y_val, 'ro', label=f'({point_float:.2f}, {y_val:.2f})')

            ax.set_title("Пересечение функций")
            self.intersection_canvas.draw()

            if real_intersections:
                result_text = "Точки пересечения:\n"
                for point in real_intersections:
                    y = func1.subs(x, point)
                    result_text += f"({float(point):.2f}, {float(y):.2f})\n"
                self.intersection_result.setText(result_text)
            else:
                self.intersection_result.setText("Нет действительных точек пересечения")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось найти пересечение: {str(e)}")

    def convert_base(self):
        try:
            number = self.number_input.text()
            from_base = int(self.from_base_input.text())
            to_base = int(self.to_base_input.text())

            if 2 <= from_base <= 16 and 2 <= to_base <= 16:
                decimal = int(number, from_base)
                result = ""
                while decimal > 0:
                    remainder = decimal % to_base
                    if remainder < 10:
                        result = str(remainder) + result
                    else:
                        result = chr(ord('A') + remainder - 10) + result
                    decimal //= to_base
                self.convert_result.setText(f"Результат: {result}")
            else:
                QMessageBox.critical(self, "Ошибка", "Основание должно быть от 2 до 16")
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Введите корректные значения")

    def load_settings(self):
        self.func_input.setText(self.settings.value('last_function', ''))
        self.func1_input.setText(self.settings.value('last_function1', ''))
        self.func2_input.setText(self.settings.value('last_function2', ''))

    def closeEvent(self, event):
        self.settings.setValue('last_function', self.func_input.text())
        self.settings.setValue('last_function1', self.func1_input.text())
        self.settings.setValue('last_function2', self.func2_input.text())
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MathApp()
    window.show()
    sys.exit(app.exec())
