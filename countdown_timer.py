import time


def countdown_timer(seconds):
    time_start = time.time()
    while seconds > 0:
        time_current = time.time()
        if (time_current - time_start) >= 1:
            time_start = time_current
            seconds -= 1
