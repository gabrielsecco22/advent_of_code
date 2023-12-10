from solution import is_range_overlap, is_sub_range


class TestSolution:

    def test_is_sub_range(self):
        assert is_sub_range((6, 6), (4, 6)) is True
        assert is_sub_range((4, 6), (6, 6)) is False
        assert is_sub_range((2, 6), (4, 8)) is False
        assert is_sub_range((23, 98), (1, 98)) is True

    def test_is_range_overlap(self):
        assert is_range_overlap((1, 3), (2, 4)) is True
        assert is_range_overlap((1, 3), (4, 5)) is False
        assert is_range_overlap((1, 3), (3, 5)) is True
        assert is_range_overlap((1, 3), (0, 1)) is True
        assert is_range_overlap((5, 7), (7, 9)) is True
        assert is_range_overlap((2, 6), (4, 8)) is True
