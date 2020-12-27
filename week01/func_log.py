import logging
import time

def logfun():
    logging.basicConfig(filename="logging.log",
                        level=logging.DEBUG,
                        datefmt='%H:%m:%d %x',
                        format='%(asctime)s %(name)-8s %(levelname)-8s [line: %(lineno)d] %(message)s'
                        )
    logging.info('func is start')
    logging.info('func is stop')
if __name__ == '__main__':
    logfun()

