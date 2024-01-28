import anyio
from asyncer import asyncify, syncify


def test_decorator():
    @syncify
    async def func(a: int):
        return a

    assert anyio.run(asyncify(func), 1) == 1


def test_decorator_with_params():
    @syncify()
    async def func(a: int):
        return a

    assert anyio.run(asyncify(func), 1) == 1


def test_inline():
    async def func(a: int):
        return a

    assert anyio.run(asyncify(syncify(func)), 1) == 1
