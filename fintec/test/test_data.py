#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import warnings

import pandas as pd

import fintec as ft


class TestData(unittest.TestCase):

    def setUp(self):
        warnings.filterwarnings('ignore', category=PendingDeprecationWarning)
        warnings.filterwarnings('ignore', category=ImportWarning)

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

