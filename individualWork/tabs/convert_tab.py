from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QIntValidator, QRegExpValidator

class ConvertTab:
    def __init__(self, parent):
        self.parent = parent
        self.number_input = None
        self.from_base_input = None
        self.to_base_input = None
        self.convert_result = None

    def setup(self, tab):
        layout = QVBoxLayout()

        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText("Введите число")
        self.from_base_input = QLineEdit()
        self.from_base_input.setPlaceholderText("Из системы с основанием")
        self.to_base_input = QLineEdit()
        self.to_base_input.setPlaceholderText("В систему с основанием")
        
        # Валидаторы для полей ввода
        self.number_input.setValidator(QRegExpValidator(QRegExp("[0-9A-Fa-f]+")))
        self.from_base_input.setValidator(QIntValidator(2, 16))
        self.to_base_input.setValidator(QIntValidator(2, 16))

        # Создаем горизонтальный layout для кнопок
        button_layout = QHBoxLayout()
        
        convert_button = QPushButton("Конвертировать")
        convert_button.clicked.connect(self.convert_base)
        clear_button = QPushButton("Очистить")
        clear_button.clicked.connect(self.clear_inputs)
        
        button_layout.addWidget(convert_button)
        button_layout.addWidget(clear_button)

        self.convert_result = QLabel("")

        layout.addWidget(self.number_input)
        layout.addWidget(self.from_base_input)
        layout.addWidget(self.to_base_input)
        layout.addLayout(button_layout)
        layout.addWidget(self.convert_result)

        tab.setLayout(layout)

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

    def _show_error(self, message):
        QMessageBox.critical(self.parent, "Ошибка", message)

    def get_values(self):
        """Получить текущие значения полей ввода"""
        return (
            self.number_input.text(),
            self.from_base_input.text(),
            self.to_base_input.text()
        )

    def set_values(self, number, from_base, to_base):
        """Установить значения полей ввода"""
        self.number_input.setText(number)
        self.from_base_input.setText(from_base)
        self.to_base_input.setText(to_base)

    def clear_inputs(self):
        self.number_input.clear()
        self.from_base_input.clear()
        self.to_base_input.clear()
        self.convert_result.clear()