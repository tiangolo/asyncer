# AnyIO 4.1.0 renamed cancellable to abandon_on_cancel
import importlib
import importlib.metadata
import sys
from typing import Callable, TypeVar, Union

import anyio
import anyio.to_thread
from anyio import CapacityLimiter

if sys.version_info >= (3, 11):
    from typing import TypeVarTuple, Unpack
else:
    from typing_extensions import TypeVarTuple, Unpack

ANYIO_VERSION = importlib.metadata.version("anyio")

T_Retval = TypeVar("T_Retval")
PosArgsT = TypeVarTuple("PosArgsT")

if ANYIO_VERSION >= "4.1.0":

    async def run_sync(
        func: Callable[[Unpack[PosArgsT]], T_Retval],
        *args: Unpack[PosArgsT],
        abandon_on_cancel: bool = False,
        limiter: Union[CapacityLimiter, None] = None,
    ) -> T_Retval:
        return await anyio.to_thread.run_sync(
            func, *args, abandon_on_cancel=abandon_on_cancel, limiter=limiter
        )
else:

    async def run_sync(
        func: Callable[[Unpack[PosArgsT]], T_Retval],
        *args: Unpack[PosArgsT],
        abandon_on_cancel: bool = False,
        limiter: Union[CapacityLimiter, None] = None,
    ) -> T_Retval:
        return await anyio.to_thread.run_sync(
            func, *args, cancellable=abandon_on_cancel, limiter=limiter
        )
