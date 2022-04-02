import machine
import utime as time
from pico_i2c_lcd import I2cLcd

__author__ = "Bartek Blachura"
__copyright__ = "Copyright 2022, Pomodoro Timer"
__version__ = "2.0.0"
__date__ = "02.04.2022"


work = 25 * 60  # minutes to seconds
short_break = 5 * 60  # minutes to seconds
long_break = 15 * 60  # minutes to seconds

sda = machine.Pin(0)
scl = machine.Pin(1)
i2c = machine.I2C(0, sda=sda, scl=scl, freq=400000)

I2C_ADDR = i2c.scan()[0]
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)


def pomodoro_timer(pomodoro, seconds):
    time_start = time.time()
    while seconds > 0:
        time_current = time.time()
        if (time_current - time_start) >= 1:
            time_start = time_current

            screen_time_left(pomodoro, seconds)

            seconds -= 1

    screen_time_left(pomodoro, 0)
    time.sleep(1)
    screen_press_button()


def screen_time_left(pomodoro, seconds):
    left_minutes = seconds // 60
    left_seconds = seconds - (left_minutes * 60)
    if left_minutes < 10:
        left_minutes = "0" + str(left_minutes)
    if left_seconds < 10:
        left_seconds = "0" + str(left_seconds)

    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr(pomodoro)
    lcd.move_to(11, 1)
    lcd.putstr(f"{left_minutes}:{left_seconds}")

    print(f"{pomodoro} - {left_minutes}:{left_seconds}")


def screen_hello():
    lcd.clear()
    lcd.move_to(1, 0)
    lcd.putstr("pomodoro timer")
    lcd.move_to(1, 1)
    lcd.putstr("--------------")
    time.sleep(1)

    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr(f"version: {__version__}")
    lcd.move_to(6, 1)
    lcd.putstr(f"{__date__}")
    time.sleep(1)

    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("author:")
    lcd.move_to(0, 1)
    lcd.putstr(f"{__author__}")
    time.sleep(1)


def screen_press_button():
    lcd.clear()
    lcd.move_to(2, 0)
    lcd.putstr("press button")
    lcd.move_to(4, 1)
    lcd.putstr("to start")


button = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_DOWN)

builtin_led = machine.Pin(25, machine.Pin.OUT)
led_red = machine.Pin(14, machine.Pin.OUT)
led_green = machine.Pin(15, machine.Pin.OUT)

builtin_led.value(0)
led_green.value(0)
led_red.value(0)

work_phase = False
break_phase = False
time_to_break = False

pomodoro_count = 0

screen_hello()
screen_press_button()

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
        led_red.value(1)

        pomodoro_timer("stay focused", work)

        pomodoro_count += 1
        led_red.value(0)
        work_phase = False
        time_to_break = True

    if break_phase:
        led_green.value(1)

        if (pomodoro_count % 4) == 0:
            pomodoro_timer("long break", long_break)
        else:
            pomodoro_timer("short break", short_break)

        led_green.value(0)
        break_phase = False
        time_to_break = False
