import multiprocessing
import os
import signal
import time
import datetime
import pigpio
from . import pattern, neo_pixel


class IndexInput:
    def __init__(self, pi):
        self.__pi = pi
        self.__pins = (27, 18, 17)
        for pin in self.__pins:
            pi.set_mode(pin, pigpio.INPUT)
            pi.set_pull_up_down(pin, pigpio.PUD_DOWN)

    @property
    def index(self):
        index = 0
        for pin in self.__pins:
            index *= 2
            index += self.__pi.read(pin)
        return index


def _start(pattern_index):
    generator = pattern.get_generator(pattern_index)
    print("start", generator)
    proc = multiprocessing.Process(target=neo_pixel.run, args=(generator,))
    proc.start()
    return proc


def run():
    # http://abyz.me.uk/rpi/pigpio/python.html#wait_for_edge
    pi = pigpio.pi()
    pi.set_mode(4, pigpio.INPUT)
    pi.set_pull_up_down(4, pigpio.PUD_DOWN)
    index_input = IndexInput(pi)
    proc = None
    pattern_index = None
    last_edge = 0
    while True:
        if pi.wait_for_edge(4, pigpio.FALLING_EDGE):
            if time.time() < last_edge + 1:
                continue
            last_edge = time.time()
            next_index = index_input.index
            if proc is not None:
                os.kill(proc.pid, signal.SIGINT)
            if proc is None or next_index != pattern_index:
                pattern_index = next_index
                proc = _start(pattern_index)
            else:
                proc = None
