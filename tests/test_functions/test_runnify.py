import anyio
from asyncer import asyncify, runnify


def test_decorator():
    @runnify
    async def func(a: int):
        return a

    assert anyio.run(asyncify(func), 1) == 1


def test_decorator_with_params():
    @runnify()
    async def func(a: int):
        return a

    assert anyio.run(asyncify(func), 1) == 1


def test_inline():
    async def func(a: int):
        return a

    assert anyio.run(asyncify(runnify(func)), 1) == 1
