#! /usr/bin/env python3
# -*- coding: utf-8 -*-

""" Gathering and manipulating data. """
import pandas as pd
import os

U_FIN_DATA_BASE = 'U_FIN_DATA_BASE'
""" The environment variable name for the data base directory. """


def data_path(filename: str) -> str:
    """
    Get the path to file f, relative to the environment variable 'U_FIN_DATA_BASE'.
    If the environment variable is not found uses 'data' as default.
    :param filename: the filename or path to append to the data base path.
    :return: complete path to the data base file.
    """
    return os.path.join(os.getenv(U_FIN_DATA_BASE, 'data'), filename)


def df_koersen(filename='fondsen.xlsx', sheet_name='koersen', index_col=0) -> pd.DataFrame:
    """
    Read Excel file filename relative to data_path, sheet 'sheet_name'. The index_col should be of type date.
    Fills NaN's, except leading and trailing.
    :return: DataFrame with dates and rates, NaN's interpolated to nearest.
    """
    df = pd.read_excel(data_path(filename), sheet_name=sheet_name, index_col=index_col) \
        .interpolate(method='nearest', axis=0)
    df[index_col] = pd.to_datetime(df[index_col])
    return df
