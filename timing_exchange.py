from datetime import datetime, time
import time as time_module


def is_within_time_range():
    current_time = datetime.now().time()

    # Создаем объекты времени через конструктор time() из datetime
    if (current_time >= time(23, 48, 50) or
            current_time <= time(7, 1, 30)):
        print('no trade')
        time_module.sleep(25960)

    elif (current_time >= time(18, 38, 50) and
          current_time <= time(19, 5, 30)):
        print('no trade')
        time_module.sleep(1600)

    else:
        print('___________trade_time___________')

