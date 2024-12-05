from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QShortcut, QMenuBar, QAction, QProgressBar, QApplication
from PyQt5.QtCore import QSettings, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QKeySequence
from constants import TabNames
from tabs.quad_tab import QuadraticTab
from tabs.graph_tab import GraphTab
from tabs.intersection_tab import IntersectionTab
from tabs.convert_tab import ConvertTab

class MathApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('MyCompany', 'MathApp')
        
        # Инициализация табов
        self.quad_tab = QuadraticTab(self)
        self.graph_tab = GraphTab(self)
        self.intersection_tab = IntersectionTab(self)
        self.convert_tab = ConvertTab(self)
        
        self.setup_ui_components()
        self._setup_menu_bar()
        self._setup_shortcuts()
        self._load_settings()

    def setup_ui_components(self):
        self._setup_window()
        self._setup_tabs()
        self._setup_status_bar()

    def _setup_window(self):
        self.setWindowTitle("Математическое приложение")
        self.setGeometry(100, 100, 800, 600)
        
        self.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #C2C7CB;
                border-radius: 4px;
            }
            QTabBar::tab {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                          stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
                border: 1px solid #C4C4C3;
                border-bottom-color: #C2C7CB;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 8ex;
                padding: 8px;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 #fafafa, stop: 0.4 #f4f4f4,
                                          stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
            }
            QPushButton {
                padding: 6px 12px;
                border-radius: 4px;
                background-color: #0d6efd;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
            QLineEdit {
                padding: 6px;
                border: 1px solid #ced4da;
                border-radius: 4px;
            }
        """)

    def _setup_tabs(self):
        self.tabs = QTabWidget()
        self.tabs.setMovable(True)  # Возможность перетаскивания вкладок
        self.tabs.setTabPosition(QTabWidget.North)  # Положение вкладок сверху
        self.tabs.currentChanged.connect(self._animate_tab_transition)
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
        
        # Добавить прогресс-бар
        self.progress = QProgressBar()
        self.progress.setMaximumWidth(150)
        self.progress.hide()
        
        self.statusBar.addPermanentWidget(self.progress)
        self.statusBar.showMessage('Готов к работе')

    def _setup_all_tabs(self):
        tab_instances = {
            TabNames.QUAD: self.quad_tab,
            TabNames.GRAPH: self.graph_tab,
            TabNames.INTERSECTION: self.intersection_tab,
            TabNames.CONVERT: self.convert_tab
        }
        
        for name, instance in tab_instances.items():
            instance.setup(self.tab_widgets[name])

    def _setup_shortcuts(self):
        shortcuts = {
            "Ctrl+Q": self.close,
            "Ctrl+W": self.quad_tab.clear_inputs,
            **{f"Ctrl+{i+1}": lambda i=i: self.tabs.setCurrentIndex(i) 
               for i in range(len(TabNames.get_display_names()))}
        }
        
        for key, func in shortcuts.items():
            QShortcut(QKeySequence(key), self, func)

    def _load_settings(self):
        self.graph_tab.set_function_text(self.settings.value('last_function', ''))
        self.intersection_tab.set_functions_text(
            self.settings.value('last_function1', ''),
            self.settings.value('last_function2', '')
        )
        
        quad_values = {
            'a': self.settings.value('quad_a', ''),
            'b': self.settings.value('quad_b', ''),
            'c': self.settings.value('quad_c', '')
        }
        self.quad_tab.set_input_values(quad_values)
        
        self.convert_tab.set_values(
            self.settings.value('convert_number', ''),
            self.settings.value('convert_from_base', ''),
            self.settings.value('convert_to_base', '')
        )

    def closeEvent(self, event):
        self.settings.setValue('last_function', self.graph_tab.get_function_text())
        func1, func2 = self.intersection_tab.get_functions_text()
        self.settings.setValue('last_function1', func1)
        self.settings.setValue('last_function2', func2)
        
        quad_values = self.quad_tab.get_input_values()
        for key, value in quad_values.items():
            self.settings.setValue(f'quad_{key}', value)
            
        number, from_base, to_base = self.convert_tab.get_values()
        self.settings.setValue('convert_number', number)
        self.settings.setValue('convert_from_base', from_base)
        self.settings.setValue('convert_to_base', to_base)
        
        event.accept()

    def _setup_menu_bar(self):
        menubar = self.menuBar()
        # добавить другие пункты меню в будущем
        pass

    def _animate_tab_transition(self, index):
        widget = self.tabs.currentWidget()
        if widget:
            animation = QPropertyAnimation(widget, b"pos")
            animation.setDuration(200)
            animation.setStartValue(widget.pos())
            animation.setEndValue(widget.pos())
            animation.setEasingCurve(QEasingCurve.OutCubic)
            animation.start()

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = MathApp()
    window.show()
    sys.exit(app.exec())