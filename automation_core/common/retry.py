import functools
import logging
from time import sleep, time
from typing import Callable, TypeVar, Any

from automation_core.common.logger import setup_logging

F = TypeVar('F', bound=Callable[..., Any])

def retry(timeout: int = 30, polling_interval: int = 500,
          msg: str = 'Failed with error') -> Callable[[Any], Any]:
    def decorator(func: F) -> Any:
        @functools.wraps(func)
        def wrapper(*args: str, **kwargs: int) -> Any:
            # global result
            result = None
            setup_logging()
            logger = logging.getLogger(func.__name__)
            delay_in_secs = polling_interval / 1000
            max_time = time() + timeout
            error_found = None
            while time() < max_time:
                start_time = time()
                try:
                    result = func(*args, **kwargs)
                    if result:
                        return result
                except Exception as e:
                    logger.debug('%s %r retrying ,', msg, error_found)
                    error_found = e
                end_time = time()
                execution_time = end_time - start_time

                if delay_in_secs > execution_time:
                    sleep(delay_in_secs - execution_time)

            if error_found:
                logger.debug('%s last attempt failed for %r: ', msg, error_found)
                raise error_found
            if result is None:
                logger.debug('%s last attempt failed as method is returning None ', msg)
                raise ValueError("return type should not be None")
            if result is False:
                logger.debug('%s last attempt failed as method is returning False ', msg)
                raise ValueError('return type should not be False')
            if result is not True:
                raise Exception

        return wrapper

    return decorator
