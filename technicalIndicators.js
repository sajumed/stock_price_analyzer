const technicalIndicators = require('technicalindicators');

class TechnicalIndicators {
    /**
     * Calculate Simple Moving Average (SMA)
     * @param {Array} prices - Array of closing prices
     * @param {number} period - SMA period
     * @returns {Array} SMA values
     */
    calculateSMA(prices, period = 20) {
        return technicalIndicators.sma({
            period: period,
            values: prices
        });
    }

    /**
     * Calculate Exponential Moving Average (EMA)
     * @param {Array} prices - Array of closing prices
     * @param {number} period - EMA period
     * @returns {Array} EMA values
     */
    calculateEMA(prices, period = 20) {
        return technicalIndicators.ema({
            period: period,
            values: prices
        });
    }

    /**
     * Calculate Relative Strength Index (RSI)
     * @param {Array} prices - Array of closing prices
     * @param {number} period - RSI period
     * @returns {Array} RSI values
     */
    calculateRSI(prices, period = 14) {
        return technicalIndicators.rsi({
            period: period,
            values: prices
        });
    }

    /**
     * Calculate Moving Average Convergence Divergence (MACD)
     * @param {Array} prices - Array of closing prices
     * @returns {Object} MACD values {MACD, signal, histogram}
     */
    calculateMACD(prices) {
        return technicalIndicators.macd({
            values: prices,
            fastPeriod: 12,
            slowPeriod: 26,
            signalPeriod: 9,
            SimpleMAOscillator: false,
            SimpleMASignal: false
        });
    }

    /**
     * Calculate Bollinger Bands
     * @param {Array} prices - Array of closing prices
     * @param {number} period - BB period
     * @param {number} stdDev - Standard deviation multiplier
     * @returns {Object} Bollinger Bands {upper, middle, lower}
     */
    calculateBollingerBands(prices, period = 20, stdDev = 2) {
        return technicalIndicators.bollingerbands({
            period: period,
            values: prices,
            stdDev: stdDev
        });
    }

    /**
     * Calculate all technical indicators for stock data
     * @param {Array} stockData - Array of stock data objects
     * @returns {Object} All calculated indicators
     */
    calculateAllIndicators(stockData) {
        const closingPrices = stockData.map(data => data.close);
        
        return {
            sma20: this.calculateSMA(closingPrices, 20),
            sma50: this.calculateSMA(closingPrices, 50),
            ema20: this.calculateEMA(closingPrices, 20),
            rsi: this.calculateRSI(closingPrices),
            macd: this.calculateMACD(closingPrices),
            bollingerBands: this.calculateBollingerBands(closingPrices)
        };
    }
}

module.exports = TechnicalIndicators;