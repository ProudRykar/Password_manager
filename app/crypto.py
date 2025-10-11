from cryptography.fernet import Fernet
import os

class CryptoManager:
    """
    Класс для шифрования и дешифрования данных с использованием Fernet.
    """

    def __init__(self, key_file="key.key"):
        """
        Инициализация шифровальщика.
        Если файл с ключом существует, ключ читается из него.
        Если нет — генерируется новый и сохраняется.
        """
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(key)
        
        self.key = key
        self.fernet = Fernet(self.key)

    def encrypt(self, data: str) -> str:
        """Шифрует строку и возвращает в виде str.

        Args:
            data (str): Строка для шифрования.

        Returns:
            str: Зашифрованная строка.
        """
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, token: str) -> str:
        """Дешифрует строку.

        Args:
            token (str): Зашифрованная строка.

        Returns:
            str: Расшифрованная строка.
        """
        return self.fernet.decrypt(token.encode()).decode()
