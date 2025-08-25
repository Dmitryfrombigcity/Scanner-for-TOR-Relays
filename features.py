import contextlib
import io
from functools import wraps
from typing import Callable, Coroutine, Any

from arguments import args


def modify(func: Callable[[], None]) -> Callable[[], None]:
    @wraps(func)
    def wrapper() -> None:
        if not (args.orbot or args.browser):
            return func()
        else:
            s = io.StringIO()
            with contextlib.redirect_stdout(s):
                args.top = True
                func()
            parts = s.getvalue().partition(
                "*********************************** Replace bridges for Orbot ***************************************"
                "\n"
            )
            if args.browser:
                print("\r                     ", parts[0])
            if args.orbot:
                print("\r                     ", parts[-1])

    return wrapper


def suppress(func: Callable[[], Coroutine[Any, Any, None]]) -> Callable[[], Coroutine[Any, Any, None]]:
    @wraps(func)
    async def wrapper() -> None:
        if not args.silent:
            return await func()

    return wrapper
