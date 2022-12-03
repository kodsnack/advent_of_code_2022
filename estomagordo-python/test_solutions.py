day1a = __import__('1a')
day1b = __import__('1b')
day2a = __import__('2a')
day2b = __import__('2b')
day3a = __import__('3a')
day3b = __import__('3b')


def test_1a():
    result = day1a.main()
    assert(69795 == result)


def test_1b():
    result = day1b.main()
    assert(208437 == result)


def test_2a():
    result = day2a.main()
    assert(11873 == result)


def test_2b():
    result = day2b.main()
    assert(12014 == result)


def test_3a():
    result = day3a.main()
    assert(7795 == result)


def test_3b():
    result = day3b.main()
    assert(2703 == result)