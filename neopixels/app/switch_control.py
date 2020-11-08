import multiprocessing
import os
import signal
import time
import datetime
import pigpio
from . import pattern, neo_pixel

def run():
    # http://abyz.me.uk/rpi/pigpio/python.html#wait_for_edge
    pi = pigpio.pi()
    pi.set_mode(14, pigpio.INPUT)
    pi.set_pull_up_down(14, pigpio.PUD_DOWN)
    pattern_index = 1
    generator = pattern.generators[pattern_index]
    print(generator)
    # proc = multiprocessing.Process(target=neo_pixel.run, args=(generator,))
    # proc.start()
    while True:
        if pi.wait_for_edge(14, pigpio.FALLING_EDGE, 1.0):
            break
        print(datetime.datetime.now(), "next edge wait")
    # os.kill(proc.pid, signal.SIGINT)
    print("stop proc")

