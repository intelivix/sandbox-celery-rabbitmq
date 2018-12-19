from calc import add
from calc import sub
from calc import mult
from calc import div
from calc import mod


class TestCalc(object):

    def test_add(self):
        assert add(4, 4) == 8

    def test_sub(self):
        assert sub(4, 4) == 0

    def test_mult(self):
        assert mult(4, 4) == 16

    def test_div(self):
        assert div(4, 4) == 1

    def test_mod(self):
        assert mod(4, 4) == 0
