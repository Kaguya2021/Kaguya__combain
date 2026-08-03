# main.py
import os
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from config import TARGET_DATE, TIME_SHIFTS, TARGET_URL
from time_sync import sync_time, get_accurate_time
from sniper import run_sniper_tasks
from logger import logger

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def render_dashboard(current_time_str, remaining_str, time_shifts):
    clear_screen()
    print("=" * 50)
    print("      BOOTLOADER UNLOCK SNIPER (TERMUX EDITION)")
    print("=" * 50)
    print(" ⚠️  ВНИМАНИЕ: Не закрывайте Termux во время работы!")
    print("-" * 50)
    print(f" Текущее время:    {current_time_str}")
    print(f" До старта (Пекин): {remaining_str}")
    print("-" * 50)
    print(" Активные Time Shift задачи (в миллисекундах):")
    for i, shift in enumerate(time_shifts, 1):
        print(f"   [{i}] Смещение: +{shift} мс [ ОЖИДАНИЕ ]")
    print("=" * 50)
    print(" Логирование идет в файл unlock_sniper.log")
    print(" Нажмите Ctrl+C для отмены.")

def main():
    logger.info("Инициализация программы...")
    
    # 1. Синхронизация времени
    ntp_offset = sync_time()
    
    # 2. Автоматический расчет целевого времени (00:00:00 по Пекину, UTC+8)
    peking_tz = ZoneInfo("Asia/Shanghai")
    now_peking = datetime.now(peking_tz)
    
    # Если дата не задана в конфиге, берем сегодняшнюю дату по Пекину
    target_date_str = TARGET_DATE if TARGET_DATE else now_peking.strftime("%Y-%m-%d")
    
    # Формируем целевое время на 00:00:00 по Пекину
    target_dt_peking = datetime.strptime(f"{target_date_str} 00:00:00", "%Y-%m-%d %H:%M:%S").replace(tzinfo=peking_tz)
    
    # Если полночь по Пекину на сегодня уже прошла, можно автоматически перенести цель на следующую полночь (опционально)
    if target_dt_peking.timestamp() < get_accurate_time(ntp_offset):
        from datetime import timedelta
        target_dt_peking = target_dt_peking + timedelta(days=1)
        logger.info("Сегодняшняя полночь по Пекину уже прошла, цель перенесена на следующий день.")

    target_timestamp = target_dt_peking.timestamp()
    logger.info(f"Цель зафиксирована: {target_dt_peking.strftime('%Y-%m-%d %H:%M:%S')} (Пекинское время UTC+8)")

    # 3. Интерактивный дашборд ожидания
    try:
        while True:
            accurate_now = get_accurate_time(ntp_offset)
            dt_now = datetime.fromtimestamp(accurate_now)
            
            remaining_sec = target_timestamp - accurate_now
            
            if remaining_sec <= 0:
                logger.info("Целевое время наступило! Активация потоков...")
                break
            
            # Форматирование оставшегося времени
            hours = int(remaining_sec // 3600)
            minutes = int((remaining_sec % 3600) // 60)
            seconds = int(remaining_sec % 60)
            millis = int((remaining_sec % 1) * 1000)
            remaining_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{millis:03d}"

            render_dashboard(
                dt_now.strftime("%H:%M:%S.%f")[:-3],
                remaining_str,
                TIME_SHIFTS
            )
            
            # Обновление экрана раз в 50мс для плавной анимации таймера
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        logger.info("Программа остановлена пользователем.")
        return

    # 4. Запуск многопоточного снайпера
    results = run_sniper_tasks(target_timestamp, TIME_SHIFTS, lambda: get_accurate_time(ntp_offset))
    
    logger.info("Работа скрипта завершена.")

if __name__ == "__main__":
    main()

