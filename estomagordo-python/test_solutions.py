day1a = __import__('1a')
day1b = __import__('1b')


def test_1a():
    result = day1a.main()
    assert(69795 == result)


def test_1b():
    result = day1b.main()
    assert(208437 == result)