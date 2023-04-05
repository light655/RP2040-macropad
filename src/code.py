import board
import digitalio
import time
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

from key_matrix import SenseMatrix, KeyMatrix
from key_mapping import KeyMap, ShiftMap
from light_pollution import PIO_RGB

# Set the pins used for the columns and rows of the sense matrix on the PCB.
column_pins = (board.GP11, board.GP10, board.GP9)
row_pins = (board.GP14, board.GP12, board.GP13)
sense_matrix = SenseMatrix(row_pins, column_pins)

# Initialise the HID device.
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# Initialise the key matrix and read from the CSV file.
key_matrix = KeyMatrix("keys.csv", sense_matrix.row_num, sense_matrix.col_num)
press_num = [0] * 231
spam = []

# Initialise the RGB LED.
RGB = PIO_RGB(board.GP16)
RGB.set_colour(0, 0, 0)
breathe_val = [0, 10, 0]
breathe_dir = [0, 0, 1]
t1 = time.monotonic()
t2 = time.monotonic()


# The press routine checks for keys that need to be pressed and have not been pressed.
def press_routine(key_list):
    for key in key_list:
        if press_num[key] == 0:
            keyboard.press(key)

        press_num[key] += 1


# The release routine check for keys that need to released and is no longer needed to be pressed.
def release_routine(key_list):
    for key in key_list:
        press_num[key] -= 1

        if press_num[key] == 0:
            keyboard.release(key)


# Main loop.
while True:
    # Scan the matrix on the PCB.
    pressed, released = sense_matrix.scan()
    
    for p in pressed:
        i = p[0]
        j = p[1]

        # Get the mode of the switch.
        this_mode = key_matrix.get_mode(i, j)
        # Mode 1 -> single press
        # Mode 2 -> press and hold
        if this_mode in ('1', '2'):
            # Get the macro keys of the switch.
            these_keys = key_matrix.get_macro(i, j)
            press_routine(these_keys)

            if this_mode == '1':
                release_routine(these_keys)

        # Mode 3 -> print out a string
        if this_mode == '3':
            # Release other keys so that they won't interfere
            press_num = [0] * 231
            keyboard.release_all()

            # Get the keys of the string that the switch is set to print.
            these_keys = key_matrix.get_str(i, j)
            t = 0
            while t < len(these_keys):
                # Flash RGB LED when printing out characters.
                if (c := t % 9) in (0, 1, 2):
                    RGB.set_colour(10, 0, 0)
                elif c in (3, 4, 5):
                    RGB.set_colour(0, 10, 0)
                else:
                    RGB.set_colour(0, 0, 10)

                # The "Empty" key will send no code and delay 1ms.
                if these_keys[t] == KeyMap["Empty"]:
                    time.sleep(0.001)
                    t += 1 
                    continue
                # If shifting is needed, press shift and the next key.
                elif these_keys[t] == KeyMap["Shift"]:
                    keyboard.press(KeyMap["Shift"])
                    t += 1

                keyboard.press(these_keys[t])
                # Release the keys after the key is printed.
                keyboard.release_all()

                t += 1

            # Turn off the RGB LED.
            RGB.set_colour(0, 0, 0)

        # Mode 4 -> spam a set of macro keys
        if this_mode == '4':
            these_keys = key_matrix.get_macro(i, j)
            # Set the keys to spam.
            spam = sorted(these_keys)
            # Set the count for flashing LED.
            s = 0

    for r in released:
        i = r[0]
        j = r[1]

        # Get the mode of the switch.
        this_mode = key_matrix.get_mode(i, j)
        # Release the macro keys.
        if this_mode == '2':
            these_keys = key_matrix.get_macro(i, j)
            release_routine(these_keys)

        # Mode 1&3 is completed when the key on the down stroke.
        if this_mode in ('1', '3'):
            pass

        if this_mode == '4':
            # Remove the keys for spamming.
            spam = []
            # Turn off the RGB LED.
            RGB.set_colour(0, 0, 0)

    # Spam the keys every loop if there is keys to spam.        
    if len(spam) > 0:
        # Flash the RGB LED every five spam cycles.
        if s % 5 == 0:
            RGB.set_colour(0, 25, 0)

        press_routine(reversed(spam))
        time.sleep(0.01)
        release_routine(spam)

        # 40% duty cycle for the flashing LED.
        if s % 5 == 2:
            RGB.set_colour(0, 0, 0)
        # Increment the count for flashing LED.
        s += 1
    # If there is no need to spam keys, make the RGB LED breathe
    else:
		t2 = time.monotonic()
		if t2 - t1 >= 0.02:
			for i in range(3):
				if breathe_val[i] == 25 and breathe_dir[i] == 1:
					breathe_dir[i - 1] = -1
					breathe_dir[i] = 0
				elif breathe_val[i] == 0 and breathe_dir[i] == -1:
					breathe_dir[i - 1] = 1
					breathe_dir[i] = 0

				breathe_val[i] += breathe_dir[i]
			t1 = time.monotonic()
			RGB.set_colour(*breathe_val)
