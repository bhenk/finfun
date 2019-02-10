#! /usr/bin/env python3
# -*- coding: utf-8 -*-

""" Classes and methods to do styling with pandas DataFrames and Jupyter NoteBooks. """
import pandas as pd


def color_negative_red(val):
    """
    Takes a scalar and returns a string with the css property `'color: red'` for negative
    values, `'color: blue'` for zero and positive values.
    :param val: the scalar
    :return: color css
    """
    color = 'red' if val < 0 else 'blue'
    return 'color: %s' % color


def c_format(x, decimals=0):
    """
    Returns a european style formatted string of x.
    :param x: number to format
    :param decimals: number of decimals to show
    :return: formatted string representing x
    """
    f = '{:,.' + str(decimals) + 'f}'
    return f.format(x).replace(',', 'x').replace('.', ',').replace('x', '.')


def p_format(x, decimals=2):
    """
    Returns a european formatted percentage string of x.
    :param x: number to format
    :param decimals: number of decimals to show
    :return: formatted string representing x
    """
    f = '{:,.' + str(decimals) + 'f}%'
    return f.format(x * 100).replace(',', 'x').replace('.', ',').replace('x', '.')


def currency(df, decimals=0):
    """
    Given a DataFrame with datetime index returns a DataFrame with european formatting
    and y-m-d for datetime index.
    :param df: DataFrame to convert
    :param decimals: number of decimals to show
    :return: new formatted DataFrame
    """
    return pd.DataFrame(df, index=df.index.strftime("%Y-%m-%d")).style \
        .format(lambda x: c_format(x, decimals)) \
        .applymap(color_negative_red)


def percentage(df, decimals=2):
    """
    Given a DataFrame with datetime index returns a DataFrame with european formatted percentages
    and y-m-d for datetime index
    :param df: DataFrame to convert
    :param decimals: number of decimals to show
    :return: new formatted DataFrame
    """
    return pd.DataFrame(df, index=df.index.strftime("%Y-%m-%d")).style \
        .format(lambda x: p_format(x, decimals)) \
        .applymap(color_negative_red)
