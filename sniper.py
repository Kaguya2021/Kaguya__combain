# sniper.py
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from logger import logger
from config import AUTH_TOKEN, TARGET_URL, MAX_RETRIES, RETRY_DELAY

def send_request_task(shift_ms, target_timestamp, offset_func):
    """Задача отправки запроса с учетом конкретного Time Shift."""
    # Вычисляем точное время срабатывания для этого шифта
    target_time_with_shift = target_timestamp + (shift_ms / 1000.0)
    
    logger.info(f"[{shift_ms}ms] Задача инициализирована. Ожидание старта...")

    while True:
        current_time = offset_func()
        remaining = target_time_with_shift - current_time
        
        if remaining <= 0:
            break
        elif remaining > 1:
            time.sleep(0.5)
        elif remaining > 0.1:
            time.sleep(0.01)
        else:
            # Микросон для точности в последние миллисекунды
            pass

    logger.info(f"[{shift_ms}ms] Время X достигнуто! Отправка запроса...")

    # Попытки отправки с обработкой ошибок
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Android; Mobile)"
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            start_req = time.time()
            # Здесь выполняется запрос к API заявки (либо имитация клика через браузерную сессию)
            response = requests.post(TARGET_URL, headers=headers, json={"action": "apply"}, timeout=5)
            latency = (time.time() - start_req) * 1000

            if response.status_code == 200:
                logger.info(f"[{shift_ms}ms] УСПЕХ! Ответ сервера: {response.text} (Задержка: {latency:.1f}мс)")
                return True
            else:
                logger.warning(f"[{shift_ms}ms] Попытка {attempt}: Сервер вернул код {response.status_code}: {response.text}")
        
        except Exception as e:
            logger.error(f"[{shift_ms}ms] Попытка {attempt} завершилась ошибкой: {e}")

        if attempt < MAX_RETRIES:
            time.sleep(RETRY_DELAY)

    logger.error(f"[{shift_ms}ms] Все попытки отправки исчерпаны.")
    return False

def run_sniper_tasks(target_timestamp, time_shifts, offset_func):
    """Запускает каждый Time Shift как независимый поток."""
    logger.info(f"Запуск {len(time_shifts)} независимых потоков Time Shift...")
    
    with ThreadPoolExecutor(max_workers=len(time_shifts)) as executor:
        futures = [
            executor.submit(send_request_task, shift, target_timestamp, offset_func)
            for shift in time_shifts
        ]
        results = [f.result() for f in futures]
    
    return results
