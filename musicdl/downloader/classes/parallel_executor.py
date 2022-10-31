import asyncio
from concurrent.futures import ThreadPoolExecutor
import sys
from typing import Any, Callable, Coroutine, List
from musicdl.downloader.interfaces import BaseParallelExecutor


class ParallelExecutor(BaseParallelExecutor):
    _configured: bool
    _loop: asyncio.AbstractEventLoop
    _semaphore: asyncio.Semaphore
    _thread_executor: ThreadPoolExecutor

    def __init__(self) -> None:
        self._configured = False

        if sys.platform == "win32":
            # ProactorEventLoop is required on Windows to run subprocess asynchronously
            # It is default since Python3.8. This is here for older versions
            self._loop = asyncio.ProactorEventLoop()
        else:
            self._loop = asyncio.new_event_loop()

        asyncio.set_event_loop(self._loop)


    def configure(self, threads: int) -> None:
        self._semaphore = asyncio.Semaphore(threads)
        self._thread_executor = ThreadPoolExecutor(max_workers=threads)
        self._configured = True


    def execute_function(self, function: Callable, args: List[Any], return_exceptions: bool = False) -> Any:
        if not self._configured:
            raise Exception("Parallel Executor not configured")

        tasks = [self._pool(function, arg) for arg in args]
        return self.execute_tasks(tasks, return_exceptions)


    def execute_tasks(self, tasks: List[Coroutine], return_exceptions: bool = False) -> Any:
        if not self._configured:
            raise Exception("Parallel Executor not configured")

        gatheredTasks = asyncio.gather(*(task for task in tasks), return_exceptions)
        return self._loop.run_until_complete(gatheredTasks)


    async def _pool(self, function: Callable, arg: Any):
        async with self._semaphore:
            return await self._loop.run_in_executor(
                self._thread_executor, function, arg
            )