#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Classes and methods to do styling with pandas DataFrames and Jupyter NoteBooks.
"""


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
