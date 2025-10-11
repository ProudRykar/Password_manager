# Модуль db

Модуль для работы с SQLite базой данных.

## Класс DBManager

**Класс для работы с SQLite базой данных.**

---
## def init:
#### Инициализирует объект DBManager.

#### Аргументы
| Аргумент | Тип | Описание |
|----------|-----|----------|
| `db_file` | `str` | Путь к базе данных. |

```python
    def __init__(self, db_file="secure.db") -> None:
        """Инициализирует объект DBManager.

        Args:
            db_file (str): Путь к базе данных.
        """
        self.conn = sqlite3.connect(db_file)
        self.create_tables()
```
---
## def create_tables:
#### Создает таблицы, если их нет.

```python
    def create_tables(self) -> None:
        """Создает таблицы, если их нет."""
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site TEXT,
            email TEXT NOT NULL,
            username TEXT,
            password TEXT NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            token TEXT NOT NULL
        )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS otps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site TEXT,
                otp TEXT
            )
        """)
        self.conn.commit()
```
---
## def add_password:
#### Добавляет пароль в базу данных.

#### Аргументы
| Аргумент | Тип | Описание |
|----------|-----|----------|
| `site` | `str` | Название сайта. |
| `email` | `str` | Электронная почта. |
| `username` | `str` | Имя пользователя. |
| `password` | `str` | Пароль. |

```python
    def add_password(self, site, email, username, password) -> None:
        """Добавляет пароль в базу данных.

        Args:
            site (str): Название сайта.
            email (str): Электронная почта.
            username (str): Имя пользователя.
            password (str): Пароль.
        """
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO passwords (site, email, username, password) VALUES (?, ?, ?, ?)",
                       (site, email, username, password))
        self.conn.commit()
```
---
## def get_passwords:
#### Возвращает список паролей из базы данных.

#### Возвращает
| Тип | Описание |
|-----|----------|
| `list` | Список паролей. |

```python
    def get_passwords(self) -> list:
        """Возвращает список паролей из базы данных.

        Returns:
            list: Список паролей.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, site, email, username, password FROM passwords")
        return cursor.fetchall()
```
---
## def add_token:
#### Добавляет токен в базу данных.

#### Аргументы
| Аргумент | Тип | Описание |
|----------|-----|----------|
| `name` | `str` | Название токена. |
| `token` | `str` | Токен. |

```python
    def add_token(self, name, token) -> None:
        """Добавляет токен в базу данных.

        Args:
            name (str): Название токена.
            token (str): Токен.
        """
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO tokens (name, token) VALUES (?, ?)", (name, token))
        self.conn.commit()
```
---
## def get_tokens:
#### Возвращает список токенов из базы данных.

#### Возвращает
| Тип | Описание |
|-----|----------|
| `list` | Список токенов. |

```python
    def get_tokens(self) -> list:
        """Возвращает список токенов из базы данных.

        Returns:
            list: Список токенов.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, token FROM tokens")
        return cursor.fetchall()
```
---
## def delete_password:
#### Удаляет пароль из базы данных.

#### Аргументы
| Аргумент | Тип | Описание |
|----------|-----|----------|
| `email` | `str` | Электронная почта. |

```python
    def delete_password(self, email) -> None:
        """Удаляет пароль из базы данных.

        Args:
            email (str): Электронная почта.
        """
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM passwords WHERE email = ?", (email,))
        self.conn.commit()
```
---
## def delete_token:
#### Удаляет токен из базы данных.

#### Аргументы
| Аргумент | Тип | Описание |
|----------|-----|----------|
| `name` | `str` | Название токена. |

```python
    def delete_token(self, name) -> None:
        """Удаляет токен из базы данных.

        Args:
            name (str): Название токена.
        """
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tokens WHERE name = ?", (name,))
        self.conn.commit()
```
---
## def add_otp:
#### Добавляет одноразовый код для сайта в базу данных.

#### Аргументы
| Аргумент | Тип | Описание |
|----------|-----|----------|
| `site` | `str` | Название сайта. |
| `otp` | `str` | Одноразовый код. |

```python
    def add_otp(self, site: str, otp: str) -> None:
        """Добавляет одноразовый код для сайта в базу данных.

        Args:
            site (str): Название сайта.
            otp (str): Одноразовый код.
        """
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO otps (site, otp) VALUES (?, ?)", (site, otp))
        self.conn.commit()
```
---
## def get_otps:
#### Возвращает список одноразовых кодов из базы данных.

#### Возвращает
| Тип | Описание |
|-----|----------|
| `list` | Список одноразовых кодов. |

```python
    def get_otps(self) -> list:
        """Возвращает список одноразовых кодов из базы данных.

        Returns:
            list: Список одноразовых кодов.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT site, otp FROM otps")
        return cursor.fetchall()
```
---
## def delete_otp:
#### Удаляет конкретный одноразовый код для сайта.

#### Аргументы
| Аргумент | Тип | Описание |
|----------|-----|----------|
| `site` | `str` | Название сайта. |
| `code` | `str` | Код для удаления. |

```python
    def delete_otp(self, site: str, code: str):
        """
        Удаляет конкретный одноразовый код для сайта.

        Args:
            site (str): Название сайта.
            code (str): Код для удаления.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT otp FROM otps WHERE site = ?", (site,))
        row = cursor.fetchone()
        if not row:
            return
        codes = [c.strip() for c in row[0].split(",") if c.strip()]
        codes = [c for c in codes if c != code]
        if codes:
            cursor.execute("UPDATE otps SET otp = ? WHERE site = ?", (",".join(codes), site))
        else:
            cursor.execute("DELETE FROM otps WHERE site = ?", (site,))
        self.conn.commit()
```
---