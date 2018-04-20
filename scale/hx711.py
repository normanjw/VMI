import RPi.GPIO as GPIO
import sys
import time


class HX711:
    def __init__(self, dout, pd_sck, gain=128):
        """
        Set GPIO Mode, and pin for communication with HX711
        :param dout: Serial Data Output pin
        :param pd_sck: Power Down and Serial Clock Input pin
        :param gain: set gain 128, 64, 32
        """
        self.GAIN = 0
        self.OFFSET = 0
        self.SCALE = 1

        try:
            if gain is 128:
                self.GAIN = 1
            elif gain is 64:
                self.GAIN = 3
            elif gain is 32:
                self.GAIN = 2
        except:
            # Sets default GAIN
            self.GAIN = 1

        # Setup the gpio pin numbering system
        GPIO.setmode(GPIO.BCM)

        # Set the pin numbers
        self.PD_SCK = pd_sck
        self.DOUT = dout

        # Setup the GPIO Pin as output
        GPIO.setup(self.PD_SCK, GPIO.OUT)

        # Setup the GPIO Pin as input
        GPIO.setup(self.DOUT, GPIO.IN)

        # Power up the chip
        self.power_up()

    def read(self):
        """
        Read data from the HX711 chip
        :return reading from the HX711
        """

        # check if the chip is ready
        while not (GPIO.input(self.DOUT) == 0):
            pass

        GPIO.output(self.PD_SCK, True)
        GPIO.output(self.PD_SCK, False)
        count = 0

        for i in range(24):
            GPIO.output(self.PD_SCK, True)
            count = count << 1
            GPIO.output(self.PD_SCK, False)
            if (GPIO.input(self.DOUT)):
                count += 1

        GPIO.output(self.PD_SCK, True)
        count = count ^ 0x800000
        GPIO.output(self.PD_SCK, False)

        return count

    def read_average(self, times=16):
        """
        Calculate average value from
        :param times: measure times amount of times to get average
        """
        sum = 0
        for i in range(times):
            sum += self.read()
        return sum / times

    def power_down(self):
        GPIO.output(self.PD_SCK, False)
        GPIO.output(self.PD_SCK, True)

    def power_up(self):
        GPIO.output(self.PD_SCK, False)

    def read_weight_kg(self):
        """
        calculates weight in gram and converts to kg
        :return: weight in kg truncated to 3 decimal places
        """
        grams_per_kg = 1000
        weight_kg = 0
        avg = self.read_average()
        weight_grams = (avg - self.OFFSET) / self.SCALE
        if weight_grams > 0:
            weight_kg = weight_grams / grams_per_kg
        print('avg ' + str(avg) + ' g: ' + str(weight_grams) + ' kg: ' + str(weight_kg))
        return round(weight_kg, 3)

    def clean_and_exit(self):
        GPIO.cleanup()
        sys.exit()

    def cycle(self):
        self.power_down()
        time.sleep(.001)
        self.power_up()
        time.sleep(2)

    def set_offset(self, offset):
        """
        Set the offset
        :param offset: offset
        """
        self.OFFSET = offset

    def set_scale(self, scale):
        """
        Set scale
        :param scale, scale
        """
        self.SCALE = scale
