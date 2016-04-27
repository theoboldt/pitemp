import lcd_config as CONFIG
import RPi.GPIO as GPIO
import time
import datetime


def init():
    time_begin_init = datetime.datetime.now()
    gpio_init()
    display_init()
    time_end_init = datetime.datetime.now()
    duration = time_end_init - time_begin_init

    lcd_byte(CONFIG.DISPLAY_LINE_1, CONFIG.DISPLAY_CMD)
    string('LCD init (' + "{:2.1f}".format(duration.total_seconds()) + 's)')

    lcd_byte(CONFIG.DISPLAY_LINE_2, CONFIG.DISPLAY_CMD)
    string(time_begin_init.strftime("%d.%m. %H:%M:%S"))

    time.sleep(1)


def gpio_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CONFIG.DISPLAY_E, GPIO.OUT)
    GPIO.setup(CONFIG.DISPLAY_RS, GPIO.OUT)
    GPIO.setup(CONFIG.DISPLAY_DATA4, GPIO.OUT)
    GPIO.setup(CONFIG.DISPLAY_DATA5, GPIO.OUT)
    GPIO.setup(CONFIG.DISPLAY_DATA6, GPIO.OUT)
    GPIO.setup(CONFIG.DISPLAY_DATA7, GPIO.OUT)


def display_init():
    lcd_byte(0x33, CONFIG.DISPLAY_CMD)
    lcd_byte(0x32, CONFIG.DISPLAY_CMD)
    lcd_byte(0x28, CONFIG.DISPLAY_CMD)
    lcd_byte(0x0C, CONFIG.DISPLAY_CMD)
    lcd_byte(0x06, CONFIG.DISPLAY_CMD)
    lcd_byte(0x01, CONFIG.DISPLAY_CMD)


def lcd_byte(bits, mode):
    GPIO.output(CONFIG.DISPLAY_RS, mode)
    GPIO.output(CONFIG.DISPLAY_DATA4, False)
    GPIO.output(CONFIG.DISPLAY_DATA5, False)
    GPIO.output(CONFIG.DISPLAY_DATA6, False)
    GPIO.output(CONFIG.DISPLAY_DATA7, False)
    if bits & 0x10 == 0x10:
        GPIO.output(CONFIG.DISPLAY_DATA4, True)
    if bits & 0x20 == 0x20:
        GPIO.output(CONFIG.DISPLAY_DATA5, True)
    if bits & 0x40 == 0x40:
        GPIO.output(CONFIG.DISPLAY_DATA6, True)
    if bits & 0x80 == 0x80:
        GPIO.output(CONFIG.DISPLAY_DATA7, True)
    time.sleep(CONFIG.E_DELAY)
    GPIO.output(CONFIG.DISPLAY_E, True)
    time.sleep(CONFIG.E_PULSE)
    GPIO.output(CONFIG.DISPLAY_E, False)
    time.sleep(CONFIG.E_DELAY)
    GPIO.output(CONFIG.DISPLAY_DATA4, False)
    GPIO.output(CONFIG.DISPLAY_DATA5, False)
    GPIO.output(CONFIG.DISPLAY_DATA6, False)
    GPIO.output(CONFIG.DISPLAY_DATA7, False)
    if bits & 0x01 == 0x01:
        GPIO.output(CONFIG.DISPLAY_DATA4, True)
    if bits & 0x02 == 0x02:
        GPIO.output(CONFIG.DISPLAY_DATA5, True)
    if bits & 0x04 == 0x04:
        GPIO.output(CONFIG.DISPLAY_DATA6, True)
    if bits & 0x08 == 0x08:
        GPIO.output(CONFIG.DISPLAY_DATA7, True)
    time.sleep(CONFIG.E_DELAY)
    GPIO.output(CONFIG.DISPLAY_E, True)
    time.sleep(CONFIG.E_PULSE)
    GPIO.output(CONFIG.DISPLAY_E, False)
    time.sleep(CONFIG.E_DELAY)


def top(message):
    lcd_byte(CONFIG.DISPLAY_LINE_1, CONFIG.DISPLAY_CMD)
    string(message)


def bottom(message):
    lcd_byte(CONFIG.DISPLAY_LINE_2, CONFIG.DISPLAY_CMD)
    string(message)


def string(message):
    message = message.ljust(CONFIG.DISPLAY_WIDTH, " ")
    for i in range(CONFIG.DISPLAY_WIDTH):
        lcd_byte(ord(message[i]), CONFIG.DISPLAY_CHR)


def screen(message_top, message_bottom):
    lcd_byte(CONFIG.DISPLAY_LINE_1, CONFIG.DISPLAY_CMD)
    string(message_top)

    lcd_byte(CONFIG.DISPLAY_LINE_2, CONFIG.DISPLAY_CMD)
    string(message_bottom)


def cleanup():
    GPIO.cleanup()
