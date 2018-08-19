import pytest

class TestMath:
    @pytest.mark.parametrize("test_input, expected", [
        ("3+5", 8),
        ("2+4", 6),
        ("6*9", 42),
    ],ids=[
        "Three plus five",
        "Two plus four",
        "Six times nine"
    ])
    def test_eval(self, test_input, expected):
        assert eval(test_input) == expected
