"""# try:
#     NO_INTERRUPT = sys.argv[2]
# except:
#     NO_INTERRUPT = False
from typing import List


async def sleep_mins(mins):
    print(f'sleep_mins({mins})')
    for i in range(mins * 60):
        if i % 5 == 0:
            secs_left = mins * 60 - i % 60
            mins_left = int(secs_left / 60)
            print(f'breaking in {mins_left}m {secs_left - mins_left * 60}s')
        await asyncio.sleep(1)


def get_localtime_str():
    return str(datetime.datetime.now())[17:23]"""
import asyncio
import sys
import random
import time

MINS = int(sys.argv[1])
try:
    NO_INTERRUPT = sys.argv[2]
except:
    NO_INTERRUPT = False
START = int(time.time())
print(f'MINS: {MINS}, NO_INTERRUPT: {NO_INTERRUPT}, START: {START}')
"""async def every_1s(required_mins):
    for i in range(required_mins):
        print(f'every_1s, iteration #{i}')
        await asyncio.sleep(1)
        # if random.random() >= 0.6:
        #     raise KeyboardInterrupt(i)
    return True"""


async def main(required_secs):
    print(f'main(required_secs={required_secs})')

    for i in range(required_secs):
        if i % 5 == 0:
            secs_left = required_secs - i
            mins_left = int(secs_left / 60)
            print(f'breaking in:  {mins_left}m {secs_left - mins_left * 60}s')
        await asyncio.sleep(1)

    """for i in range(required_mins):
        task = asyncio.create_task(every_1s(required_mins))
        results = await asyncio.gather(task, return_exceptions=True)

        if all(results):
            print(f'\n\ttask completed successfully, after {MINS} mins')"""


def run(secs):
    print(f'\nrun(secs={secs})')
    try:
        asyncio.run(main(secs))
        print(f'Done asyncio.run(main({secs}))')
    except KeyboardInterrupt:
        if NO_INTERRUPT:
            exception_at = int(time.time())
            has_been_running_for = exception_at - START
            secs_left = MINS - has_been_running_for
            print(f'''\nNO_INTERRUPT! 
    exception_at: {exception_at}
    has_been_running_for: {has_been_running_for}
    secs_left: {secs_left}s
    Calling run({secs_left})''')
            run(secs_left)

            """completed_mins: int = e.args[0]
            required_mins = mins - completed_mins
    
            if required_mins == 0:
                print('Completed successfully, sys.exit()')
                sys.exit()
    
            print(f'''\nKeyboardInterrupt caught
            completed_mins: {completed_mins}, calling run({required_mins})''')
            run(required_mins)"""


run(MINS)
