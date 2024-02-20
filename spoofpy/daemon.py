import threading
import time
import os
import sys
import datetime
import traceback
import logging

class SafeLoopThread(object):
    """
    A wrapper to repeatedly execute a function in a daemon thread; if the
    function crashes, automatically restarts the function.

    Usage:

    def my_func(a, b=1):
        pass

    SafeLoopThread(my_func, args=['a'], kwargs={'b': 2}, sleep_time=1)

    TODO: Rewrite this as a decorator.

    """
    def __init__(self, func, args=[], kwargs={}, sleep_time=1) -> None:

        self._func = func
        self._func_args = args
        self._func_kwargs = kwargs
        self._sleep_time = sleep_time

        th = threading.Thread(target=self._execute_repeated_func_safe)
        th.daemon = True
        th.start()

    def _repeat_func(self):
        """Repeatedly calls the function."""

        log('[SafeLoopThread] Starting %s %s %s' % (self._func, self._func_args, self._func_kwargs))

        while True:
            self._func(*self._func_args, **self._func_kwargs)
            if self._sleep_time:
                time.sleep(self._sleep_time)

    def _execute_repeated_func_safe(self):
        """Safely executes the repeated function calls."""

        while True:

            try:
                self._repeat_func()

            except Exception as e:

                err_msg = '=' * 80 + '\n'
                err_msg += 'Time: %s\n' % datetime.datetime.today()
                err_msg += 'Function: %s %s %s\n' % (self._func, self._func_args, self._func_kwargs)
                err_msg += 'Exception: %s\n' % e
                err_msg += str(traceback.format_exc()) + '\n\n\n'

                sys.stderr.write(err_msg + '\n')
                log(err_msg)

                time.sleep(self._sleep_time)
