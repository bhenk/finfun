#! /usr/bin/env python3
# -*- coding: utf-8 -*-

""" Calculating data. """
from typing import Union, Sequence

import pandas as pd
import plotly.graph_objs as go
from IPython.core.display import display
from plotly.offline import iplot
import ipywidgets as widgets

__all__ = ['ValueFrame']


class ValueFrame(object):
    """
    A date-indexed frame.

    """
    def __init__(self, dfx: Union[pd.DataFrame, Sequence[pd.DataFrame]]) -> None:
        """
        Construct a date-indexed frame.

        :param dfx: pd.DataFrame or sequence of DataFrames with a date index
        """
        self.df = pd.DataFrame()
        self.merge(dfx)

    def merge(self, dfx: Union[pd.DataFrame, Sequence[pd.DataFrame]]) -> None:
        """
        Merge the given DataFrame(s) with this frame.

        :param dfx: pd.DataFrame or sequence of DataFrames with a date index
        :return: None
        """
        if isinstance(dfx, pd.DataFrame):
            dfx = [dfx]
        for dfi in dfx:
            self.df = pd.merge(self.df, dfi.sort_index(), how='outer', left_index=True, right_index=True)

    def first_index(self, as_string: bool = True) -> Union[str, pd.Timestamp]:
        start = self.df.index[0]
        if as_string:
            return start.strftime('%Y-%m-%d')
        else:
            return start

    def last_index(self, as_string: bool = True) -> Union[str, pd.Timestamp]:
        last = self.df.index[-1:][0]
        if as_string:
            return last.strftime('%Y-%m-%d')
        else:
            return last

    def first(self) -> pd.DataFrame:
        return self.df[:self.first_index()]

    def last(self) -> pd.DataFrame:
        return self.df[self.last_index():]

    def slice(self, start: Union[str, pd.Timestamp] = None, end: Union[str, pd.Timestamp] = None) -> pd.DataFrame:
        if start is None:
            start = self.first_index(False)
        if isinstance(start, str):
            start = pd.to_datetime(start)
        if end is None:
            end = pd.Timestamp.today()
        if isinstance(end, str):
            end = pd.to_datetime(end)
        start = self.df.index[self.df.index.get_loc(start, method='nearest')]
        end = self.df.index[self.df.index.get_loc(end, method='nearest')]
        return self.df[start:end]

    def abs_daily_change(self, start: Union[str, pd.Timestamp] = None,
                         end: Union[str, pd.Timestamp] = None) -> pd.DataFrame:
        return self.slice(start, end).interpolate(method='zero', axis=0).diff()

    def rel_daily_change(self, start: Union[str, pd.Timestamp] = None,
                         end: Union[str, pd.Timestamp] = None) -> pd.DataFrame:
        dfs = self.slice(start, end).interpolate(method='zero', axis=0)
        return dfs.diff() / dfs

    def abs_change(self, start: Union[str, pd.Timestamp] = None, end: Union[str, pd.Timestamp] = None) -> pd.DataFrame:
        return self.slice(start, end).interpolate(method='zero', axis=0).diff().cumsum()

    def rel_change(self, start: Union[str, pd.Timestamp] = None, end: Union[str, pd.Timestamp] = None) -> pd.DataFrame:
        dfs = self.slice(start, end).interpolate(method='zero', axis=0)
        df_change = dfs.diff().cumsum()
        df = df_change / dfs.iloc[0]
        df.iloc[0] = 0
        return df

    def scatter_rel_change(self, start='2017-01-04', tick_format='.01%', height=700):
        df = self.rel_change(start=start)
        data = []
        for column in df.columns:
            trace = go.Scatter(
                x=df.index,
                y=df[column],
                name=column,
            )
            data.append(trace)
        layout = go.Layout(
            yaxis=dict(
                tickformat=tick_format
            ),
            height=height,
        )
        fig = go.Figure(data=data, layout=layout)
        iplot(fig)

    def display_rel_change(self, start='2017-01-04'):
        start = pd.Timestamp.today() - pd.DateOffset(days=400)
        date = widgets.DatePicker(description='Start Date', value=start)
        ui = widgets.HBox([date])
        out = widgets.interactive_output(self.scatter_rel_change, {'start': date})
        display(ui, out)
