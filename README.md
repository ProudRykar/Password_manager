# Password manager V0.1
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

This is a simple password manager written in Tkinter. It creates a database using the built-in sqlite3 library and adds email and password data to it. Version V0.1 does not have hashed passwords (for now).

# Design
![Design](/pics/Design.png)

**Primary functions:** The program can write data to the database (Button "_Save_"), update it ("_Update_" button), and delete data from the database ("_Delete_"). You also can copy email or password in your copyboard

**Password generation:** The program has a function to generate a 25-character password.
