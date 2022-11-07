import time


def timer(f):
    def wrapper_timer(*args, **kargs):
        start = time.time()
        output = f(*args, **kargs)
        stop = time.time()
        crono = stop-start
        return output, crono
    return wrapper_timer
