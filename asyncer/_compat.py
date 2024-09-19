import sys
from typing import Callable, Tuple, TypeVar, Union

import anyio
import anyio.to_thread
from anyio import CapacityLimiter
from typing_extensions import TypeVarTuple, Unpack

if sys.version_info < (3, 10):
    from importlib_metadata import version as get_version
else:
    from importlib.metadata import version as get_version

ANYIO_VERSION: Tuple[int, ...] = tuple(
    int(num) for num in get_version("anyio").split(".")[:3]
)

T_Retval = TypeVar("T_Retval")
PosArgsT = TypeVarTuple("PosArgsT")


# AnyIO 4.1.0 renamed cancellable to abandon_on_cancel
if ANYIO_VERSION >= (4, 1):

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
