import anyio
from asyncer import asyncify


def test_decorator():
    @asyncify
    def func(a: int):
        return a

    assert anyio.run(func, 1) == 1


def test_decorator_with_params():
    @asyncify()
    def func(a: int):
        return a

    assert anyio.run(func, 1) == 1


def test_inline():
    def func(a: int):
        return a

    assert anyio.run(asyncify(func), 1) == 1
