#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import fintec as ft
import unittest
import os
import pandas as pd

import warnings


class TestData(unittest.TestCase):

    def setUp(self):
        warnings.filterwarnings('ignore', category=PendingDeprecationWarning)
        warnings.filterwarnings('ignore', category=ImportWarning)

    def test_data_path(self):
        self.assertEqual(ft.data_path('foo.txt'), 'data/foo.txt')
        os.environ[ft.U_FIN_DATA_BASE] = 'test-data'
        self.assertEqual(ft.data_path('foo.txt'), 'test-data/foo.txt')
        del os.environ[ft.U_FIN_DATA_BASE]
        self.assertEqual(ft.data_path('foo.txt'), 'data/foo.txt')

    def test_read_data(self):
        df = ft.read_data('fondsen.xlsx')
        self.assertListEqual(list(df.columns), ['msuaf', 'nngf', 'nnitf', 'rgfte', 'smwtf'])

        df = ft.read_data('rates.csv')
        self.assertListEqual(list(df.columns), ['msuaf', 'nngf', 'nnitf', 'rgfte', 'smwtf'])

    def test_read_data_with_str_index(self):
        df = ft.read_data('fondsen.xlsx', index_col='msuaf')
        self.assertIsInstance(df.index, pd.Float64Index)

        df = ft.read_data('rates.csv', index_col='msuaf')
        self.assertIsInstance(df.index, pd.Float64Index)

    def test_read_data_with_seq_index(self):
        df = ft.read_data('fondsen.xlsx', index_col=[0, 3])
        self.assertIsInstance(df.index, pd.MultiIndex)

        df = ft.read_data('rates.csv', index_col=[0, 3])
        self.assertIsInstance(df.index, pd.MultiIndex)

    def test_read_data_with_no_index(self):
        df = ft.read_data('fondsen.xlsx', index_col=None)
        self.assertIsInstance(df.index, pd.RangeIndex)

        df = ft.read_data('rates.csv', index_col=False)
        self.assertIsInstance(df.index, pd.RangeIndex)

    def test_df_rates(self):
        df = ft.df_rates()
        self.assertIsInstance(df.index, pd.DatetimeIndex)
        self.assertListEqual(list(df.columns), ['msuaf', 'nngf', 'nnitf', 'rgfte', 'smwtf'])
        self.assertEqual(5, df.msuaf.isna().sum())
        self.assertEqual(3, df.rgfte.isna().sum())

    def test_df_rates_from_csv(self):
        df = ft.df_rates('rates.csv')
        self.assertIsInstance(df.index, pd.DatetimeIndex)
        self.assertListEqual(list(df.columns), ['msuaf', 'nngf', 'nnitf', 'rgfte', 'smwtf'])
        self.assertEqual(2, df.msuaf.isna().sum())
        self.assertEqual(3, df.rgfte.isna().sum())

