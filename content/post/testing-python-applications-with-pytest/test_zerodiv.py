import pytest

class TestDivByZero:
    def test_div_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            print(1/0)

    def test_no_error(self):
        with pytest.raises(ZeroDivisionError):
            print(1/1)
