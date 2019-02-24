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

    @unittest.SkipTest
    def test_update_index(self):
        df = ft.update_index(ft.Idx.AEX)
        self.assertIsInstance(df.index, pd.DatetimeIndex)
        self.assertListEqual(list(df.columns), ['Price', 'Open', 'High', 'Low', 'Vol.', 'Change %'])
        self.assertTrue((pd.datetime.now() - df.index.max()).days < 4)


class TestIdx(unittest.TestCase):

    def test_for_name(self):
        idx = ft.Idx.for_name('aex')
        self.assertEqual(ft.Idx.AEX, idx)

    def test_for_name_with_invalid_para(self):
        with warnings.catch_warnings(record=True) as w:
            idx = ft.Idx.for_name('not a name')
        self.assertTrue(len(w) == 1)
        self.assertEqual(str(w.pop(0).message), 'No Idx with name "NOT A NAME"')
        self.assertIsNone(idx)



