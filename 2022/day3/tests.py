from solution import binary_search, split_line, get_priority, solution1, solution2


class TestSolution:

    def test_binary_search(self):
        assert binary_search('a', ['a', 'b', 'c']) == 0
        assert binary_search('b', ['a', 'b', 'c']) == 1
        assert binary_search('c', ['a', 'b', 'c']) == 2
        assert binary_search('d', ['a', 'b', 'c']) == -1

    def test_split_line(self):
        assert split_line('abcde') == ('ab', 'cde')
        assert split_line('abcdef') == ('abc', 'def')
        assert split_line('tdltdtmhlRNCBcwmHr') == ('tdltdtmhl', 'RNCBcwmHr')

    def test_get_priority(self):
        assert get_priority('p') == 16
        assert get_priority('A') == 27
        assert get_priority('z') == 26
        assert get_priority('Z') == 52

    def test_solution1(self):
        """
        test cases:
        vJrwpWtwJgWrhcsFMMfFFhFp - 16(p)
        jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL - 38(L)
        PmmdzqPrVvPwwTWBwg - 42(P)
        wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn - 22(v)
        ttgJtRGJQctTZtZT - 20(t)
        CrZsJsPPZsGzwwsLwLmpwMDw - 19(s)
        """
        assert solution1(['vJrwpWtwJgWrhcsFMMfFFhFp']) == 16
        assert solution1(['jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL']) == 38
        assert solution1(['PmmdzqPrVvPwwTWBwg']) == 42
        assert solution1(['wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn']) == 22
        assert solution1(['ttgJtRGJQctTZtZT']) == 20
        assert solution1(['CrZsJsPPZsGzwwsLwLmpwMDw']) == 19

    def test_solution2(self):
        """
        test cases:
        ["vJrwpWtwJgWrhcsFMMfFFhFp", "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL", "PmmdzqPrVvPwwTWBwg"] - 18(r)
        ["wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn", "ttgJtRGJQctTZtZT", "CrZsJsPPZsGzwwsLwLmpwMDw"] - 52(Z)
        """
        assert solution2(["vJrwpWtwJgWrhcsFMMfFFhFp", "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL", "PmmdzqPrVvPwwTWBwg"]) == 18
        assert solution2(["wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn", "ttgJtRGJQctTZtZT", "CrZsJsPPZsGzwwsLwLmpwMDw"]) == 52

# if __name__ == '__main__':
    # unittest.main()
#     test_binary_search()
#     test_split_line()
#     test_get_priority()
#     test_solution1()
#     test_solution2()
#     print('All tests passed!')
