import finfun as ff
import unittest


class TestStyling(unittest.TestCase):

    def test_color_negative_red(self):
        css = ff.color_negative_red(2)
        self.assertEqual(css, 'color: blue')

        css = ff.color_negative_red(0.0)
        self.assertEqual(css, 'color: blue')

        css = ff.color_negative_red(-0.0)
        self.assertEqual(css, 'color: blue')

        css = ff.color_negative_red(-42.5)
        self.assertEqual(css, 'color: red')

    def test_c_format(self):
        ff.color_negative_red



