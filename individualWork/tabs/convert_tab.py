from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
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

        convert_button = QPushButton("Конвертировать")
        convert_button.clicked.connect(self.convert_base)

        self.convert_result = QLabel("")

        layout.addWidget(self.number_input)
        layout.addWidget(self.from_base_input)
        layout.addWidget(self.to_base_input)
        layout.addWidget(convert_button)
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