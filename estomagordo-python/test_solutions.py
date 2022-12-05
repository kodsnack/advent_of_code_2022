day1a = __import__('1a')
day1b = __import__('1b')
day2a = __import__('2a')
day2b = __import__('2b')
day3a = __import__('3a')
day3b = __import__('3b')
day4a = __import__('4a')
day4b = __import__('4b')
day5a = __import__('5a')
day5b = __import__('5b')


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


def test_4a():
    result = day4a.main()
    assert(494 == result)


def test_4b():
    result = day4b.main()
    assert(833 == result)


def test_5a():
    result = day5a.main()
    assert('PSNRGBTFT' == result)


def test_5b():
    result = day5b.main()
    assert('BNTZFPMMW' == result)