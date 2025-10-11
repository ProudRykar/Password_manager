## Класс LoginWindow

**Окно входа / регистрации пользователя.**

---
## def init:
#### Инициализация окна входа.

```python
    def __init__(self) -> None:
        """Инициализация окна входа."""
        super().__init__()
        self.setWindowTitle("Secure Manager — Вход")
        self.resize(400, 200)

        self.auth = AuthManager()
        self.logged_in_user = None

        # Apply stylesheet
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: #ffffff;
                border-radius: 5px;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
                padding: 5px;
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
        """)

        layout = QGridLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        self.label_info = QLabel()
        layout.addWidget(self.label_info, 0, 0, 1, 2)
        self.label_info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин")
        layout.addWidget(self.username_input, 1, 0, 1, 2)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input, 2, 0, 1, 2)

        self.submit_button = QPushButton()
        layout.addWidget(self.submit_button, 3, 0, 1, 2)

        self.submit_button.setDefault(True)
        self.submit_button.clicked.connect(self.handle_submit)
        self.setLayout(layout)

        if not self.auth.has_users():
            self.mode = "register"
            self.label_info.setText("Первый запуск — создайте пользователя")
            self.submit_button.setText("Создать пользователя")
        else:
            self.mode = "login"
            self.label_info.setText("Введите логин и пароль")
            self.submit_button.setText("Войти")
```
---
## def handle_submit:
#### Обработка регистрации или входа.

```python
    def handle_submit(self) -> None:
        """Обработка регистрации или входа."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль!")
            return

        if self.mode == "register":
            if self.auth.register_user(username, password):
                QMessageBox.information(self, "Успех", "Пользователь создан! Теперь войдите.")
                self.mode = "login"
                self.label_info.setText("Введите логин и пароль")
                self.submit_button.setText("Войти")
            else:
                QMessageBox.warning(self, "Ошибка", "Такой пользователь уже существует.")
        else:
            if self.auth.verify_user(username, password):
                self.logged_in_user = username
                self.accept()
            else:
                QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль.")
```
---