#!/usr/bin/env python3
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go
from enum import Enum, auto


class PlotType(Enum):
    CandleStick = auto()
    Closed = auto()
    Opened = auto()
    High = auto()
    Low = auto()
    Volume = auto()

class Plotter:
    def __init__(self):
        self.df = pd.read_parquet("sp500.zstd.parquet")
    
    def plot_stock(self, stock_name: str, plot_type: PlotType, /, *, days_ago: int = 365, file_path: str | None = None) -> None:
        stock_info = self.df.loc[2 :, self.df.iloc[0] == stock_name]
        dates = self.df['Price'][2:][-days_ago - 1 : -1]
        try:
            if plot_type in {PlotType.CandleStick, PlotType.Closed}:
                closed_prices = stock_info.iloc[:, 0][-days_ago - 1 : -1]
            if plot_type in {PlotType.CandleStick, PlotType.High}:
                high_price = stock_info.iloc[:, 1][-days_ago - 1 : -1]
            if plot_type in {PlotType.CandleStick, PlotType.Low}:
                low_price = stock_info.iloc[:, 2][-days_ago - 1 : -1]
            if plot_type in {PlotType.CandleStick, PlotType.Opened}:
                open_price = stock_info.iloc[:, 3][-days_ago - 1 : -1]
            if plot_type == PlotType.Volume:
                volume = stock_info.iloc[:, 4][-days_ago - 1 : -1].astype('UInt32')
        except IndexError as e:
            raise Exception(f"Bad stock name {repr(stock_name)}") from e

        # This could be simplified but i could just copy paste everything so idc lol
        match plot_type:
            case PlotType.CandleStick:
                fig = go.Figure(data=[go.Candlestick(
                    x=dates,
                    open=open_price,
                    high=high_price,
                    low=low_price,
                    close=closed_prices
                )]).update_layout(
                    title=f"S&P 500: {stock_name}",
                    xaxis={'title' : 'Date'},
                    yaxis={'title' : 'Price in dollar'}
                )
            case PlotType.Volume:
                fig = px.bar(x=dates, y=volume, labels={
                    'x' : 'Date',
                    'y' : 'Volume',
                    'title' : f'S&P 500: {stock_name}'
                })
            case PlotType.Closed:
                fig = px.line(x=dates, y=closed_prices.astype('float'), labels={
                    'x' : 'Date',
                    'y' : 'Closed Price',
                    'title' : f'S&P 500: {stock_name}'
                })
            case PlotType.Opened:
                fig = px.line(x=dates, y=open_price.astype('float'), labels={
                    'x' : 'Date',
                    'y' : 'Opened Price',
                    'title' : f'S&P 500: {stock_name}'
                })
            case PlotType.High:
                fig = px.line(x=dates, y=high_price.astype('float'), labels={
                    'x' : 'Date',
                    'y' : 'High Price',
                    'title' : f'S&P 500: {stock_name}'
                })
            case PlotType.Low:
                fig = px.line(x=dates, y=low_price.astype('float'), labels={
                    'x' : 'Date',
                    'y' : 'Low Price',
                    'title' : f'S&P 500: {stock_name}'
                })

        file_path = file_path or f"{stock_name}-{days_ago}-{plot_type.name}.png"
        fig.write_image(file_path)
        

if __name__ == '__main__':
    plotter = Plotter()
    plotter.plot_stock('NVDA', PlotType.CandleStick, days_ago=30)
