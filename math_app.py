from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QKeySequence
from constants import TabNames
from individualWork.tabs.quad_tab import QuadraticTab
from tabs.graph_tab import GraphTab
# ... другие импорты ...

class MathApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('MyCompany', 'MathApp')
        self.quad_tab = QuadraticTab(self)
        self.graph_tab = GraphTab(self)
        # ... инициализация других табов ...
        
        self.setup_ui_components()
        self._setup_shortcuts()
        self._load_settings()

    def setup_ui_components(self):
        self._setup_window()
        self._setup_tabs()
        self._setup_status_bar()
        
    # ... остальные методы ... 