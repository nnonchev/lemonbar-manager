import asyncio
from typing import List, Tuple, Dict

from connection import get_async_server_sock
from bar import Bar
try:
    from config import bar_config
except ModuleNotFoundError:
    bar_config = {}
try:
    from config import to_update
except ModuleNotFoundError:
    to_update = []
try:
    from config import to_subscribe
except ModuleNotFoundError:
    to_subscribe = []


async def main_loop(
    config: Dict
) -> None:

    async with Bar(**config) as bar:
        with get_async_server_sock() as sock:
            while True:
                obj = await sock.recv_json()
                rep = await bar.parse(obj)
                sock.send_json(rep)


async def exec_after(
    to_update: List[Tuple[int, List[str]]],
    to_subscribe: List[Tuple[str, List[str]]],
) -> None:

    """
        Create and execute processes that can either 
        run in background (triggered by events) or be executed every Nth second.

        Parameters:
            to_update: a list containing all the jobs to schedule for updates
            to_subscribe: a list containing all the jobs to schedule for background execs

        A job is a tuple which contains:
            - the delay in seconds
            - a list of the command and args to execute
    """

    async def _update(delay, cmd):
        """ 
            Creates and Executes a process every Nth second 

            Example:
                To execute the command echo "Hello world" every 2 seconds:
                    await _update(2, ["echo", "Hello world"])
        """

        while True:
            await asyncio.create_subprocess_exec(*cmd)
            await asyncio.sleep(delay)

    async def _subscribe(ev, cb):
        """ 
            Creates and Executes a process in the background triggered on an event call

            Example:
                To execute the command echo "Hello world":
                    job = (2, ["echo", "Hello world"])
                    await _subscribe([job])
        """

        event = await asyncio.create_subprocess_exec(
            *ev,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        while True:
            await asyncio.create_subprocess_exec(*cb)
            await event.stdout.readline()

    # To excute tasks in parallel:
    #     1. Store all tasks in an array/tuple/set/etc.
    #     2. loop trough each task and await
    # NOTE: If you try to await the tasks directly (before storing them in a list),
    #           the first task will block

    tasks = []

    for delay, cmd in jobs:
        tasks.append(
            asyncio.create_task(_update(delay, cmd))
        )

    for ev, cb in jobs:
        tasks.append(
            asyncio.create_task(_subscribe(ev, cb))
        )

    for task in tasks:
        await task


async def main():
    await asyncio.gather(
        main_loop(bar_config),
        exec_after(
            to_update,
            to_subscribe,
        )
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
