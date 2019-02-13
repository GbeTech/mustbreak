import asyncio
import sys
import time
import subprocess
from optparse import OptionParser

parser = OptionParser()
parser.add_option('--no_interrupt', action='store_true', default=False)
parser.add_option('--lock_mins', type=int, default=10)
START = int(time.time())
options, args = parser.parse_args()
MINS = int(args[0])
print(f'MINS: {MINS}, no_interrupt: {options.no_interrupt}, lock_mins: {options.lock_mins}')


def lock():
    try:
        subprocess.run(r'c:\Sync\Scripts\lock_modifiers.exe', timeout=int(options.lock_mins) * 60)
    except subprocess.TimeoutExpired:
        return True


async def wait(required_secs):
    print(f'wait(required_secs={required_secs})')

    for i in range(required_secs):
        if i % 5 == 0:
            secs_left = required_secs - i
            mins_left = int(secs_left / 60)
            print(f'Locking in:  {mins_left}m {secs_left - mins_left * 60}s')
        await asyncio.sleep(1)


def run(secs):
    print(f'\nrun(secs={secs})')
    try:
        asyncio.run(wait(secs))
        print(f'Done asyncio.run(wait({secs})). Calling lock().')
        lock()
        print(f'Done locking.')
    except KeyboardInterrupt:
        if options.no_interrupt:
            exception_at = int(time.time())
            secs_left = START + MINS - exception_at
            print(f'''\nNO_INTERRUPT! 
    exception_at: {exception_at}
    secs_left: {secs_left}s
    Calling run({secs_left})''')

            run(secs_left)

        else:
            print(f'KeyboardInterrupt, exiting.')
            sys.exit()


run(MINS * 60)
