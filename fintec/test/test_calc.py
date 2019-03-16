#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import warnings

import pandas as pd

import fintec as ft


class TestValueFrame(unittest.TestCase):

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

    def test_construction_with_one(self):
        vf = ft.ValueFrame(ft.df_index(ft.Idx.DOW))
        self.assertListEqual(list(vf.df.columns), ['close', 'open', 'high', 'low', 'volume', 'change'])

    def test_construction_with_multiple(self):
        vf = ft.ValueFrame([ft.df_indices(ft.Idx.DOW), ft.df_indices(ft.Idx.AEX)])
        self.assertListEqual(list(vf.df.columns), ['DOW', 'AEX'])

    def test_first_index(self):
        vf = ft.ValueFrame(ft.df_indices([ft.Idx.AEX, ft.Idx.DOW]))
        first = vf.first_index()
        self.assertIsInstance(first, str)
        self.assertEqual('2019-01-02', first)

        first = vf.first_index(as_string=False)
        self.assertIsInstance(first, pd.Timestamp)

    def test_last_index(self):
        vf = ft.ValueFrame(ft.df_indices([ft.Idx.AEX, ft.Idx.DOW]))
        last = vf.last_index()
        self.assertIsInstance(last, str)
        self.assertEqual('2019-03-01', last)

        last = vf.last_index(as_string=False)
        self.assertIsInstance(last, pd.Timestamp)
        # print(vf.df[last:])

    def test_first(self):
        vf = ft.ValueFrame(ft.df_indices([ft.Idx.AEX, ft.Idx.DOW]))
        self.assertIsInstance(vf.first(), pd.DataFrame)
        # print(vf.first())

    def test_last(self):
        vf = ft.ValueFrame(ft.df_indices([ft.Idx.AEX, ft.Idx.DOW]))
        self.assertIsInstance(vf.last(), pd.DataFrame)
        #print(vf.last())

    def test_abs_daily_change(self):
        vf = ft.ValueFrame(ft.df_indices([ft.Idx.AEX, ft.Idx.DOW]))
        df = vf.abs_daily_change()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(0, df.DOW['2019-01-21'])
        # print(df)

        df = vf.abs_daily_change(start='2019-02-28', end='2020-01-31')
        # print(df)

    def test_rel_daily_change(self):
        vf = ft.ValueFrame(ft.df_indices([ft.Idx.AEX, ft.Idx.DOW]))
        df = vf.rel_daily_change()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(0, df.DOW['2019-01-21'])
        # print(df)

    def test_abs_change(self):
        vf = ft.ValueFrame(ft.df_indices([ft.Idx.AEX, ft.Idx.DOW]))
        df = vf.abs_change()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.DOW['2019-01-18'], df.DOW['2019-01-21'])
        # print(df)

    def test_rel_change(self):
        vf = ft.ValueFrame(ft.df_indices([ft.Idx.AEX, ft.Idx.DOW]))
        df = vf.rel_change()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.DOW['2019-01-18'], df.DOW['2019-01-21'])
        # print(df)

    def test_scatter_rel_change(self):
        vf = ft.ValueFrame(ft.df_indices([ft.Idx.AEX, ft.Idx.DOW]))
        vf.scatter_rel_change()
