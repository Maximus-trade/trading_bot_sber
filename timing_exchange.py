from datetime import datetime, time
import time as time_module

def is_within_time_range():
    current_time = datetime.now().time()

    # Временные диапазоны
    ranges = [
        (time(23, 48, 50), time(7, 1, 30)),
        (time(18, 38, 50), time(19, 5, 30))
    ]

    # Проверка текущего времени
    for start, end in ranges:
        if (start <= end and start <= current_time <= end) or \
           (start > end and (current_time >= start or current_time <= end)):
            print('no trade')
            sleep_duration = 25960 if start == time(23, 48, 50) else 1600
            time_module.sleep(sleep_duration)
            return

    print('___________trade_time___________')
