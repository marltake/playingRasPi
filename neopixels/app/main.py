import multiprocessing
import os
import signal
import time
from . import pattern, neo_pixel


def main():
    pattern_index = 2
    generator = pattern.generators[pattern_index]
    print(generator)
    proc = multiprocessing.Process(target=neo_pixel.run, args=(generator,))
    proc.start()
    time.sleep(4)
    os.kill(proc.pid, signal.SIGINT)


if __name__ == "__main__":
    main()
