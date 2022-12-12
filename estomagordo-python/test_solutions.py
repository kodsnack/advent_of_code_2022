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
day6a = __import__('6a')
day6b = __import__('6b')
day7a = __import__('7a')
day7b = __import__('7b')
day8a = __import__('8a')
day8b = __import__('8b')
day9a = __import__('9a')
day9b = __import__('9b')
day10a = __import__('10a')
day10b = __import__('10b')
day11a = __import__('11a')
day11b = __import__('11b')
day12a = __import__('12a')
day12b = __import__('12b')


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


def test_6a():
    result = day6a.main()
    assert(1566 == result)


def test_6b():
    result = day6b.main()
    assert(2265 == result)


def test_7a():
    result = day7a.main()
    assert(1648397 == result)


def test_7b():
    result = day7b.main()
    assert(1815525 == result)


def test_8a():
    result = day8a.main()
    assert(1816 == result)


def test_8b():
    result = day8b.main()
    assert(383520 == result)


def test_9a():
    result = day9a.main()
    assert(5513 == result)


def test_9b():
    result = day9b.main()
    assert(2427 == result)


def test_10a():
    result = day10a.main()
    assert(14860 == result)


def test_10b():
    result = day10b.main()
    assert([['#', '#', '#', '.', '.', '.', '#', '#', '.', '.', '#', '#', '#', '#', '.', '#', '#', '#', '#', '.', '#', '.', '.', '#', '.', '#', '.', '.', '#', '.', '#', '#', '#', '.', '.', '#', '.', '.', '#', '.'], ['#', '.', '.', '#', '.', '#', '.', '.', '#', '.', '.', '.', '.', '#', '.', '#', '.', '.', '.', '.', '#', '.', '.', '#', '.', '#', '.', '.', '#', '.', '#', '.', '.', '#', '.', '#', '.', '#', '.', '.'], ['#', '.', '.', '#', '.', '#', '.', '.', '.', '.', '.', '.', '#', '.', '.', '#', '#', '#', '.', '.', '#', '#', '#', '#', '.', '#', '.', '.', '#', '.', '#', '.', '.', '#', '.', '#', '#', '.', '.', '.'], ['#', '#', '#', '.', '.', '#', '.', '#', '#', '.', '.', '#', '.', '.', '.', '#', '.', '.', '.', '.', '#', '.', '.', '#', '.', '#', '.', '.', '#', '.', '#', '#', '#', '.', '.', '#', '.', '#', '.', '.'], ['#', '.', '#', '.', '.', '#', '.', '.', '#', '.', '#', '.', '.', '.', '.', '#', '.', '.', '.', '.', '#', '.', '.', '#', '.', '#', '.', '.', '#', '.', '#', '.', '#', '.', '.', '#', '.', '#', '.', '.'], ['#', '.', '.', '#', '.', '.', '#', '#', '#', '.', '#', '#', '#', '#', '.', '#', '#', '#', '#', '.', '#', '.', '.', '#', '.', '.', '#', '#', '.', '.', '#', '.', '.', '#', '.', '#', '.', '.', '#', '.']] == result)


def test_11a():
    result = day11a.main()
    assert(55944 == result)


def test_11b():
    result = day11b.main()
    assert(15117269860 == result)


def test_12a():
    result = day12a.main()
    assert(350 == result)


def test_12b():
    result = day12b.main()
    assert(349 == result)