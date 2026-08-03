# config.py
import os
from datetime import datetime

# ==========================================
# НАСТРОЙКИ СНАЙПЕРА
# ==========================================

# Дата проведения разблокировки (ГГГГ-ММ-ДД)
# Если пустая строка (""), скрипт автоматически определит сегодняшнюю дату по Пекину
TARGET_DATE = ""

# URL API Mi Community / Xiaomi для отправки заявки
TARGET_URL = "https://new.c.mi.com/api/unlock/apply"

# Имя файла, в который пользователь должен вставить свой popRunToken
TOKEN_FILE = "token.txt"

# Задержки Time Shift в миллисекундах для многопоточной отправки
TIME_SHIFTS = [150, 250, 350, 500]

# Настройки повторных попыток
MAX_RETRIES = 3
RETRY_DELAY = 0.5


def load_auth_token():
    """Загружает токен из файла token.txt. Если файла нет — создает его."""
    if not os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write("# Вставьте ваш авторизационный токен (popRunToken) в эту строку\n")
        print(f"[!] Файл {TOKEN_FILE} создан. Пожалуйста, вставьте туда ваш токен!")
        return ""
    
    with open(TOKEN_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        return lines[0] if lines else ""

# Создаем переменную AUTH_TOKEN
AUTH_TOKEN = load_auth_token()

