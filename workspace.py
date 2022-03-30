
from pico_i2c_lcd import I2cLcd
from machine import I2C, Pin
import utime as time

sda=machine.Pin(0)
scl=machine.Pin(1)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=100000)
# i2c = I2C(id=1,scl=Pin(27),sda=Pin(26),freq=100000)
lcd = I2cLcd(i2c, 0x27, 2, 16) # LCD 16x2

lcd.putstr('Hello World')