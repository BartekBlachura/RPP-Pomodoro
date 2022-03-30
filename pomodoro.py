import machine
import utime as time
from pico_i2c_lcd import I2cLcd


work = 5  # seconds
short_break = 1  # seconds
long_break = 3  # seconds

sda=machine.Pin(0)
scl=machine.Pin(1)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=100000)
lcd = I2cLcd(i2c, 0x27, 2, 16) # LCD 16x2


def work_time():
    stopwatch = work  # seconds

    while stopwatch > 0:
        print_on_screen(str(stopwatch))
        stopwatch -= 1
        time.sleep(1)

    print_on_screen("Time to break!")


def break_time(seconds):
    stopwatch = seconds  # seconds

    while stopwatch > 0:
        print_on_screen(str(stopwatch))
        stopwatch -= 1
        time.sleep(1)

    print_on_screen("Time to work!")


def print_on_screen(message):
    lcd.clear()
    lcd.putstr(message)
    print(message)


button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)

builtin_led = machine.Pin(25, machine.Pin.OUT)
led_external = machine.Pin(15, machine.Pin.OUT)

builtin_led.value(0)
led_external.value(0)

work_phase = False
break_phase = False
time_to_break = False

pomodoro_count = 0

print_on_screen("pomodoro timer")

while True:
    if not work_phase and not break_phase:
        builtin_led.value(1)
        if not time_to_break:
            if button.value() == 1:
                work_phase = True
                builtin_led.value(0)
        if time_to_break:
            if button.value() == 1:
                break_phase = True
                builtin_led.value(0)

    if work_phase:
        led_external.value(1)

        work_time()

        pomodoro_count += 1
        led_external.value(0)
        work_phase = False
        time_to_break = True

    if break_phase:
        led_external.value(1)

        if (pomodoro_count % 4) == 0:
            break_time(long_break)
        else:
            break_time(short_break)

        led_external.value(0)
        break_phase = False
        time_to_break = False
