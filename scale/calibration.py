import RPi.GPIO as GPIO
import time
import sys
from hx711 import HX711
import numpy


hx = HX711(5, 6)


def cleanAndExit():
    GPIO.cleanup()
    sys.exit()


def cycle():
    hx.power_down()
    time.sleep(.001)
    hx.power_up()
    time.sleep(2)


def read_offset():
    offset_readings = []
    input('when no weight on scale hit enter: ')
    for i in range(10):
        offset_read = hx.read_average()
        print(offset_read)
        offset_readings.append(offset_read)
        cycle()
    return numpy.mean(offset_readings)


def read_calibration_weight():
    weight = input('place weight on scale (grams), type in weight and hit enter: ')
    return weight


def read_sensor_output():
    sensor_readings = []
    for i in range(10):
        sensor_reading = hx.read_average()
        sensor_readings.append(sensor_reading)
    return numpy.mean(sensor_readings)


def calibrate():
    try:
        offset = read_offset()
        calibration_weight = read_calibration_weight()
        sensor_output = read_sensor_output()
        ratio = (calibration_weight - offset) / sensor_output
        print('ratio= ' + ratio + ', offset= ' + offset)
    except SystemExit:
        cleanAndExit()


if __name__ == "__main__":
    calibrate()
