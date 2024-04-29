/**
 * Technical Indicators Calculator - Calculates various technical indicators
 */

class TechnicalIndicators {
    /**
     * Calculate Simple Moving Average (SMA)
     * @param {Array} data - Array of price data
     * @param {number} period - Period for SMA calculation
     * @param {string} priceField - Field to use for calculation ('close', 'open', etc.)
     * @returns {Array} Array of SMA values
     */
    static calculateSMA(data, period, priceField = 'close') {
        const sma = [];
        
        for (let i = period - 1; i < data.length; i++) {
            const slice = data.slice(i - period + 1, i + 1);
            const sum = slice.reduce((acc, item) => acc + item[priceField], 0);
            const average = sum / period;
            
            sma.push({
                date: data[i].date,
                value: average
            });
        }
        
        return sma;
    }

    /**
     * Calculate Exponential Moving Average (EMA)
     */
    static calculateEMA(data, period, priceField = 'close') {
        const ema = [];
        const multiplier = 2 / (period + 1);
        
        // First EMA value is SMA
        const firstSMA = this.calculateSMA(data.slice(0, period), period, priceField)[0].value;
        ema.push({ date: data[period - 1].date, value: firstSMA });
        
        // Calculate subsequent EMA values
        for (let i = period; i < data.length; i++) {
            const currentPrice = data[i][priceField];
            const previousEMA = ema[ema.length - 1].value;
            const currentEMA = (currentPrice - previousEMA) * multiplier + previousEMA;
            
            ema.push({
                date: data[i].date,
                value: currentEMA
            });
        }
        
        return ema;
    }

    /**
     * Calculate Relative Strength Index (RSI)
     */
    static calculateRSI(data, period = 14) {
        const rsi = [];
        const gains = [];
        const losses = [];
        
        // Calculate price changes
        for (let i = 1; i < data.length; i++) {
            const change = data[i].close - data[i - 1].close;
            gains.push(change > 0 ? change : 0);
            losses.push(change < 0 ? Math.abs(change) : 0);
        }
        
        // Calculate RSI
        for (let i = period; i < gains.length; i++) {
            const avgGain = gains.slice(i - period, i).reduce((a, b) => a + b, 0) / period;
            const avgLoss = losses.slice(i - period, i).reduce((a, b) => a + b, 0) / period;
            
            if (avgLoss === 0) {
                rsi.push({ date: data[i + 1].date, value: 100 });
            } else {
                const rs = avgGain / avgLoss;
                const rsiValue = 100 - (100 / (1 + rs));
                rsi.push({ date: data[i + 1].date, value: rsiValue });
            }
        }
        
        return rsi;
    }

    /**
     * Calculate Moving Average Convergence Divergence (MACD)
     */
    static calculateMACD(data) {
        const ema12 = this.calculateEMA(data, 12);
        const ema26 = this.calculateEMA(data, 26);
        
        const macdLine = [];
        const signalLine = [];
        const histogram = [];
        
        // Calculate MACD line (12-day EMA - 26-day EMA)
        for (let i = 0; i < ema26.length; i++) {
            const macdValue = ema12[i + 14].value - ema26[i].value; // Offset due to different lengths
            macdLine.push({
                date: ema26[i].date,
                value: macdValue
            });
        }
        
        // Calculate signal line (9-day EMA of MACD line)
        const signal = this.calculateEMA(
            macdLine.map(item => ({ close: item.value, date: item.date })), 
            9
        );
        
        // Calculate histogram (MACD line - signal line)
        for (let i = 0; i < signal.length; i++) {
            histogram.push({
                date: signal[i].date,
                value: macdLine[i + 8].value - signal[i].value // Offset due to signal calculation
            });
        }
        
        return {
            macdLine: macdLine.slice(8 + 9), // Adjust for offsets
            signalLine: signal,
            histogram: histogram
        };
    }

    /**
     * Calculate Bollinger Bands
     */
    static calculateBollingerBands(data, period = 20, stdDev = 2) {
        const bands = [];
        const sma = this.calculateSMA(data, period);
        
        for (let i = 0; i < sma.length; i++) {
            const startIndex = i;
            const endIndex = i + period;
            const slice = data.slice(startIndex, endIndex);
            
            const mean = sma[i].value;
            const variance = slice.reduce((acc, item) => {
                return acc + Math.pow(item.close - mean, 2);
            }, 0) / period;
            
            const standardDeviation = Math.sqrt(variance);
            
            bands.push({
                date: sma[i].date,
                upper: mean + (standardDeviation * stdDev),
                middle: mean,
                lower: mean - (standardDeviation * stdDev)
            });
        }
        
        return bands;
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TechnicalIndicators;
}