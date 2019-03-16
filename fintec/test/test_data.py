#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest, os, logging, sys
import warnings

import pandas as pd

import fintec as ft


class TestData(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     # logging:
    #     root = logging.getLogger()
    #     root.setLevel(logging.DEBUG)
    #     ch = logging.StreamHandler(sys.stdout)
    #     ch.setLevel(logging.DEBUG)
    #     formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
    #     ch.setFormatter(formatter)
    #     root.addHandler(ch)

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

    def test_initiate_index(self):
        ft.initiate_index(ft.Idx.N225)
        self.assertFalse(os.path.exists(ft.Idx.N225.filename()))

    def test_df_index(self):
        df = ft.df_index(ft.Idx.AEX)
        self.assertIsInstance(df.index, pd.DatetimeIndex)
        self.assertListEqual(list(df.columns), ['close', 'open', 'high', 'low', 'volume', 'change'])
        self.assertEqual(0, df.close.isna().sum())
        self.assertEqual(0, df.change.isna().sum())
        self.assertEqual(0, df.volume.isna().sum())

    def test_indices(self):
        df = ft.df_indices([ft.Idx.AEX, ft.Idx.DOW], col='high')
        self.assertIsInstance(df.index, pd.DatetimeIndex)
        self.assertListEqual(list(df.columns), ['AEX', 'DOW'])
        # print(df)

    @unittest.SkipTest
    def test_logging_indices(self):
        ft.debug(ft.df_indices, [ft.Idx.AEX, ft.Idx.DOW], col='high')
        print('\nstop logging level debug')
        df = ft.info(ft.df_indices, [ft.Idx.AEX, ft.Idx.DOW], col='high')
        print()
        print(df.tail())
        print('no more logging')
        ft.df_indices([ft.Idx.AEX, ft.Idx.DOW])
        print('end of function')

    def test_display_update_indices(self):
        ft.display_update_indices()


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



