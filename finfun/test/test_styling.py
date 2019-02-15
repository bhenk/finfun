#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import finfun as ff
import unittest
import pandas as pd


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
        s = ff.c_format(42, 3)
        self.assertEqual('42,000', s)

    def test_p_format(self):
        p = ff.p_format(0.06234)
        self.assertEqual('6,23%', p)

    def test_currency(self):
        df = pd.DataFrame(index=[pd.to_datetime('2019/02/10')], data={'A': [1.2]})
        dfc = ff.currency(df)
        print(dfc)

