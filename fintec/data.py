#! /usr/bin/env python3
# -*- coding: utf-8 -*-

""" Gathering and manipulating data. """
import enum
import logging
import os
import warnings
from enum import Enum
from typing import Union, Sequence, Iterable

import pandas as pd
import numpy as np
import requests

from fintec import styling

__all__ = ['U_FIN_DATA_BASE',
           'df_rates',
           'Idx', 'update_index', 'update_indices', 'initiate_index', 'initiate_indices',
           'df_index', 'df_indices', 'df_indices_change']


_log = logging.getLogger(__name__)
_STRINT = Union[str, int]
_IDXCOL = Union[_STRINT, Sequence[int], None]

U_FIN_DATA_BASE = 'U_FIN_DATA_BASE'
""" The environment variable name for the data base directory. """


def _all_date_range(start_date: str = '2018-01-01') -> pd.date_range:
    """
    Return a date range starting at start_date and ending now inclusive, with frequency Day.
    :param start_date: start date of range
    :return: pd.date_range
    """
    return pd.date_range(start_date, periods=(pd.Timestamp.today() - pd.to_datetime(start_date)).days + 1, freq='D',
                         name='Date')


def _data_path(filename: str) -> str:
    """
    Get the path to file f, relative to the environment variable 'U_FIN_DATA_BASE'.
    If the environment variable is not found uses 'data' as default.

    :param filename: the filename or path to append to the data base path.
    :return: complete path to the data base file.
    """
    return os.path.join(os.getenv(U_FIN_DATA_BASE, 'data'), filename)


def _read_data(filename: str, index_col: _IDXCOL = 0, sheet_name: _STRINT = 0, converters=None):
    """
    Read in a DataFrame, either from a csv file or an Excel file.

    :param filename: file to read
    :param index_col: int, str or sequence or False or None, default 0
    :param sheet_name: if it is an Excel file, the name or index number of the sheet, default 0
    :param converters: dict, default None
                    Dict of functions for converting values in certain columns. Keys can either
                    be integers or column labels
    :return: pandas.DataFrame
    """
    if os.path.splitext(filename)[1].lower() == '.csv':
        # _log.debug('Reading csv data. filename={}'.format(filename))
        df = pd.read_csv(filename, index_col=index_col, converters=converters)
    else:
        # _log.debug('Reading excel data. filename={}'.format(filename))
        df = pd.read_excel(filename, sheet_name=sheet_name, index_col=index_col, converters=converters)
    return df


def _read_date_indexed_data(filename: str, index_col: _IDXCOL = 0, sheet_name: _STRINT = 0, converters=None):
    """
    Read data with a datetime index, interpolate nearest.

    :param filename: file to read
    :param index_col: int, str or sequence or False or None, default 0
    :param sheet_name: if it is an Excel file, the name or index number of the sheet, default 0
    :param converters: dict, default None
                    Dict of functions for converting values in certain columns. Keys can either
                    be integers or column labels
    :return: pandas.DataFrame
    """
    df = _read_data(filename, index_col, sheet_name, converters=converters)
    df.index = pd.to_datetime(df.index)
    df = df.interpolate(method='nearest', axis=0).sort_index()
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
    _log.debug('Reading rates. filename={}, index_col={}, sheet_name={}'.format(filename, index_col, sheet_name))
    return _read_date_indexed_data(_data_path(filename), index_col, sheet_name)


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
    STOXX = ('STOXX 600', 'stoxx-600')
    SSEC = ('Shanghai Composite', 'shanghai-composite')
    N225 = ('Nikkei 225', 'japan-ni225')

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
        return _data_path('html/{}.html'.format(self.name.lower()))

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


def update_index(idx: Idx, table_index: int = 1) -> pd.DataFrame:
    """
    Update the given index.

    :param idx: index to update
    :param table_index: index number of the table to read from html
    :return: DataFrame with ohlc
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(idx.ic_historical_data_url(), headers=headers)
    if response.status_code != 200:
        raise Exception('Unexpected response status: {}'.format(response.status_code))
    # old index
    dfo = _read_date_indexed_data(idx.filename())
    # new index
    dfn = pd.read_html(response.text, index_col=0)[table_index]
    dfn.index = pd.to_datetime(dfn.index)
    dfn = dfn.sort_index()
    # concat on last day
    lastday = dfn.index[0] + pd.DateOffset(days=-1)
    dfi = pd.concat([dfo[:lastday], dfn], join='inner')
    dfi.to_csv(idx.filename())
    _log.debug('Updated {}'.format(idx.describe()))
    return dfi


def update_indices(indices: Union[iter, Idx] = Idx, table_index: int = 1):
    """
    Update indices.

    :param indices: indices to update. Default Idx
    :param days_back: backward synchronizing, number of days back
    :param table_index: index number of the table to read from html
    :return: None
    """
    _log.debug('Updating indices')
    if not isinstance(indices, Iterable):
        indices = [indices]
    for idx in indices:
        update_index(idx, table_index)


def initiate_index(idx: Idx, table_index: int = 0, log: bool = True) -> pd.DataFrame:
    """
    Initiate the given index. Assumes html has been saved manually at idx.init_file().
    :param idx: the index to initiate
    :param table_index: index number of the table to read from html
    :param log: print logging to std.out, default True
    :return: DataFrame with ohlc
    """
    if log: styling.start_logging()
    if os.path.exists(idx.filename()):
        _log.info('Not initiating {}. File \'{}\' exists'.format(idx, idx.filename()))
        dfi = pd.read_csv(idx.filename(), index_col=0)
        dfi.index = pd.to_datetime(dfi.index)
        dfi = dfi.sort_index()
    elif os.path.exists(idx.init_file()):
        _log.info('Initiating index from {}'.format(idx.init_file()))
        dfs = pd.read_html(idx.init_file(), index_col=0)
        dfi = dfs[table_index]
        dfi.index = pd.to_datetime(dfi.index)
        dfi = dfi.sort_index()
        dfi.to_csv(idx.filename())
        _log.info('Initiated index {}'.format(idx.filename()))
    else:
        msg = 'Not initiating {}. Initial file not found: {}'.format(idx, idx.init_file())
        _log.warning(msg)
        warnings.warn(msg)
        dfi = None
    if log: styling.end_logging()
    return dfi


def initiate_indices(indices: Union[iter, Idx] = Idx, table_index: int = 0):
    """
    Initiate the given indices. Assumes html pages have been saved manually at idx.init_file().
    :param indices: the indices to initiate
    :param table_index: index number of the table to read from html
    :return: None
    """
    _log.debug('Updating indices')
    if not isinstance(indices, Iterable):
        indices = [indices]
    for idx in indices:
        initiate_index(idx, table_index=table_index)


def __convert_volume__(v: str) -> float:
    """
    Convert cell content from the column 'Vol.' from investing.com/indices data.
    :param v: the string value of the cell data
    :return: the number value for the cell data
    """
    if v[-1] == 'K':
        return float(v[:-1]) * 1000
    elif v[-1] == 'M':
        return float(v[:-1]) * 1000000
    elif v[-1] == 'B':
        return float(v[:-1]) * 1000000000
    elif v == '-':
        return np.nan
    else:
        return float(v)


def __convert_change__(c: str) -> float:
    """
    Convert cell content from the column 'Change %' from investing.com/indices data.
    :param c: the string value of the cell data
    :return: the number value for the cell data
    """
    if c[-1] == '%':
        return float(c[:-1]) / 100
    else:
        return np.nan


def df_index(idx: Idx) -> pd.DataFrame:
    """
    Read the index table indicated by idx. Fills NaN's, except leading and trailing.

    :param idx: index table to read
    :return: DataFrame with date index, ohlc, volume and change percentage
    """
    _log.debug('Reading index {}'.format(idx.filename()))
    converters = {'Vol.': __convert_volume__, 'Change %': __convert_change__}
    return _read_date_indexed_data(idx.filename(), converters=converters) \
        .rename(columns={'Price': 'close', 'Vol.': 'volume', 'Change %': 'change'}) \
        .rename(columns=np.unicode.lower)


def df_indices(indices: Union[iter, Idx] = Idx, col: str = 'close', start: str = '2018-01-01') -> pd.DataFrame:
    """
    Returns a dataframe with the columns named col from indices.

    :param indices: iterable of indices, default Idx
    :param col: which column should be merged in the final frame.
            one of ['close', 'open', 'high', 'low', 'volume', 'change']
    :param start start date
    :return: DataFrame with date index, indices represented with column named by col
    """
    _log.debug('Merging column \'{}\' of indices.'.format(col))
    if not isinstance(indices, Iterable):
        indices = [indices]
    dfm = None
    for idx in indices:
        df = df_index(idx).rename(columns={col: idx.name})
        if dfm is None:
            dfm = df[[idx.name]]
        else:
            dfm = pd.merge(dfm, df[[idx.name]], how='outer', left_index=True, right_index=True)

    dt = pd.to_datetime(start)
    dti = dfm.index[dfm.index.get_loc(dt, method='nearest')]
    strt = '{0:%Y-%m-%d}'.format(dti)
    return dfm.loc[strt:]


def df_indices_change(indices: Union[iter, Idx] = Idx, col: str = 'close', start: str = '2018-01-01'):

    dfm = df_indices(indices, col)
    dfa = pd.merge(pd.DataFrame(index=_all_date_range()), dfm, left_index=True, right_index=True, how='outer') \
        .interpolate(method='zero', axis=0)
    dt = pd.to_datetime(start)
    dti = dfa.index[dfa.index.get_loc(dt, method='nearest')]
    strt = '{0:%Y-%m-%d}'.format(dti)
    df_change = dfa.loc[strt:].diff()
    return df_change

