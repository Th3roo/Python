from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
import numpy as np

class QuadraticTab:
    def __init__(self, parent):
        self.parent = parent
        self.quad_inputs = {}
        self.quad_result = None

    def setup(self, tab):
        layout = QVBoxLayout()
        
        self.quad_inputs = {
            'a': self._create_input("Введите коэффициент a", 'Введите коэффициент при x²'),
            'b': self._create_input("Введите коэффициент b", 'Введите коэффициент при x'),
            'c': self._create_input("Введите коэффициент c", 'Введите свободный член')
        }
        
        buttons = {
            "Решить": self.solve_quadratic,
            "Очистить": self.clear_inputs
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
        QMessageBox.critical(self.parent, "Ошибка", message)

    def clear_inputs(self):
        for input_field in self.quad_inputs.values():
            input_field.clear()
        self.quad_result.clear()

    def get_input_values(self):
        return {key: input_field.text() 
                for key, input_field in self.quad_inputs.items()}

    def set_input_values(self, values):
        for key, value in values.items():
            if key in self.quad_inputs:
                self.quad_inputs[key].setText(value)