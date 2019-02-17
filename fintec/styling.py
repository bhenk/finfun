#! /usr/bin/env python3
# -*- coding: utf-8 -*-

""" Classes and methods to do styling with pandas DataFrames on Jupyter NoteBooks. """
import pandas as pd

__all__ = ['color_negative_red', 'c_format', 'p_format', 'currency', 'percentage']

def color_negative_red(val) -> str:
    """
    Takes a scalar and returns a string with the css property `'color: red'` for negative
    values, `'color: blue'` for zero and positive values.
    :param val: the scalar
    :return: color css
    """
    color = 'red' if val < 0 else 'blue'
    return 'color: {}'.format(color)


def eu_format(number_string: str) -> str:
    return number_string.replace(',', 'x').replace('.', ',').replace('x', '.')


def c_format(x, decimals=0) -> str:
    """
    Returns a european style formatted string of x.
    :param x: number to format
    :param decimals: number of decimals to show
    :return: formatted string representing x
    """
    f = '{{:,.{0}f}}'.format(decimals)
    return eu_format(f.format(x))


def p_format(x, decimals=2) -> str:
    """
    Returns a european formatted percentage string of x.
    :param x: number to format
    :param decimals: number of decimals to show
    :return: formatted string representing x
    """
    f = '{{:,.{0}f}}%'.format(decimals)
    return eu_format(f.format(x * 100))


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
