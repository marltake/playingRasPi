# The MIT License (MIT)
#
# Copyright (c) 2016 Damien P. George
# Copyright (c) 2017 Scott Shawcroft for Adafruit Industries
# Copyright (c) 2020 Otake Shigenori
#

import time
import pigpio
import copy


class NeoPixel:
    def __init__(self, pi, n, channel=0, aux=0):
        self.__pi = pi
        self.__n = n
        self.__buf = bytearray(n * 24)
        self.colors = [0] * n
        flag = 0
        if aux == 1:
            flag = 256
        self.__h = self.__pi.spi_open(channel, 6400000, flag)

    def stop(self):
        self.fill(0)
        self.show()
        self.__pi.spi_close(self.__h)

    @staticmethod
    def __color_code(color):
        if type(color) is list or type(color) is tuple:
            return ((color[0] << 16) | (color[1] << 8) | color[2])
        return color

    def set_color(self, i, color):
        self.colors[i] = NeoPixel.__color_code(color)

    def fill(self, color):
        self.colors = [NeoPixel.__color_code(color)] * self.__n

    def show(self):
        """Shows the new colors on the pixels themselves if they haven't already
        been autowritten.

        The colors may or may not be showing after this function returns because
        it may be done asynchronously."""
        self.push(self.colors)

    def push(self, colors):
        for i, c in enumerate(colors[:self.__n]):
            # RGB -> GRB
            d = ((c & 0xff0000) >> 8) | (
                (c & 0x00ff00) << 8) | ((c & 0x0000ff))
            # print('#{:06x}'.format(d))
            # MSB なので，上位ビットから変換
            for j in range(24):
                # 2進数の1桁を抽出して比較
                if ((d >> (23 - j)) & 0b1) == 0b00:
                    self.__buf[24 * i + j] = 0xE0
                else:
                    self.__buf[24 * i + j] = 0xF8
        self.__pi.spi_write(self.__h, self.__buf[:(i+1)*24])
        time.sleep(100e-6)

def run(generator, interval=0.03):
    pi = pigpio.pi()
    if not pi.connected:
        exit()
    time.sleep(0.7)  # wait for enabling drive signal
    num_pixels = 60
    pixels = NeoPixel(pi, n=num_pixels)
    try:
        while True:
            for colors in generator():
                pixels.push(colors)
                time.sleep(interval)
    # except KeyboardInterrupt:
    finally:
        pixels.stop()
        pi.stop()
        print("pigpio stopped")
