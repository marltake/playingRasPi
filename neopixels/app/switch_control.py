import multiprocessing
import os
import signal
import time
import datetime
import pigpio
from . import pattern, neo_pixel


class IndexInput:
    def __init__(self):
        # config input
        pass

    @property
    def index(self):
        return 1


def _start(pattern_index):
    generator = pattern.get_generator(pattern_index)
    print("start", generator)
    proc = multiprocessing.Process(target=neo_pixel.run, args=(generator,))
    proc.start()
    return proc


def run():
    # http://abyz.me.uk/rpi/pigpio/python.html#wait_for_edge
    pi = pigpio.pi()
    pi.set_mode(14, pigpio.INPUT)
    pi.set_pull_up_down(14, pigpio.PUD_DOWN)
    index_input = IndexInput()
    proc = None
    pattern_index = None
    while True:
        if pi.wait_for_edge(14, pigpio.FALLING_EDGE, 1.0):
            next_index = index_input.index
            if proc is not None:
                os.kill(proc.pid, signal.SIGINT)
            if proc is None or next_index != pattern_index:
                pattern_index = next_index
                proc = _start(pattern_index)
            else:
                proc = None
