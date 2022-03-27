import machine
import utime

button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)

builtin_led = machine.Pin(25, machine.Pin.OUT)
led_external = machine.Pin(15, machine.Pin.OUT)

pomodoro_phase = False
pomodoro_stopwatch = 25
pomodoro_count = 0

rest_phase = False
rest_stopwatch = 5


while True:
    if pomodoro_stopwatch == 0:
        pomodoro_count += 1
        pomodoro_phase = False
        pomodoro_stopwatch = 25

    if not pomodoro_phase:
        builtin_led.value(1)
        if button.value() == 1:
            pomodoro_phase = True
    else:
        while pomodoro_stopwatch > 0:
            print(pomodoro_stopwatch)
            if pomodoro_stopwatch % 5 == 0:
                led_external.value(1)
            else:
                led_external.value(0)
            pomodoro_stopwatch -= 1
            utime.sleep(1)

