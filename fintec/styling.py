#! /usr/bin/env python3
# -*- coding: utf-8 -*-

""" Classes and methods to do styling with pandas DataFrames on Jupyter NoteBooks. """
import csv
import datetime
import os
from logging.handlers import RotatingFileHandler
from io import StringIO
import pandas as pd
import logging, sys

__all__ = ['color_negative_red', 'c_format', 'p_format', 'currency', 'percentage',
           'start_logging', 'end_logging', 'initiate_file_logging', 'log']

_log = logging.getLogger(__name__)
__LOG_CHANNEL__ = logging.StreamHandler(sys.stdout)


def start_logging(level=logging.DEBUG):
    """
    Start logging log messages to stdout.
    :param level: log level
    :return: None
    """
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
    __LOG_CHANNEL__.setFormatter(formatter)
    __LOG_CHANNEL__.setLevel(level)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(__LOG_CHANNEL__)


def end_logging():
    """
    Stop logging log messages to stdout.
    :return: None
    """
    root = logging.getLogger()
    root.removeHandler(__LOG_CHANNEL__)


def log(func, *args, **kwargs):
    """
    Wrapper for functions that want to be logged to stdout. After the function returns, logging is turned of again.
    :param func: the function to call
    :param args: arguments for the function
    :param kwargs: named arguments for the function
    :return: the return value of the function
    """
    start_logging()
    try:
        ret_val = func(*args, **kwargs)
    finally:
        end_logging()
    return ret_val


class CsvFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.output = StringIO()
        self.writer = csv.writer(self.output, quoting=csv.QUOTE_ALL)

    def format(self, record):
        time = datetime.datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S.%f')
        self.writer.writerow([time, record.threadName, record.process, record.levelname, record.filename,
                              record.lineno, record.funcName, record.msg, record.pathname])
        data = self.output.getvalue()
        self.output.truncate(0)
        self.output.seek(0)
        return data.strip()


def initiate_file_logging(log_file='logs/fintec.log', level=logging.DEBUG, max_bytes=1000 * 1000 * 1024,
                          backup_count=3, encoding='utf-8'):
    """
    Initiate logging to a rotating file. If needed, the log file output can be picked up in a DataFrame:
    ```
    names = ['date', 'thread', 'process', 'level', 'file', 'line', 'function', 'msg', 'path']
    df = pd.read_csv('logs/fintec.log', header=None, quoting=1, converters={0: pd.to_datetime}, names=names)
    ```

    :param log_file: the path or file to write to. Directories will be created.
    :param level: the log level. one of logging levels
                logging.DEBUG (10), logging.INFO (20), logging.WARNING (30), logging.ERROR (40), logging.CRITICAL (50)
    :param max_bytes: max bytes for roll over
    :param backup_count: how many files are kept
    :param encoding: encoding of the file
    :return: None
    """
    path = os.path.dirname(log_file)
    os.makedirs(path, exist_ok=True)
    log_channel = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count, encoding=encoding)
    log_channel.setFormatter(CsvFormatter())
    log_channel.setLevel(level)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(log_channel)
    _log.debug('Initiated file logging to {}'.format(log_file))


def color_negative_red(val) -> str:
    """
    Takes a scalar and returns a string with the css property `'color: red'` for negative
    values, `'color: blue'` for zero and positive values.
    :param val: the scalar
    :return: color css
    """
    color = 'red' if val < 0 else 'blue'
    return 'color: {}'.format(color)


def _eu_format(number_string: str) -> str:
    return number_string.replace(',', 'x').replace('.', ',').replace('x', '.')


def c_format(x, decimals=0) -> str:
    """
    Returns a european style formatted string of x.
    :param x: number to format
    :param decimals: number of decimals to show
    :return: formatted string representing x
    """
    f = '{{:,.{0}f}}'.format(decimals)
    return _eu_format(f.format(x))


def p_format(x, decimals=2) -> str:
    """
    Returns a european formatted percentage string of x.
    :param x: number to format
    :param decimals: number of decimals to show
    :return: formatted string representing x
    """
    f = '{{:,.{0}f}}%'.format(decimals)
    return _eu_format(f.format(x * 100))


def currency(df: pd.DataFrame, decimals=0):
    """
    Given a DataFrame with datetime index returns a pandas.io.formats.style.Styler object
    with european formatting and y-m-d for datetime index.
    :param df: DataFrame to convert
    :param decimals: number of decimals to show
    :return: new formatted DataFrame
    """
    return pd.DataFrame(df, index=df.index.strftime("%Y-%m-%d")).style \
        .format(lambda x: c_format(x, decimals)) \
        .applymap(color_negative_red)


def percentage(df: pd.DataFrame, decimals=2):
    """
    Given a DataFrame with datetime index returns a pandas.io.formats.style.Styler object
    with european formatted percentages and y-m-d for datetime index.
    :param df: DataFrame to convert
    :param decimals: number of decimals to show
    :return: new formatted DataFrame
    """
    return pd.DataFrame(df, index=df.index.strftime("%Y-%m-%d")).style \
        .format(lambda x: p_format(x, decimals)) \
        .applymap(color_negative_red)
