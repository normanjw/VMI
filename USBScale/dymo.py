#!/usr/bin/env python
import os
import struct
from datetime import datetime
from time import sleep
import signal


class Scale:
    def __init__(self):
        self._currentWeight = 0
        self._environment = ''

    @property
    def environment(self):
        if not self._environment:
            self._environment = os.environ.get("ENVIRONMENT")
            if not self._environment:
                self._environment = "prod"

        return self._environment

    def getWeightInGrams(self, dev="/dev/usb/hiddev0"):
        """
        This device normally appears on /dev/usb/hiddev0, assume
        device still appears on this file handle.
        """
        # If we cannot find the USB device, return -1
        grams = -1
        try:
            with open(dev, 'r+b') as f:
                # Read 4 unsigned integers from USB device
                fmt = "IIII"
                bytes_to_read = struct.calcsize(fmt)
                r = f.read(bytes_to_read)
                usb_binary_read = struct.unpack(fmt, r)
                if len(usb_binary_read) == 4:
                    grams = usb_binary_read[3]
        except OSError as e:
            print("{0} - Failed to read from USB device".format(datetime.utcnow()))
        return grams

    def handle_alarm(self, signum, frame):
        raise Exception("signum: {0} - frame: {1}".format(signum, frame))

    def main(self):
        self._currentWeight = self.getWeightInGrams()
        signal.signal(signal.SIGALRM, self.handle_alarm)

        while True:
            try:
                signal.alarm(5)
                tmpWeight = self.getWeightInGrams()
                print(tmpWeight)
            finally:
                signal.alarm(0)
            sleep(1)


if __name__ == "__main__":
    scale = Scale()
    scale.main()
