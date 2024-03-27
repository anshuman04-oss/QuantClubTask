import numpy as np

def ema(data, period):
    # exponential moving average is calculated using a custom exponent, and previous 
    # ema values.
    weights = np.exp(np.linspace(-1., 0., period))
    weights /= weights.sum()
    ema_values = np.convolve(data, weights, mode='full')[:len(data)]
    return ema_values

def sma(data, period):
    # Simple Moving average is just the average over the given period.
    sma_values = np.convolve(data, np.ones(period)/period, mode='valid')
    a = np.full(period-1, np.nan)  # Initialize array with NaN values
    result = np.concatenate((a, sma_values))  # Combine NaN-padded array with calculated moving averages
    return result


# data = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
# a=sma(data, 20)
# print(a)

def sma_50(data):
    return sma(data, 50)

def sma_20(data):
    return sma(data, 20)

def macd(data, short_period=12, long_period=26, signal_period=9):
    # Calculate the short-term Exponential Moving Average (EMA)
    short_ema = ema(data, short_period)
    
    # Calculate the long-term Exponential Moving Average (EMA)
    long_ema = ema(data, long_period)
    
    # Calculate the MACD line
    macd_line = short_ema - long_ema
    
    # Calculate the signal line using EMA of the MACD line
    signal_line = ema(macd_line, signal_period)
    
    # Calculate the histogram by subtracting the signal line from the MACD line
    histogram = macd_line - signal_line
    
    return histogram




def rsi(data, length=14):
    """
    Calculate Relative Strength Index (RSI) for the given closing data.

    Parameters:
        data (list or numpy array): List or array containing closing prices.
        length (int): Length of the RSI calculation period (default is 14).

    Returns:
        numpy array: Array containing RSI values corresponding to the input data.
    """
    deltas = np.diff(data)
    seed = deltas[:length]
    up = seed[seed >= 0].sum() / length
    down = -seed[seed < 0].sum() / length
    rs = up / down
    rsi_values = np.zeros_like(data)
    rsi_values[:length] = 100. - 100. / (1. + rs)

    for i in range(length, len(data)):
        delta = deltas[i - 1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up * (length - 1) + upval) / length
        down = (down * (length - 1) + downval) / length

        rs = up / down
        rsi_values[i] = 100. - 100. / (1. + rs)

    return rsi_values


def obv(data, close_prices, volumes):
    # Momentum indicator
    # Initialize an array to store On-Balance Volume (OBV) values
    obv_values = np.zeros_like(close_prices)
    
    # Set the initial OBV value to the first volume
    obv_values[0] = volumes[0]
    
    # Iterate over the close prices and volumes
    for i in range(1, len(close_prices)):
        # If the current close price is higher than the previous close price
        if close_prices[i] > close_prices[i - 1]:
            # Add the volume to the previous OBV value
            obv_values[i] = obv_values[i - 1] + volumes[i]
        # If the current close price is lower than the previous close price
        elif close_prices[i] < close_prices[i - 1]:
            # Subtract the volume from the previous OBV value
            obv_values[i] = obv_values[i - 1] - volumes[i]
        # If the current close price is equal to the previous close price
        else:
            # Maintain the same OBV value as the previous day
            obv_values[i] = obv_values[i - 1]
    
    # Return the calculated OBV values
    return obv_values


def bb(data, window=20, num_std=2):
    # Volatility indicator.
    # This works on the principle:
    # There are two critical lines, one above the market price and the other below the current
    # market price. So, we will create two bands using standard deviation.
    sma_values = sma(data, window)
    std_dev = np.std(data[-window:])
    upper_band = sma_values + num_std * std_dev
    lower_band = sma_values - num_std * std_dev
    return upper_band, lower_band


def adx(high, low, close, period=14):
    # We will take standard convention of 14 days Average Directional Index
    # ADX is a strength indicator, which is used for the prediction of continuation of trend
    
    # Calculate the upward price movement
    up_move = high - np.roll(high, 1)
    
    # Calculate the downward price movement
    down_move = np.roll(low, 1) - low
    
    # Calculate the Positive Directional Movement (DM)
    positive_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
    # Calculate the Negative Directional Movement (DM)
    negative_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
    
    # Calculate the Average True Range (ATR)
    atr_values = atr(high, low, close, period)
    
    # Calculate the Smoothed Positive Directional Movement (SMOOTHED +DM)
    smoothed_positive_dm = sma(positive_dm, period)
    # Calculate the Smoothed Negative Directional Movement (SMOOTHED -DM)
    smoothed_negative_dm = sma(negative_dm, period)
    
    # Calculate the True Range (TR)
    true_range = np.maximum(high - low, np.abs(high - np.roll(close, 1)), np.abs(low - np.roll(close, 1)))
    atr_values = atr(true_range, close, period)  # Pass 'close' prices to atr function
    
    # Calculate the Positive Directional Index (DI+)
    positive_di = 100 * smoothed_positive_dm / atr_values
    # Calculate the Negative Directional Index (DI-)
    negative_di = 100 * smoothed_negative_dm / atr_values
    
    # Calculate the Directional Movement Index (DX)
    dx = 100 * np.abs(positive_di - negative_di) / (positive_di + negative_di)
    # Calculate the Average Directional Index (ADX)
    adx_line = sma(dx, period)
    return adx_line

def atr(high, low, close, period=14):
    # Average True Range -> Greatest of the current high and low price, 
    # difference between current high price and previous low price, and 
    # difference between current low price and previous close price. 
    tr = np.maximum(high - low, np.abs(high - np.roll(close, 1)), np.abs(low - np.roll(close, 1)))
    atr_values = sma(tr, period)
    return atr_values

def stochastic_oscillator(close, high, low, period=14):
    # Momentum indicator
    stochastic_values = 100 * ((close - np.min(low[-period:])) / (np.max(high[-period:]) - np.min(low[-period:])))
    return stochastic_values

def standard_deviation(data, window=20):
    std_dev = np.std(data[-window:])
    return std_dev


