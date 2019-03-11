import asyncio
import sys
import time
import subprocess
from optparse import OptionParser
from datetime import datetime, timedelta

parser = OptionParser()
parser.add_option('--no_interrupt', action='store_true', default=False, help="Default: False")
parser.add_option('--lock_minutes', type=int, default=10, help="Duration of lock period in minutes. Default: 10")
parser.add_option('--work_minutes', type=int, default=120,
                  help="Duration of work (unlocked) period in minutes. Default: 120")
start_time = int(time.time())
options, args = parser.parse_args()
lock_minutes = int(options.lock_minutes)
work_minutes = int(options.work_minutes)

if lock_minutes >= 30:
    answer = input(f"Lock period set to {lock_minutes} minutes, are you sure? y/n ")
    if answer == 'n':
        lock_minutes = int(input('Input number of minutes '))

print(f'lock_minutes: {lock_minutes}, no_interrupt: {options.no_interrupt}')


def now(add_mins=0):
    _now = datetime.now()
    _delta = timedelta(minutes=add_mins)
    _dt = _now + _delta
    return _dt.strftime('%X')


def lock():
    try:
        subprocess.run(r'c:\Sync\Scripts\lock_modifiers.exe', timeout=lock_minutes * 60)
    except subprocess.TimeoutExpired:
        return True


async def wait(required_secs):
    print(f'wait(required_secs={required_secs})')

    for i in range(required_secs):
        if i % 5 == 0:  # print every 5 seconds
            secs_left = required_secs - i
            mins_left = int(secs_left / 60)
            print(f'Locking in:  {mins_left}m {secs_left % 60}s')
        await asyncio.sleep(1)


def run(secs):
    print(f'\nrun(secs={secs})')
    try:
        asyncio.run(wait(secs))
        print(f'{now()} Done asyncio.run(wait({secs})). Calling lock(). Release at {(now(lock_minutes))}')
        lock()
        print(f'Done locking.')
    except KeyboardInterrupt:
        if options.no_interrupt:
            exception_at = int(time.time())
            secs_left = start_time + lock_minutes - exception_at
            print(f'''\nNO_INTERRUPT! 
    exception_at: {exception_at}
    secs_left: {secs_left}s
    Calling run({secs_left})''')

            run(secs_left)

        else:
            print(f'KeyboardInterrupt, exiting.')
            sys.exit()


run(work_minutes * 60)
