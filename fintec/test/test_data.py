#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import fintec as ff
import unittest
import os
import pandas as pd


class TestData(unittest.TestCase):

    def test_data_path(self):
        self.assertEqual(ff.data_path('foo.txt'), 'data/foo.txt')
        os.environ[ff.U_FIN_DATA_BASE] = 'test-data'
        self.assertEqual(ff.data_path('foo.txt'), 'test-data/foo.txt')
        del os.environ[ff.U_FIN_DATA_BASE]
        self.assertEqual(ff.data_path('foo.txt'), 'data/foo.txt')

    def test_df_koersen(self):
        df = ff.df_koersen()
        self.assertIsInstance(pd.DatetimeIndex, df.index)

