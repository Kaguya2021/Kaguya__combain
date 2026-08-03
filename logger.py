# logger.py
import logging
import sys

def setup_logger():
    logger = logging.getLogger("UnlockSniper")
    logger.setLevel(logging.DEBUG)

    # Формат вывода в терминал и файл
    formatter = logging.Formatter(
        "[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )

    # Вывод в консоль
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Запись в файл
    fh = logging.FileHandler("unlock_sniper.log", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

logger = setup_logger()
