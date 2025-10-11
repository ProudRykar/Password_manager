"""Основное окно приложения с тромя вкладками: пароли, токены и recovery коды."""
# MainWindow

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView, QMenu, QDialog, QSizePolicy, QTabBar, QLabel, QFrame, QHBoxLayout, QScrollArea
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from db import DBManager
from crypto import CryptoManager

class ExpandingTabBar(QTabBar):
    """Вкладки, которые растягиваются на всю ширину окна."""
    def tabSizeHint(self, index):
        size = super().tabSizeHint(index)
        count = self.count()
        if count > 0:
            size.setWidth(self.parent().width() // count)
        return size

    def resizeEvent(self, event):
        """Принудительно обновляем геометрию вкладок при изменении размера."""
        super().resizeEvent(event)
        self.updateGeometry()

class RecoveryCodesCard(QFrame):
    """
    Карточка с названием сайта и одноразовыми резервными кодами.
    """
    def __init__(self, site_name: str, codes: list[str], delete_callback=None, copy_callback=None):
        """
        Args:
            site_name (str): Название сайта.
            codes (list[str]): Список одноразовых кодов.
            delete_callback (callable, optional): Функция для удаления кода из БД. 
                Должна принимать аргументы (site_name, code).
        """
        super().__init__()
        self.site_name = site_name
        self.codes = codes
        self.delete_callback = delete_callback
        self.copy_callback = copy_callback
        self.code_labels = []
        self.init_ui()

    def init_ui(self) -> None:
        """Инициализация интерфейса."""
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                border-radius: 12px;
                border: 1px solid #3c3f41;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
                padding: 4px;
            }
        """)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        site_label = QLabel(self.site_name)
        site_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        site_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        site_label.setFixedWidth(160)
        main_layout.addWidget(site_label)

        codes_layout = QVBoxLayout()
        codes_layout.setSpacing(6)

        for code in self.codes:
            code_label = QLabel(code)
            code_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            code_label.setStyleSheet("""
                background-color: #3c3f41;
                border-radius: 8px;
                font-size: 16px;
                padding: 6px;
            """)
            code_label.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            code_label.customContextMenuRequested.connect(
                lambda pos, lbl=code_label: self.show_context_menu(lbl)
            )
            code_label.mouseDoubleClickEvent = lambda event, c=code: self.copy_code(c)
            codes_layout.addWidget(code_label)
            self.code_labels.append(code_label)

        main_layout.addLayout(codes_layout, 1)

    def show_context_menu(self, label: QLabel):
        """Показать контекстное меню для конкретного кода.
        Args:
            label (QLabel): Код для контекстного меню.
        """
        menu = QMenu()
        delete_action = menu.addAction("🗑 Удалить")
        action = menu.exec(label.mapToGlobal(label.rect().bottomRight()))
        if action == delete_action:
            code = label.text()
            if self.delete_callback:
                self.delete_callback(self.site_name, code)
            # Убираем код с интерфейса
            label.setParent(None)
            self.code_labels.remove(label)
            self.codes.remove(code)

    def copy_code(self, code: str):
        """Копирование кода в буфер обмена через callback или напрямую.
        Args:
            code (str): Код для копирования.
        """
        if self.copy_callback:
            self.copy_callback(self.site_name, code)
        else:
            clipboard = QApplication.clipboard()
            clipboard.setText(code)
            QMessageBox.information(self, "Скопировано", "Код скопирован в буфер обмена!")


class SecureManagerApp(QMainWindow):
    """
    Основное окно приложения с двумя вкладками: пароли и токены.
    """

    def __init__(self) -> None:
        """Инициализация основного окна приложения."""
        super().__init__()
        self.setWindowTitle("Secure Manager")
        self.resize(700, 500)

        self.crypto = CryptoManager()
        self.db = DBManager()

        self.tabs = QTabWidget()
        self.tabs.setTabBar(ExpandingTabBar())


        self.password_tab = QWidget()
        self.token_tab = QWidget()
        self.recovery_tab = QWidget()

        self.tabs.addTab(self.password_tab, "Пароли")
        self.tabs.addTab(self.token_tab, "Токены")
        self.tabs.addTab(self.recovery_tab, "Одноразовые коды")
        self.setCentralWidget(self.tabs)

        
        tab_bar = self.tabs.tabBar()
        tab_bar.setExpanding(True)
        tab_bar.setElideMode(Qt.TextElideMode.ElideNone)

        self.tabs.tabBar().setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.tabs.setStyleSheet(self.tabs.styleSheet())

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QWidget {
                background-color: #2b2b2b;
            }
            QTabWidget::pane {
                border: 1px solid #555555;
                background: #353535;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #353535;
                color: #ffffff;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: #4a90e2;
                color: #ffffff;
            }
            QTabBar::tab:hover {
                background: #4a90e2;
                color: #ffffff;
            }
            QTableWidget {
                background-color: #3c3f41;
                color: #ffffff;
                border: 1px solid #555555;
                gridline-color: #555555;
                border-radius: 5px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #4a90e2;
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #2b2b2b;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #555555;
                font-weight: bold;
                font-size: 12px;
            }
            QHeaderView::section:horizontal {
                border-bottom: 2px solid #4a90e2;
            }
            QHeaderView::section:vertical {
                background-color: #2b2b2b;
                border-right: 2px solid #4a90e2;
                min-width: 30px;
                color: #ffffff;
            }
            QLineEdit {
                background-color: #3c3f41;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 8px;
                margin: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #4a90e2;
            }
            QPushButton {
                background-color: #4a90e2;
                color: #ffffff;
                border: none;
                padding: 10px;
                border-radius: 5px;
                margin: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2a6099;
            }
            QMessageBox {
                background-color: #353535;
                color: #ffffff;
            }
            QMessageBox QLabel {
                color: #ffffff;
            }
            QMessageBox QPushButton {
                background-color: #4a90e2;
                color: #ffffff;
                border: none;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QMessageBox QPushButton:hover {
                background-color: #357abd;
            }
            QMessageBox QPushButton:pressed {
                background-color: #2a6099;
            }
            QMenu {
                background-color: #353535;
                color: #353535;
                border: 1px solid #555555;
                border-radius: 8px;
                padding: 4px;
                font-size: 14px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
            }
            QMenu::item {
                padding: 10px 24px;
                background-color: #353535;
                color: #353535;
                border-radius: 4px;
                margin: 2px 4px;
            }
            QMenu::item:selected {
                background-color: #4a90e2;
                color: #4D4D4DFF;
            }
            QMenu::item:pressed {
                background-color: #2a6099;
            }
            QMenu::icon {
                margin-right: 8px;
            }
            QMenu::separator {
                height: 1px;
                background: #555555;
                margin: 4px 8px;
            }
            QInputDialog {
                background-color: #353535;
                color: #ffffff;
            }
            QInputDialog QLineEdit {
                background-color: #3c3f41;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 8px;
            }
            QInputDialog QPushButton {
                background-color: #4a90e2;
                color: #ffffff;
                border: none;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QInputDialog QPushButton:hover {
                background-color: #357abd;
            }
            QInputDialog QPushButton:pressed {
                background-color: #2a6099;
            }
        """)

        self.init_password_tab()
        self.init_token_tab()
        self.init_recovery_tab()

    # ------------------- Вкладка паролей -------------------
    def init_password_tab(self) -> None:
        """Инициализация вкладки паролей."""
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        self.password_table = QTableWidget()
        self.password_table.setColumnCount(4)
        self.password_table.setHorizontalHeaderLabels(["Сайт", "Почта", "Логин", "Пароль"])
        self.password_table.horizontalHeader().setStretchLastSection(True)
        self.password_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.password_table.verticalHeader().setVisible(True)
        layout.addWidget(self.password_table)

        self.password_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.password_table.customContextMenuRequested.connect(self.password_context_menu)
        
        self.site_input = QLineEdit()
        self.site_input.setPlaceholderText("Ссылка на сайт")
        layout.addWidget(self.site_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Почта")
        layout.addWidget(self.email_input)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.add_password_btn = QPushButton("Добавить пароль")
        self.add_password_btn.setIcon(QIcon.fromTheme("list-add"))
        
        self.add_password_btn.clicked.connect(self.add_password)
        layout.addWidget(self.add_password_btn)

        self.password_tab.setLayout(layout)
        self.load_passwords()
        self.password_input.returnPressed.connect(self.add_password)

    def load_passwords(self) -> None:
        """Загрузка паролей из базы данных."""
        self.password_table.setRowCount(0)
        for row_data in self.db.get_passwords():
            row = self.password_table.rowCount()
            self.password_table.insertRow(row)
            for col, data in enumerate(row_data[1:]):
                if col == 3:
                    item = QTableWidgetItem("*****")
                    item.setData(Qt.ItemDataRole.UserRole, data)
                else:
                    item = QTableWidgetItem(str(data))

                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.password_table.setItem(row, col, item)

        self.password_table.cellDoubleClicked.connect(self.copy_password)

    def add_password(self) -> None:
        """Добавление пароля в базу данных."""
        site = self.site_input.text()
        email = self.email_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        if not email or not password:
            QMessageBox.warning(self, "Ошибка", "Почта и пароль обязательны!")
            return
        enc_password = self.crypto.encrypt(password)
        self.db.add_password(site, email, username, enc_password)
        self.load_passwords()
        self.site_input.clear()
        self.email_input.clear()
        self.username_input.clear()
        self.password_input.clear()

    def copy_password(self, row: int, column: int) -> None:
        """Копирование пароля в буфер обмена."""
        if column == 3:
            item = self.password_table.item(row, column)
            enc_pass = item.data(Qt.ItemDataRole.UserRole)
            dec_pass = self.crypto.decrypt(enc_pass)
            clipboard = QApplication.clipboard()
            clipboard.setText(dec_pass)

    # ------------------- Вкладка токенов -------------------
    def init_token_tab(self) -> None:
        """Инициализация вкладки токенов."""
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        self.token_table = QTableWidget()
        self.token_table.setColumnCount(2)
        self.token_table.setHorizontalHeaderLabels(["Название", "Токен"])
        self.token_table.horizontalHeader().setStretchLastSection(True)
        self.token_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.token_table.verticalHeader().setVisible(True)
        layout.addWidget(self.token_table)

        self.token_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.token_table.customContextMenuRequested.connect(self.token_context_menu)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Название токена")
        layout.addWidget(self.name_input)

        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("Токен")
        self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.token_input)

        self.add_token_btn = QPushButton("Добавить токен")
        self.add_token_btn.setIcon(QIcon.fromTheme("list-add"))
        self.add_token_btn.clicked.connect(self.add_token)
        layout.addWidget(self.add_token_btn)

        self.token_tab.setLayout(layout)
        self.load_tokens()
        self.token_input.returnPressed.connect(self.add_token)

    def load_tokens(self) -> None:
        """Загрузка токенов из базы данных."""
        self.token_table.setRowCount(0)
        for row_data in self.db.get_tokens():
            row = self.token_table.rowCount()
            self.token_table.insertRow(row)
            for col, data in enumerate(row_data[1:]):
                if col == 1:
                    item = QTableWidgetItem("*****")
                    item.setData(Qt.ItemDataRole.UserRole, data)
                else:
                    item = QTableWidgetItem(str(data))
                
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.token_table.setItem(row, col, item)

        self.token_table.cellDoubleClicked.connect(self.copy_token)

    def add_token(self) -> None:
        """Добавление токена в базу данных."""
        name = self.name_input.text()
        token = self.token_input.text()
        if not name or not token:
            QMessageBox.warning(self, "Ошибка", "Название и токен обязательны!")
            return
        enc_token = self.crypto.encrypt(token)
        self.db.add_token(name, enc_token)
        self.load_tokens()
        self.name_input.clear()
        self.token_input.clear()

    def copy_token(self, row: int, column: int) -> None:
        """Копирование токена в буфер обмена.
        Args:
            row (int): Номер строки.
            column (int): Номер столбца.
        """
        if column == 1:
            item = self.token_table.item(row, column)
            enc_token = item.data(Qt.ItemDataRole.UserRole)
            dec_token = self.crypto.decrypt(enc_token)
            clipboard = QApplication.clipboard()
            clipboard.setText(dec_token)

    def delete_password(self, row: int):
        """Удаление пароля из базы данных."""
        email = self.password_table.item(row, 1).text()
        self.db.delete_password(email)
        self.load_passwords()

    def delete_token(self, row: int):
        """Удаление токена из базы данных."""
        name = self.token_table.item(row, 0).text()
        self.db.delete_token(name)
        self.load_tokens()

    def password_context_menu(self, position) -> None:
        """Контекстное меню для таблицы паролей
        Args:
            position (QPoint): Позиция курсора.
        """
        index = self.password_table.indexAt(position)
        if not index.isValid():
            return

        menu = QMenu()
        delete_action = menu.addAction("🗑 Удалить")

        action = menu.exec(self.password_table.viewport().mapToGlobal(position))
        if action == delete_action:
            self.delete_password(index.row())

    def token_context_menu(self, position) -> None:
        """Контекстное меню для таблицы токенов
        Args:
            position (QPoint): Позиция курсора.
        """
        index = self.token_table.indexAt(position)
        if not index.isValid():
            return

        menu = QMenu()
        delete_action = menu.addAction("🗑 Удалить")

        action = menu.exec(self.token_table.viewport().mapToGlobal(position))
        if action == delete_action:
            self.delete_token(index.row())

    # ------------------- Вкладка одноразовых кодов -------------------
    def init_recovery_tab(self) -> None:
        """Инициализация вкладки одноразовых кодов с карточками."""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_content)
        self.scroll_layout.setSpacing(10)
        scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(scroll_content)
        layout.addWidget(self.scroll_area)

        self.site_input = QLineEdit()
        self.site_input.setPlaceholderText("Название сайта")
        layout.addWidget(self.site_input)

        self.otp_input = QLineEdit()
        self.otp_input.setPlaceholderText("Одноразовые коды через запятую")
        layout.addWidget(self.otp_input)

        self.add_otp_btn = QPushButton("Добавить одноразовый код")
        self.add_otp_btn.clicked.connect(self.add_otp)
        layout.addWidget(self.add_otp_btn)

        self.recovery_tab.setLayout(layout)
        self.tabs.addTab(self.recovery_tab, "Одноразовые коды")
        self.load_otps()

    def load_otps(self) -> None:
        """Загрузка OTP из базы данных и отображение через карточки с контекстным меню."""
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for site, codes_str in self.db.get_otps():
            codes = [c.strip() for c in codes_str.split(",")]
            card = RecoveryCodesCard(
                site, 
                codes, 
                delete_callback=self.delete_otp,
                copy_callback=self.copy_otp
            )
            self.scroll_layout.addWidget(card)

        self.scroll_layout.addStretch()

    def copy_otp(self, site_name: str, code: str):
        """Копирование Recovery Code в буфер обмена.

        Args:
            site_name (str): Название сайта.
            code (str): Код для копирования.
        """
        clipboard = QApplication.clipboard()
        clipboard.setText(code)
        QMessageBox.information(self, "Скопировано", f"Код для {site_name} скопирован в буфер обмена!")


    def delete_otp(self, site_name: str, code: str):
        """Удаление Recovery Code из БД и обновление интерфейса.

        Args:
            site_name (str): Название сайта.
            code (str): Код для удаления.
        """
        self.db.delete_otp(site_name, code)  # Реализуй в DBManager удаление конкретного кода
        self.load_otps()

    def add_otp(self) -> None:
        """Добавление OTP в базу данных и обновление карточек."""
        site = self.site_input.text().strip()
        otp_text = self.otp_input.text().strip()
        if not site or not otp_text:
            QMessageBox.warning(self, "Ошибка", "Название сайта и коды обязательны!")
            return
        self.db.add_otp(site, otp_text)
        self.load_otps()
        self.site_input.clear()
        self.otp_input.clear()



if __name__ == "__main__":
    app = QApplication(sys.argv)

    from login_window import LoginWindow
    login_window = LoginWindow()

    if login_window.exec() == QDialog.DialogCode.Accepted:
        window = SecureManagerApp()
        window.show()
        sys.exit(app.exec())
