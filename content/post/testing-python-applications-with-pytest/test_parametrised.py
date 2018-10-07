import pytest

class TestPower:
    @pytest.mark.parametrize("testing_input, expected",
                             [
                                 ((2,3),8),
                                 ((2,2),4),
                                 ((2,1),2)
                                   ],ids=[
                            "Two to the power of three",
                            "Two to the power of two",
                            "Two to the power of one"
                             ])
    def test_power(testing_input, expected):
        assert testing_input[0]**testing_input[1]==expected
