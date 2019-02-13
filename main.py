import asyncio
import subprocess
import sys


def get_localtime_str():
    localtime = time.localtime()
    return f'{localtime.tm_hour}:{localtime.tm_min}:{localtime.tm_sec}'


async def sleep_secs(secs):
    print(f'sleep_secs({secs})')
    for i in range(secs):
        if i % 5 == 0:
            print(f'breaking in {secs - i} seconds')
        await asyncio.sleep(1)


async def sleep_mins(mins):
    print(f'sleep_mins({mins})')
    for i in range(mins * 60):
        if i % 5 == 0:
            secs_left = mins * 60 - i % 60
            mins_left = int(secs_left / 60)
            print(f'breaking in {mins_left}m {secs_left - mins_left * 60}s')
        await asyncio.sleep(1)


def run(mins):
    loop = asyncio.get_event_loop()
    started_at = time.time()
    try:
        task = asyncio.create_task(sleep_mins(mins))
        loop.run_until_complete(sleep_mins(mins))
    except KeyboardInterrupt:
        if disallow_interrupt:
            exception_at = time.time()
            secs_left = int(mins) * 60 - (started_at - exception_at)
            mins_left = int(secs_left / 60)
            print(f'\ndisallow_interrupt! {mins_left} mins left\n')
            loop.run_until_complete(sleep_mins(mins_left))
        else:
            print('KeyboardInterrupt, exiting')
            sys.exit()
    print('Done waiting')

    try:
        localtime = get_localtime_str()
        print(f'running exe, {localtime}')
        # p = subprocess.run(r'c:\Sync\Scripts\lock_modifiers.exe', timeout=10 * 60)
        # loop.run_until_complete(sleep_mins(10))
        p = subprocess.run(r'c:\Sync\Scripts\lock_modifiers.exe', timeout=5)
        loop.run_until_complete(sleep_secs(5))
    except subprocess.TimeoutExpired:
        localtime = get_localtime_str()
        print(f'exe disabled {localtime}')


if __name__ == '__main__':
    import time

    mins = sys.argv[1]
    try:
        disallow_interrupt = sys.argv[2]
    except:
        disallow_interrupt = False
    print(f'mins: {mins}, disallow_interrupt: {disallow_interrupt}')
    run(int(mins))
