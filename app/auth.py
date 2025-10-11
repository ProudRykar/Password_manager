import sqlite3
import bcrypt

class AuthManager:
    """
    Класс для управления регистрацией и авторизацией пользователей.
    """

    def __init__(self, db_file="secure.db") -> None:
        """
        Инициализирует объект AuthManager.

        Args:
            db_file (str): Путь к базе данных.
        """
        self.conn = sqlite3.connect(db_file)
        self.create_user_table()

    def create_user_table(self):
        """Создает таблицу пользователей, если её нет."""
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        """)
        self.conn.commit()

    def has_users(self) -> bool:
        """Проверяет, есть ли зарегистрированные пользователи.

        Returns:
            bool: True, если есть пользователи, False в противном случае.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        return count > 0

    def register_user(self, username: str, password: str) -> bool:
        """Регистрирует нового пользователя.

        Args:
            username (str): Имя пользователя.
            password (str): Пароль.

        Returns:
            bool: True, если пользователь успешно зарегистрирован, False в противном случае.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            return False

        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        self.conn.commit()
        return True

    def verify_user(self, username: str, password: str) -> bool:
        """Проверяет логин и пароль.

        Args:
            username (str): Имя пользователя.
            password (str): Пароль.

        Returns:
            bool: True, если логин и пароль верны, False в противном случае.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if not row:
            return False
        return bcrypt.checkpw(password.encode(), row[0])
