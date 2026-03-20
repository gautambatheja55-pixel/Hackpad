import usb_hid
import rotaryio
import digitalio
import pwmio
import board
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
import time

# RGB LED
led_r = pwmio.PWMOut(board.A0)
led_g = pwmio.PWMOut(board.A1)
led_b = pwmio.PWMOut(board.A2)

def set_color(r, g, b):
    led_r.duty_cycle = int(r / 255 * 65535)
    led_g.duty_cycle = int(g / 255 * 65535)
    led_b.duty_cycle = int(b / 255 * 65535)

set_color(255, 0, 0)

keyboard = Keyboard(usb_hid.devices)
keyboard.release_all()
mouse = Mouse(usb_hid.devices)

key1 = digitalio.DigitalInOut(board.D10)  # Ctrl
key2 = digitalio.DigitalInOut(board.D9)   # C
key3 = digitalio.DigitalInOut(board.D8)   # V

for key in [key1, key2, key3]:
    key.direction = digitalio.Direction.INPUT
    key.pull = digitalio.Pull.UP

encoder = rotaryio.IncrementalEncoder(board.A3, board.A4)
encoder.position = 0
last_position = 0

encoder_btn = digitalio.DigitalInOut(board.A5)
encoder_btn.direction = digitalio.Direction.INPUT
encoder_btn.pull = digitalio.Pull.UP

# Track previous states
prev_key1 = True
prev_key2 = True
prev_key3 = True
prev_btn = True

while True:
    # Key 1 - Ctrl (non-blocking)
    if not key1.value and prev_key1:
        keyboard.press(Keycode.CONTROL)
        set_color(0, 255, 0)
    elif key1.value and not prev_key1:
        keyboard.release(Keycode.CONTROL)
        set_color(255, 0, 0)
    prev_key1 = key1.value

    # Key 2 - C
    if not key2.value and prev_key2:
        keyboard.press(Keycode.C)
        set_color(0, 255, 0)
    elif key2.value and not prev_key2:
        keyboard.release(Keycode.C)
        set_color(255, 0, 0)
    prev_key2 = key2.value

    # Key 3 - V
    if not key3.value and prev_key3:
        keyboard.press(Keycode.V)
        set_color(0, 255, 0)
    elif key3.value and not prev_key3:
        keyboard.release(Keycode.V)
        set_color(255, 0, 0)
    prev_key3 = key3.value

    # Rotary encoder scroll
    current_position = encoder.position
    if current_position != last_position:
        set_color(255, 165, 0)
        diff = (current_position - last_position) // 2
        if diff != 0:
            mouse.move(wheel=-diff)
            last_position = current_position
        time.sleep(0.05)
        set_color(255, 0, 0)

    # Encoder button - left click
    if not encoder_btn.value and prev_btn:
        set_color(255, 165, 0)
        mouse.click(Mouse.LEFT_BUTTON)
    elif encoder_btn.value and not prev_btn:
        set_color(255, 0, 0)
    prev_btn = encoder_btn.value

    time.sleep(0.01)