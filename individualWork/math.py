import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTabWidget, QMessageBox, QShortcut
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from sympy import symbols, solve, sympify
from PyQt5.QtCore import QSettings, QRegExp
from PyQt5.QtGui import QIntValidator, QRegExpValidator, QKeySequence
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class TabNames:
    QUAD = "quad"
    GRAPH = "graph"
    INTERSECTION = "intersection"
    CONVERT = "convert"

    @classmethod
    def get_display_names(cls):
        return {
            cls.QUAD: "Квадратное уравнение",
            cls.GRAPH: "График функции",
            cls.INTERSECTION: "Пересечение функций",
            cls.CONVERT: "Перевод систем счисления"
        }

class MathApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('MyCompany', 'MathApp')
        self.setup_ui_components()
        self._setup_shortcuts()
        self._load_settings()

    def setup_ui_components(self):
        self._setup_window()
        self._setup_tabs()
        self._setup_status_bar()

    def _setup_window(self):
        self.setWindowTitle("Математическое приложение")
        self.setGeometry(100, 100, 800, 600)

    def _setup_tabs(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tab_widgets = self._create_tab_widgets()
        self._add_tabs_to_widget()
        self._setup_all_tabs()

    def _create_tab_widgets(self):
        return {name: QWidget() for name in TabNames.get_display_names().keys()}

    def _add_tabs_to_widget(self):
        for key, name in TabNames.get_display_names().items():
            self.tabs.addTab(self.tab_widgets[key], name)

    def _setup_status_bar(self):
        self.statusBar = self.statusBar()
        self.statusBar.showMessage('Готов к работе')

    def _setup_all_tabs(self):
        setup_methods = {
            "quad": self._setup_quad_tab,
            "graph": self._setup_graph_tab,
            "intersection": self._setup_intersection_tab,
            "convert": self._setup_convert_tab
        }
        
        for key, method in setup_methods.items():
            method(self.tab_widgets[key])

    def _setup_shortcuts(self):
        shortcuts = {
            "Ctrl+Q": self.close,
            "Ctrl+W": self.clear_quad_inputs,
            **{f"Ctrl+{i+1}": lambda i=i: self.tabs.setCurrentIndex(i) 
               for i in range(len(TabNames.get_display_names()))}
        }
        
        for key, func in shortcuts.items():
            QShortcut(QKeySequence(key), self, func)

    def _setup_quad_tab(self, tab):
        layout = QVBoxLayout()
        
        # Создаем словарь для input полей
        self.quad_inputs = {
            'a': self._create_input("Введите коэффициент a", 'Введите коэффициент при x²'),
            'b': self._create_input("Введите коэффициент b", 'Введите коэффициент при x'),
            'c': self._create_input("Введите коэффициент c", 'Введите свободный член')
        }
        
        buttons = {
            "Решить": self.solve_quadratic,
            "Очистить": self.clear_quad_inputs
        }
        
        for input_field in self.quad_inputs.values():
            layout.addWidget(input_field)
            
        for text, func in buttons.items():
            button = QPushButton(text)
            button.clicked.connect(func)
            layout.addWidget(button)
            
        self.quad_result = QLabel("")
        layout.addWidget(self.quad_result)
        
        tab.setLayout(layout)

    def _create_input(self, placeholder, status_tip):
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setStatusTip(status_tip)
        return input_field

    def solve_quadratic(self):
        try:
            coeffs = {key: float(input_field.text()) 
                     for key, input_field in self.quad_inputs.items()}
            
            discriminant = coeffs['b']**2 - 4*coeffs['a']*coeffs['c']
            
            if discriminant > 0:
                x1 = (-coeffs['b'] + np.sqrt(discriminant)) / (2*coeffs['a'])
                x2 = (-coeffs['b'] - np.sqrt(discriminant)) / (2*coeffs['a'])
                result = f"Корни: x1 = {x1:.2f}, x2 = {x2:.2f}"
            elif discriminant == 0:
                x = -coeffs['b'] / (2*coeffs['a'])
                result = f"Один корень: x = {x:.2f}"
            else:
                result = "Нет действительных корней"
                
            self.quad_result.setText(result)
        except ValueError:
            self._show_error("Введите корректные числовые значения")

    def _show_error(self, message):
        QMessageBox.critical(self, "Ошибка", message)

    def clear_quad_inputs(self):
        for input_field in self.quad_inputs.values():
            input_field.clear()
        self.quad_result.clear()    

    def _setup_graph_tab(self, tab):
        layout = QVBoxLayout()

        self.func_input = QLineEdit()
        self.func_input.setPlaceholderText("Введите функцию (например, x**2 + 2*x + 1)")

        plot_button = QPushButton("Построить график")
        plot_button.clicked.connect(self.plot_function)

        self.graph_canvas = FigureCanvas(plt.figure())
        self.toolbar = NavigationToolbar(self.graph_canvas, self)

        layout.addWidget(self.func_input)
        layout.addWidget(plot_button)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.graph_canvas)

        tab.setLayout(layout)

    def _setup_intersection_tab(self, tab):
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
        # Добавляем панель инструментов для управления графиком
        self.intersection_toolbar = NavigationToolbar(self.intersection_canvas, self)

        layout.addWidget(self.func1_input)
        layout.addWidget(self.func2_input)
        layout.addWidget(intersection_button)
        layout.addWidget(self.intersection_result)
        # Добавляем toolbar перед canvas
        layout.addWidget(self.intersection_toolbar)
        layout.addWidget(self.intersection_canvas)

        tab.setLayout(layout)

    def _setup_convert_tab(self, tab):
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

        tab.setLayout(layout)

    def _setup_common_plot(self, ax, title):
        ax.clear()
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.grid(True)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(title)
        # Устанавливаем одинаковые пределы для обоих графиков
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)

    def plot_function(self):
        try:
            self._plot_function_internal()
        except Exception as e:
            self._show_error(f"Не удалось построить график: {e}")

    def _plot_function_internal(self):
        func_str = self.func_input.text()
        x = symbols('x')
        func = sympify(func_str)
        
        x_vals, y_vals = self._calculate_function_values(func, x)
        self._draw_function_plot(x_vals, y_vals, func_str)

    def _calculate_function_values(self, func, x, points=1000):
        x_vals = np.linspace(-10, 10, points)
        y_vals = [func.subs(x, val) for val in x_vals]
        return x_vals, y_vals

    def _draw_function_plot(self, x_vals, y_vals, func_str):
        self.graph_canvas.figure.clear()
        ax = self.graph_canvas.figure.add_subplot(111)
        
        self._setup_common_plot(ax, f"График функции: {func_str}")
        ax.plot(x_vals, y_vals)
        
        self._adjust_and_draw_plot(self.graph_canvas)

    def _adjust_and_draw_plot(self, canvas):
        canvas.figure.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        canvas.draw()

    def find_intersection(self):
        try:
            func1_str = self.func1_input.text()
            func2_str = self.func2_input.text()

            x = symbols('x')
            func1 = sympify(func1_str)
            func2 = sympify(func2_str)
            intersections = solve(func1 - func2)
            
            real_intersections = [point for point in intersections if point.is_real]

            x_vals = np.linspace(-10, 10, 1000)
            y1_vals = [float(func1.subs(x, val)) for val in x_vals]
            y2_vals = [float(func2.subs(x, val)) for val in x_vals]

            self.intersection_canvas.figure.clear()
            ax = self.intersection_canvas.figure.add_subplot(111)
            
            self._setup_common_plot(ax, "Пересечение функций")
            ax.plot(x_vals, y1_vals, label=func1_str)
            ax.plot(x_vals, y2_vals, label=func2_str)
            ax.legend()
            
            if real_intersections:
                for point in real_intersections:
                    point_float = float(point)
                    y_val = float(func1.subs(x, point_float))
                    ax.plot(point_float, y_val, 'ro')

            self.intersection_canvas.figure.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
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
            self._validate_and_convert_base()
        except ValueError:
            self._show_error("Введите корректные значения")

    def _validate_and_convert_base(self):
        number = self.number_input.text()
        from_base = int(self.from_base_input.text())
        to_base = int(self.to_base_input.text())

        if not self._are_bases_valid(from_base, to_base):
            raise ValueError("Неверное основание системы счисления")

        result = self._convert_number(number, from_base, to_base)
        self.convert_result.setText(f"Результат: {result}")

    def _are_bases_valid(self, from_base, to_base):
        return 2 <= from_base <= 16 and 2 <= to_base <= 16

    def _convert_number(self, number, from_base, to_base):
        decimal = int(number, from_base)
        if decimal == 0:
            return "0"
            
        result = ""
        while decimal > 0:
            remainder = decimal % to_base
            result = self._get_digit_char(remainder) + result
            decimal //= to_base
        return result

    def _get_digit_char(self, digit):
        return str(digit) if digit < 10 else chr(ord('A') + digit - 10)

    def _load_settings(self):
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
