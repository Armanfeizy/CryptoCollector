import numpy as np
import pandas as pd
import mplfinance as mpf
import seaborn as sns
from matplotlib import pyplot as plt

from candlestick.chart import Chart


def plot_price_heatmap(chart: Chart, symbol: str, num_buckets: int = 20):

    all_prices = [price for candle in chart.candles for price in [candle.low, candle.high]]

    min_price, max_price = min(all_prices), max(all_prices)

    bucket_edges = np.linspace(min_price, max_price, num_buckets + 1)
    bucket_labels = [(bucket_edges[i] + bucket_edges[i + 1]) / 2 for i in range(num_buckets)]  # Midpoint labels

    price_counts = np.histogram(all_prices, bins=bucket_edges)[0]

    df = pd.DataFrame({"Price": bucket_labels, "Occurrences": price_counts})

    # Generate heatmap matrix
    timestamps = np.arange(100)  # Fake 100 timestamps for full horizontal lines
    heatmap_data = np.tile(df["Occurrences"].values[:, np.newaxis], len(timestamps))

    # Plot heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap="Reds", linewidths=0, xticklabels=False, yticklabels=np.round(df["Price"], 2))
    plt.gca().invert_yaxis()

    # Titles and labels
    plt.title(f"{symbol} - Price Level Heatmap ({num_buckets} Buckets)")
    plt.xlabel("Time (ignored)")
    plt.ylabel("Price Buckets")

    # Show plot
    plt.show()


def plot_ohlc(chart: Chart, symbol: str):

    """
    Plots OHLC candlestick chart for a given symbol and timeframe.

    :param chart: Instance of candlestick chart.
    :param symbol: Symbol name (e.g., BTCUSDT).
    """

    # Convert to DataFrame
    df = chart.get_as_data_frame()

    # Plot the candlestick chart
    mpf.plot(df, type="candle", volume=True, title=f"{symbol} Candlestick Chart",
             ylabel="Price", ylabel_lower="Volume", style="charles")


def plot_combined(chart: Chart, symbol: str, num_buckets: int = 50):
    """
    Plots a candlestick chart with a heatmap background.

    :param chart: Instance of candlestick chart.
    :param symbol: Trading symbol (e.g., BTCUSDT).
    :param num_buckets: Number of price buckets for heatmap.
    """
    price_bins = chart.get_price_buckets(num_buckets)

    price_counts, _ = np.histogram(chart.get_swing_prices(), bins=price_bins)

    # Convert to a 2D heatmap format
    timestamps = np.arange(len(chart.candles))  # Use actual number of timestamps
    heatmap_data = np.tile(price_counts[:, np.newaxis], (1, len(timestamps)))

    # Create figure and axes
    fig, ax = plt.subplots(figsize=(14, 7))

    # Plot Heatmap as Background
    extent = (0, len(chart.candles), chart.get_min_value(), chart.get_max_value())  # Aligns heatmap with price axis
    ax.imshow(heatmap_data, cmap="Reds", aspect="auto", extent=extent, alpha=0.5, origin="lower")

    # Plot Candlestick Chart on the Same Axes
    mpf.plot(chart.get_as_data_frame(), type="candle", ax=ax, style="charles")

    # Show final figure
    plt.title(f"{symbol} - Candlestick Chart with Heatmap")
    plt.show()


