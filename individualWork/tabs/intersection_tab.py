from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from sympy import symbols, solve, sympify
import numpy as np

class IntersectionTab:
    def __init__(self, parent):
        self.parent = parent
        self.func1_input = None
        self.func2_input = None
        self.intersection_result = None
        self.intersection_canvas = None
        self.intersection_toolbar = None

    def setup(self, tab):
        layout = QVBoxLayout()

        self.func1_input = QLineEdit()
        self.func1_input.setPlaceholderText("Введите функцию 1")
        self.func2_input = QLineEdit()
        self.func2_input.setPlaceholderText("Введите функцию 2")

        intersection_button = QPushButton("Найти пересечение")
        intersection_button.clicked.connect(self.find_intersection)

        self.intersection_result = QLabel("")

        self.intersection_canvas = FigureCanvasQTAgg(plt.figure())
        self.intersection_toolbar = NavigationToolbar2QT(self.intersection_canvas, self.parent)

        layout.addWidget(self.func1_input)
        layout.addWidget(self.func2_input)
        layout.addWidget(intersection_button)
        layout.addWidget(self.intersection_result)
        layout.addWidget(self.intersection_toolbar)
        layout.addWidget(self.intersection_canvas)

        tab.setLayout(layout)

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
            self._show_error(f"Не удалось найти пересечение: {str(e)}")

    def _setup_common_plot(self, ax, title):
        ax.clear()
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.grid(True)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(title)
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)

    def _show_error(self, message):
        QMessageBox.critical(self.parent, "Ошибка", message)

    def get_functions_text(self):
        return self.func1_input.text(), self.func2_input.text()

    def set_functions_text(self, func1_text, func2_text):
        self.func1_input.setText(func1_text)
        self.func2_input.setText(func2_text) 