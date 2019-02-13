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

ITERATIONS = int(sys.argv[1])

async def every_1s(required_iterations):
    completed_iterations = 0
    for i in range(required_iterations):
        print(f'every_1s, iteration #{completed_iterations}')
        await asyncio.sleep(1)
        completed_iterations += 1
        if random.random() >= 0.6:
            raise KeyboardInterrupt(completed_iterations)
    return True

async def main(required_iterations):
    print(f'main(required_iterations={required_iterations})')
    for i in range(required_iterations):
        task = asyncio.create_task(every_1s(required_iterations))
        results = await asyncio.gather(task, return_exceptions=True)

        if all(results):
            print(f'\n\ttask completed successfully, after {ITERATIONS} iterations')

def run(iterations):
    print(f'\nrun(iterations={iterations})')
    try:
        asyncio.run(main(iterations))
    except KeyboardInterrupt as e:
        completed_iterations: int = e.args[0]
        required_iterations = iterations - completed_iterations

        if required_iterations == 0:
            print('Completed successfully, sys.exit()')
            sys.exit()

        print(f'''\nKeyboardInterrupt caught
        completed_iterations: {completed_iterations}, calling run({required_iterations})''')
        run(required_iterations)


run(ITERATIONS)
