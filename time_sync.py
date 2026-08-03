# time_sync.py
import ntplib
import time
from datetime import datetime
from logger import logger

def sync_time():
    """Синхронизирует локальное время с сервером NTP для максимальной точности."""
    ntp_servers = [
        'pool.ntp.org',
        'time.google.com',
        'time.cloudflare.com'
    ]
    
    client = ntplib.NTPClient()
    for server in ntp_servers:
        try:
            logger.info(f"Попытка синхронизации времени с {server}...")
            response = client.request(server, version=3, timeout=3)
            offset = response.offset
            logger.info(f"смещение: {offset:.4f} сек.")
            return offset
        except Exception as e:
            logger.warning(f"Не удалось синхронизироваться с {server}: {e}")
            
    logger.error("Не удалось синхронизировать время ни с одним NTP-сервером. Используется системное время.")
    return 0.0

def get_accurate_time(offset=0.0):
    """Возвращает точное текущее время с учетом смещения."""
    return time.time() + offset
