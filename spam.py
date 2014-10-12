import logging
from mongolog.handlers import MongoHandler
from time import sleep
from random import random, choice

log = logging.getLogger('spambot')
log.setLevel(logging.DEBUG)
log.addHandler(MongoHandler.to(db='mongolog', collection='log'))
log.addHandler(logging.StreamHandler())

LEVELS = [log.debug, log.info]
EXCEPTIONS = [Exception, ArithmeticError, BufferError, LookupError]


def buggy(fail=True):
    if fail:
        raise choice(EXCEPTIONS)('failed')
    else:
        log.warning('success')


while True:
    try:
        buggy(fail=choice([True, False]))
    except Exception as e:
        log.error(repr(e), exc_info=True)

    sleep_time = random()*10
    choice(LEVELS)('Sleeping {}'.format(sleep_time), extra={'sleep_time': sleep_time})
    sleep(sleep_time)
