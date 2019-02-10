#! /usr/bin/env python3
# -*- coding: utf-8 -*-


def color_negative_red(val):
    """
    Takes a scalar and returns a string with the css property `'color: red'` for negative
    strings, blue otherwise.
    :param val: the scalar
    :return: color css
    """
    color = 'red' if val < 0 else 'blue'
    return 'color: %s' % color
