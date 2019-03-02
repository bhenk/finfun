#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest, os, logging, sys
import warnings

import pandas as pd

import fintec as ft


class TestData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # logging:
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
        ch.setFormatter(formatter)
        root.addHandler(ch)

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

    @unittest.SkipTest
    def test_initiate_index(self):
        os.environ[ft.U_FIN_DATA_BASE] = '/Users/ecco/work/fin/beleg/data'

        self.assertEqual(ft.Idx.N225.init_file(), '/Users/ecco/work/fin/beleg/data/html/n225.html')
        self.assertEqual(ft.Idx.N225.filename(), '/Users/ecco/work/fin/beleg/data/indices/n225.csv')

        ft.initiate_index(ft.Idx.N225)
        self.assertTrue(os.path.exists(ft.Idx.N225.filename()))

        del os.environ[ft.U_FIN_DATA_BASE]
        self.assertEqual(ft.Idx.N225.filename(), 'data/indices/n225.csv')

    def test_df_index(self):
        df = ft.df_index(ft.Idx.AEX)
        self.assertIsInstance(df.index, pd.DatetimeIndex)
        self.assertListEqual(list(df.columns), ['close', 'open', 'high', 'low', 'volume', 'change'])
        self.assertEqual(0, df.close.isna().sum())
        self.assertEqual(0, df.change.isna().sum())
        self.assertEqual(0, df.volume.isna().sum())

    def test_indices(self):
        df = ft.df_indices()
        self.assertIsInstance(df.index, pd.DatetimeIndex)
        self.assertListEqual(list(df.columns), ['DOW', 'SPX', 'NDX', 'AEX', 'DAX', 'FTSE', 'SSEC', 'N225'])
        self.assertEqual(16, df.DOW.isna().sum())
        self.assertEqual(16, df.SPX.isna().sum())
        self.assertEqual(16, df.NDX.isna().sum())
        self.assertEqual(7, df.AEX.isna().sum())
        self.assertEqual(9, df.DAX.isna().sum())
        self.assertEqual(7, df.FTSE.isna().sum())
        self.assertEqual(102, df.SSEC.isna().sum())
        self.assertEqual(19, df.N225.isna().sum())
        df = ft.df_indices([ft.Idx.AEX, ft.Idx.DOW], col='high')
        self.assertIsInstance(df.index, pd.DatetimeIndex)
        self.assertListEqual(list(df.columns), ['AEX', 'DOW'])
        # print(df)
        df = ft.df_indices(ft.Idx.AEX)
        # print(df)

    # def test_df_indices_change(self):
    #     df = ft.df_indices_change(ft.Idx.NDX, start='2019-01-01')
    #     self.assertIsInstance(df.index, pd.DatetimeIndex)
    #     df = ft.df_indices(ft.Idx.NDX, start='2019-01-01')
    #     df = ft.df_index(ft.Idx.NDX).loc['2019-01-01':]
    #     #print(df)

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



