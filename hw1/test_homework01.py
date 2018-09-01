from itertools import islice

import pytest

from homework01 import call_count, fac, fib, flatten, gcd


@pytest.mark.parametrize('a, b', [
    (5, 120),
    (7, 5040),
    (8, 40320),
    (9, 362880)
])
def test_fac(a, b):
    assert fac(a) == b


@pytest.mark.parametrize('a, b, c', [
    (1, 1, 1),
    (2, 3, 1),
    (2, 4, 2),
    (3, 8, 1),
    (6, 9, 3),
    (54, 24, 6)
])
def test_gcd(a, b, c):
    assert gcd(a, b) == c


def test_fib():
    head = islice(fib(), 10)
    assert list(head) == [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]


@pytest.mark.parametrize('in_seq, out_seq', [
    ([], []),
    ([1, 2], [1, 2]),
    ([1, [2, [3]]], [1, 2, 3]),
    ([(1, 2), (3, 4)], [1, 2, 3, 4])
])
def test_flatten(in_seq, out_seq):
    assert list(flatten(in_seq)) == list(out_seq)


def test_call_count():

    @call_count
    def test_fn(*args, **kwargs):
        return locals()

    assert test_fn.call_count == 0

    args = (1, 2)
    kwargs = {'a': 3}
    res = test_fn(*args, **kwargs)

    assert res == {'args': args, 'kwargs': kwargs},\
        'Декоратор некорректно обрабатывает возвращаемое значение функции'

    assert test_fn.call_count == 1

    test_fn()
    test_fn()

    assert test_fn.call_count == 3

    with pytest.raises(Exception):
        test_fn.call_count = 100
