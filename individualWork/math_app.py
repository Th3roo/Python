from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QShortcut
from PyQt5.QtCore import QSettings
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

    def closeEvent(self, event):
        # Сохранение настроек при закрытии
        self.settings.setValue('last_function', self.graph_tab.get_function_text())
        func1, func2 = self.intersection_tab.get_functions_text()
        self.settings.setValue('last_function1', func1)
        self.settings.setValue('last_function2', func2)
        event.accept()

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = MathApp()
    window.show()
    sys.exit(app.exec())