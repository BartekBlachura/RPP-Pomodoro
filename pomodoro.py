import machine
import utime

button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)

builtin_led = machine.Pin(25, machine.Pin.OUT)
led_external = machine.Pin(15, machine.Pin.OUT)

pomodoro_phase = False
pomodoro_stopwatch = 25  # seconds
pomodoro_count = 0

rest_phase = False
rest_stopwatch = 5  # seconds

stopwatch = 0  # seconds

builtin_led.value(0)
led_external.value(0)
start_time = utime.time()

while True:
    if not pomodoro_phase and not rest_phase:
        builtin_led.value(1)
        if button.value() == 1:
            pomodoro_phase = True
            builtin_led.value(0)
            start_time = utime.time()

    if pomodoro_phase:
        led_external.value(1)
        while stopwatch < pomodoro_stopwatch:
            stopwatch += 1 / pomodoro_stopwatch
            utime.sleep(1 / pomodoro_stopwatch)
            print(stopwatch)

        if stopwatch > pomodoro_stopwatch:
            stopwatch = 0
            pomodoro_phase = False
            led_external.value(0)
            print(utime.time() - start_time)
    if rest_phase:
        pass
