#! /usr/bin/env python3
# -*- coding: utf-8 -*-

""" Calculating the data. """
import pandas as pd
import numpy as np
from typing import Union, Sequence, Iterable

START_DATE = '2017-01-01'

__all__ = ['ValueFrame']


class ValueFrame(object):

    def __init__(self, dfx: Union[pd.DataFrame, Sequence[pd.DataFrame]] = None):
        self.df = pd.DataFrame()
        self.merge(dfx)

    def merge(self, dfx: Union[pd.DataFrame, Sequence[pd.DataFrame]] = None):
        if dfx is not None:
            if isinstance(dfx, pd.DataFrame):
                dfx = [dfx]
            for dfi in dfx:
                self.df = pd.merge(self.df, dfi, how='outer', left_index=True, right_index=True)

    def first_index(self, as_string: bool = True):
        if len(self.df.index) == 0:
            return np.nan
        start = self.df.index[0]
        if as_string:
            return start.strftime('%Y-%m-%d')
        else:
            return start

    def last_index(self, as_string: bool = True):
        if len(self.df.index) == 0:
            return np.nan
        last = self.df.index[-1:][0]
        if as_string:
            return last.strftime('%Y-%m-%d')
        else:
            return last

    def first(self):
        if len(self.df.index) == 0:
            return np.nan
        return self.df[:self.first_index()]

    def last(self):
        if len(self.df.index) == 0:
            return np.nan
        return self.df[self.last_index():]

    def abs_change(self, start: Union[str, pd.Timestamp] = START_DATE, end: Union[str, pd.Timestamp] = None):
        if len(self.df) == 0:
            return self.df
        if end is None:
            end = pd.Timestamp.today()
        if isinstance(end, str):
            end = pd.to_datetime(end)
        if isinstance(start, str):
            start = pd.to_datetime(start)
        start = self.df.index[self.df.index.get_loc(start, method='nearest')]
        end = self.df.index[self.df.index.get_loc(end, method='nearest')]
        return self.df[start:end].interpolate(method='zero', axis=0).diff()
