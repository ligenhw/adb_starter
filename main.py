#!/usr/bin/env python3

import sched, time, datetime
import subprocess
import argparse
import logging; logging.basicConfig(level=logging.DEBUG)
import functools

s = sched.scheduler()

def sched_next(timedelta):
    def wrapper(func):
        @functools.wraps(func)
        def decorator(*argv, **kw):
            func(*argv, **kw)
            s.enter(timedelta.total_seconds(), 0, decorator)
            logging.info('sched next delay %s second.', timedelta.total_seconds())
        return decorator
    return wrapper

@sched_next(datetime.timedelta(days=1))
def signed(password):
    subprocess.run(["bash", "signed.sh", password])
    # mail to

def get_delay(time):
    hour, minute = time.split(':')
    delay_time = datetime.time(int(hour), int(minute))

    now = datetime.datetime.now()

    if delay_time > now.time():
        day = now.day        
    else:
        day = now.day + 1
    delay_datetime = datetime.datetime(now.year, now.month, day,
             delay_time.hour, delay_time.minute)
    dt = delay_datetime - now
    return dt.total_seconds()

parser = argparse.ArgumentParser(description='auto click welink by adb.')
parser.add_argument('-t', '--time', nargs='+', help='enter schedule time like 20:40.')
parser.add_argument('-p', '--password', help='lock screen password.')
args = parser.parse_args()

password = args.password if args.password is not None else '0000'

if args.time is None:
    delay = 0
    logging.info('schedule at now')
    s.enter(delay, 0, signed, (password,) )
else:
    for time in args.time:
        logging.info('schedule at %s.', time)
        delay = get_delay(time)
        logging.info('delay %s second.', delay)
        s.enter(delay, 0, signed, (password,) )

s.run()
