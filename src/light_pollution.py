import adafruit_pioasm
import board
import rp2pio

from array import array


class PIO_RGB:
    # A PIO assembly program to communicate with the onboard WS2812 RGB LED.
    # The program is the same as Adafruit's PIO example code.
    program = """
    .program ws2812
    .side_set 1
    .wrap_target
    bitloop:
        out x 1         side 0  [6]
        jmp !x do_zero  side 1  [3]
    do_one:
        jmp bitloop     side 1  [4]
    do_zero:
        nop             side 0  [4]
    .wrap
    """


    def __init__(self, pin):
        # Set the pin to send data to the WS2812 RGB LED.
        self._RGB_pin = pin
        # Assemble the program
        self._assembled = adafruit_pioasm.assemble(PIO_RGB.program)
        # Initialise the PIO state machine.
        # The pull_threshold parameter is different from the example because we will send array instead of bytes.
        self._sm = rp2pio.StateMachine(
            self._assembled,
            frequency=12800000,
            first_sideset_pin=self._RGB_pin,
            auto_pull=True,
            out_shift_right=False,
            pull_threshold=24,
        )


    # A function to restart the state machine if needed.
    def connect(self):
        self._sm.restart()


    # A function to stop the state machine if needed.
    def disconnect(self):
        self._sm.stop()


    # A function to set the colour and brightness of the RGB LED.
    def set_colour(self, R: int, G: int, B: int):
        # Construct a unsigned long like array object in the order of G-R-B.
        value = array('L', [(G << 24) + (R << 16) + (B << 8)])
        # Write the value into the state machine and send it to the WS2812 RGB LED.
        self._sm.write(value)
