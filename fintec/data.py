#! /usr/bin/env python3
# -*- coding: utf-8 -*-

""" Gathering and manipulating data. """
import os
import warnings
from enum import Enum
from typing import Union, Sequence

import pandas as pd
import requests

__all__ = ['U_FIN_DATA_BASE',
           'df_rates',
           'Idx', 'update_index', 'update_indices']

_STRINT = Union[str, int]
_IDXCOL = Union[_STRINT, Sequence[int], None]

U_FIN_DATA_BASE = 'U_FIN_DATA_BASE'
""" The environment variable name for the data base directory. """


def _data_path(filename: str) -> str:
    """
    Get the path to file f, relative to the environment variable 'U_FIN_DATA_BASE'.
    If the environment variable is not found uses 'data' as default.

    :param filename: the filename or path to append to the data base path.
    :return: complete path to the data base file.
    """
    return os.path.join(os.getenv(U_FIN_DATA_BASE, 'data'), filename)


def _read_data(filename: str, index_col: _IDXCOL = 0, sheet_name: _STRINT = 0):
    """
    Read in a DataFrame, either from a csv file or an Excel file.

    :param filename: file to read
    :param index_col: int, str or sequence or False or None, default 0
    :param sheet_name: if it is an Excel file, the name or index number of the sheet, default 0
    :return: pandas.DataFrame
    """
    if os.path.splitext(filename)[1].lower() == '.csv':
        df = pd.read_csv(_data_path(filename), index_col=index_col)
    else:
        df = pd.read_excel(_data_path(filename), sheet_name=sheet_name, index_col=index_col)
    return df


def _read_date_indexed_data(filename: str, index_col: _IDXCOL = 0, sheet_name: _STRINT = 0):
    """
    Read data with a datetime index, interpolate nearest.

    :param filename: file to read
    :param index_col: int, str or sequence or False or None, default 0
    :param sheet_name: if it is an Excel file, the name or index number of the sheet, default 0
    :return: pandas.DataFrame
    """
    df = _read_data(filename, index_col, sheet_name)
    df.index = pd.to_datetime(df.index)
    df = df.interpolate(method='nearest', axis=0)
    return df


def df_rates(filename='fondsen.xlsx', index_col: _IDXCOL = 0, sheet_name: _STRINT = 'koersen') -> pd.DataFrame:
    """
    Read file filename relative to data_path, sheet 'sheet_name'. The index_col should be of type date.
    Fills NaN's, except leading and trailing. The type of file and how it is read is determined
    by the file extension, either .csv or .xlsx.

    :param filename: file to read
    :param index_col: int, str or sequence or False or None, default 0
    :param sheet_name: if it is an Excel file, the name or index number of the sheet, default 'koersen'
    :return: pandas.DataFrame
    """
    return _read_date_indexed_data(filename, index_col, sheet_name)


class Idx(Enum):
    """
    Enumeration of indices.
    """
    DOW = ('Dow Jones Industrial Average (DJI)', 'us-30')
    SPX = ('Standard & Poor\'s 500 ', 'us-spx-500')
    NDX = ('National Association of Securities Dealers Automated Quotations', 'nq-100')
    AEX = ('Amsterdam Exchange Index', 'netherlands-25')
    DAX = ('Deutscher Aktienindex', 'germany-30')
    FTSE = ('Financial Times Stock Exchange Index', 'uk-100')
    SSEC = ('Shanghai Composite', 'shanghai-composite')

    def __init__(self, long_name: str, ic_name: str):
        self.long_name = long_name
        self.ic_name = ic_name

    def describe(self) -> (str, str):
        return self.name, self.value

    def long_name(self) -> str:
        return self.long_name

    def filename(self) -> str:
        """
        Local filename of the index.
        :return: filename of the index
        """
        return _data_path('indices/{}.csv'.format(self.name.lower()))

    def ic_historical_data_url(self) -> str:
        """
        URL of the index history.
        :return: URL of the index history
        """
        return 'https://www.investing.com/indices/{}-historical-data'.format(self.ic_name)

    def init_file(self) -> str:
        """
        Local filename of the initial file as downloaded manually.
        :return: filename of the initial file
        """
        return 'html/{}.html'.format(self.name.lower())

    @classmethod
    def for_name(cls, name: str):
        """
        Gives the Idx for the given name or None if given name is not an Idx.
        :param name: name (case insensitive) of the Idx
        :return: Idx or None if name is not an Idx
        """
        nu = name.upper()
        if nu in cls.__members__:
            return cls.__members__[nu]
        else:
            warnings.warn('No {} with name "{}"'.format(cls.__name__, nu))
        return None


def update_index(idx: Idx, days_back: int=20) -> pd.DataFrame:
    """
    Update the given index. The maximum number of days back depends on the data table on the source site.

    :param idx: index to update
    :param days_back: backward synchronizing, number of days back
    :return: DataFrame with ohlc
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(idx.ic_historical_data_url(), headers=headers)
    if response.status_code != 200:
        raise Exception('Unexpected response status: {}'.format(response.status_code))
    # old index
    dfo = pd.read_csv(idx.filename(), index_col=0)
    dfo.index = pd.to_datetime(dfo.index)
    dfo = dfo.sort_index()
    # new index
    df_tables = pd.read_html(response.text, index_col=0)
    dfn = df_tables[1]
    dfn.index = pd.to_datetime(dfn.index)
    dfn = dfn.sort_index()
    # concat on last day
    index = dfo.index[-days_back:][0]
    dfi = pd.concat([dfo[:-days_back], dfn[index :]], join='inner')
    dfi.to_csv(idx.filename())
    print('Updated {}'.format(idx.describe()))
    return dfi


def update_indices(days_back=20):
    """
    Update all indices.
    :param days_back: backward synchronizing, number of days back
    :return: None
    """
    for idx in Idx:
        update_index(idx, days_back)


def initiate_index(idx: Idx) -> pd.DataFrame:
    """
    Initiate the given index. Assumes html has been saved manually at idx.init_file().
    :param idx: the index to initiate
    :return: DataFrame with ohlc
    """
    dfs = pd.read_html(idx.init_file(), index_col=0)
    dfi = dfs[0]
    dfi.index = pd.to_datetime(dfi.index)
    dfi = dfi.sort_index()
    dfi.to_csv(idx.filename())
    return dfi
