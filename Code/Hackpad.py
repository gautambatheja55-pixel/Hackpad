import usb_hid
import rotaryio
import digitalio
import board
import neopixel
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
import time

led = neopixel.NeoPixel(board.A0, 1, brightness=0.2, pixel_order=neopixel.GRBW)
led[0] = (255, 0, 0, 0)

keyboard = Keyboard(usb_hid.devices)
keyboard.release_all()
mouse = Mouse(usb_hid.devices)

RED = (255, 0, 0, 0)
GREEN = (0, 255, 0, 0)
ORANGE = (255, 165, 0, 0)

ctrl_key = digitalio.DigitalInOut(board.D10)
c_key = digitalio.DigitalInOut(board.D9)
v_key = digitalio.DigitalInOut(board.D8)

for key in [ctrl_key, c_key, v_key]:
    key.direction = digitalio.Direction.INPUT
    key.pull = digitalio.Pull.UP

encoder = rotaryio.IncrementalEncoder(board.A3, board.A4)
encoder.position = 0
last_position = 0

encoder_button = digitalio.DigitalInOut(board.A5)
encoder_button.direction = digitalio.Direction.INPUT
encoder_button.pull = digitalio.Pull.UP

prev_ctrl = True
prev_c = True
prev_v = True
prev_encoder_button = True

while True:
    if not ctrl_key.value and prev_ctrl:
        keyboard.press(Keycode.CONTROL)
        led[0] = GREEN
    elif ctrl_key.value and not prev_ctrl:
        keyboard.release(Keycode.CONTROL)
        led[0] = RED
    prev_ctrl = ctrl_key.value

    if not c_key.value and prev_c:
        keyboard.press(Keycode.C)
        led[0] = GREEN
    elif c_key.value and not prev_c:
        keyboard.release(Keycode.C)
        led[0] = RED
    prev_c = c_key.value

    if not v_key.value and prev_v:
        keyboard.press(Keycode.V)
        led[0] = GREEN
    elif v_key.value and not prev_v:
        keyboard.release(Keycode.V)
        led[0] = RED
    prev_v = v_key.value

    current_position = encoder.position
    if current_position != last_position:
        led[0] = ORANGE
        diff = (current_position - last_position) // 2
        if diff != 0:
            mouse.move(wheel=-diff)
        last_position = current_position
        time.sleep(0.05)
        led[0] = RED

    if not encoder_button.value and prev_encoder_button:
        led[0] = ORANGE
        mouse.click(Mouse.LEFT_BUTTON)
    elif encoder_button.value and not prev_encoder_button:
        led[0] = RED
    prev_encoder_button = encoder_button.value

    time.sleep(0.01)
