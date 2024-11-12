from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QMessageBox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from sympy import symbols, sympify
import numpy as np

class GraphTab:
    def __init__(self, parent):
        self.parent = parent
        self.func_input = None
        self.graph_canvas = None
        self.toolbar = None
        
    def setup(self, tab):
        layout = QVBoxLayout()

        self.func_input = QLineEdit()
        self.func_input.setPlaceholderText("Введите функцию (например, x**2 + 2*x + 1)")

        plot_button = QPushButton("Построить график")
        plot_button.clicked.connect(self.plot_function)

        self.graph_canvas = FigureCanvasQTAgg(plt.figure())
        self.toolbar = NavigationToolbar2QT(self.graph_canvas, self.parent)

        layout.addWidget(self.func_input)
        layout.addWidget(plot_button)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.graph_canvas)

        tab.setLayout(layout)

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
        
        self._adjust_and_draw_plot()

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

    def _adjust_and_draw_plot(self):
        self.graph_canvas.figure.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        self.graph_canvas.draw()

    def _show_error(self, message):
        QMessageBox.critical(self.parent, "Ошибка", message)

    def get_function_text(self):
        return self.func_input.text()

    def set_function_text(self, text):
        self.func_input.setText(text)
        