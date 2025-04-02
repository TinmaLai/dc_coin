import numpy as np
import pandas as pd
from datetime import datetime

class PatternAnalyzer:
    def __init__(self):
        self.patterns = {
            'head_and_shoulders': self.detect_head_and_shoulders,
            'double_top': self.detect_double_top,
            'double_bottom': self.detect_double_bottom,
            'triple_top': self.detect_triple_top,
            'triple_bottom': self.detect_triple_bottom,
            'triangle': self.detect_triangle,
            'wedge': self.detect_wedge,
            'flag': self.detect_flag
        }
        self.retest_zones = {
            'head_and_shoulders': self.check_hs_retest,
            'double_top': self.check_top_retest,
            'double_bottom': self.check_bottom_retest,
            'triple_top': self.check_top_retest,
            'triple_bottom': self.check_bottom_retest,
            'symmetric_triangle': self.check_triangle_retest,
            'ascending_triangle': self.check_triangle_retest,
            'descending_triangle': self.check_triangle_retest,
            'rising_wedge': self.check_wedge_retest,
            'falling_wedge': self.check_wedge_retest,
            'bull_flag': self.check_flag_retest,
            'bear_flag': self.check_flag_retest
        }

    def check_retest(self, df, pattern, pattern_type):
        """General method to check for retest based on pattern type"""
        if pattern_type in self.retest_zones:
            retest_info = self.retest_zones[pattern_type](df, pattern)
            if retest_info:
                pattern.update(retest_info)
        return pattern

    def check_hs_retest(self, df, pattern):
        """Check retest for head and shoulders pattern"""
        try:
            neckline = pattern.get('entry_price')
            if not neckline:
                return None

            # Get recent price action
            recent_prices = df['close'].iloc[-5:].values
            recent_low = min(recent_prices)
            recent_high = max(recent_prices)

            # Define retest zone (1% tolerance)
            zone_lower = neckline * 0.99
            zone_upper = neckline * 1.01

            if zone_lower <= recent_high <= zone_upper:
                return {
                    'retest_status': 'confirmed',
                    'retest_price': recent_high,
                    'retest_description': f'Giá đã retest thành công neckline tại {recent_high:.2f}'
                }
            elif recent_high > zone_upper:
                return {
                    'retest_status': 'failed',
                    'retest_price': recent_high,
                    'retest_description': f'Giá đã vượt qua vùng retest tại {recent_high:.2f}'
                }
            elif recent_high < zone_lower:
                return {
                    'retest_status': 'pending',
                    'retest_description': 'Đang chờ retest neckline'
                }
        except Exception as e:
            print(f"Error checking H&S retest: {e}")
        return None

    def check_top_retest(self, df, pattern):
        """Check retest for double/triple top patterns"""
        try:
            resistance = pattern.get('stop_loss')  # Using stop loss as resistance level
            if not resistance:
                return None

            recent_prices = df['high'].iloc[-5:].values
            recent_high = max(recent_prices)

            # Define retest zone (1% tolerance)
            zone_lower = resistance * 0.99
            zone_upper = resistance * 1.01

            if zone_lower <= recent_high <= zone_upper:
                return {
                    'retest_status': 'confirmed',
                    'retest_price': recent_high,
                    'retest_description': f'Giá đã retest thành công vùng kháng cự tại {recent_high:.2f}'
                }
            elif recent_high > zone_upper:
                return {
                    'retest_status': 'failed',
                    'retest_price': recent_high,
                    'retest_description': f'Giá đã vượt qua vùng kháng cự tại {recent_high:.2f}'
                }
            elif recent_high < zone_lower:
                return {
                    'retest_status': 'pending',
                    'retest_description': 'Đang chờ retest vùng kháng cự'
                }
        except Exception as e:
            print(f"Error checking top retest: {e}")
        return None

    def check_bottom_retest(self, df, pattern):
        """Check retest for double/triple bottom patterns"""
        try:
            support = pattern.get('stop_loss')  # Using stop loss as support level
            if not support:
                return None

            recent_prices = df['low'].iloc[-5:].values
            recent_low = min(recent_prices)

            # Define retest zone (1% tolerance)
            zone_lower = support * 0.99
            zone_upper = support * 1.01

            if zone_lower <= recent_low <= zone_upper:
                return {
                    'retest_status': 'confirmed',
                    'retest_price': recent_low,
                    'retest_description': f'Giá đã retest thành công vùng hỗ trợ tại {recent_low:.2f}'
                }
            elif recent_low < zone_lower:
                return {
                    'retest_status': 'failed',
                    'retest_price': recent_low,
                    'retest_description': f'Giá đã phá vỡ vùng hỗ trợ tại {recent_low:.2f}'
                }
            elif recent_low > zone_upper:
                return {
                    'retest_status': 'pending',
                    'retest_description': 'Đang chờ retest vùng hỗ trợ'
                }
        except Exception as e:
            print(f"Error checking bottom retest: {e}")
        return None

    def check_triangle_retest(self, df, pattern):
        """Check retest for triangle patterns"""
        try:
            breakout_level = pattern.get('entry_price')
            if not breakout_level:
                return None

            recent_prices = df['close'].iloc[-5:].values
            recent_price = recent_prices[-1]

            # Define retest zone (1% tolerance)
            zone_lower = breakout_level * 0.99
            zone_upper = breakout_level * 1.01

            if zone_lower <= recent_price <= zone_upper:
                return {
                    'retest_status': 'confirmed',
                    'retest_price': recent_price,
                    'retest_description': f'Giá đã retest thành công đường xu hướng tại {recent_price:.2f}'
                }
            elif recent_price < zone_lower and pattern.get('pattern_type') == 'ascending_triangle':
                return {
                    'retest_status': 'failed',
                    'retest_price': recent_price,
                    'retest_description': f'Giá đã phá vỡ đường xu hướng tại {recent_price:.2f}'
                }
            elif recent_price > zone_upper and pattern.get('pattern_type') == 'descending_triangle':
                return {
                    'retest_status': 'failed',
                    'retest_price': recent_price,
                    'retest_description': f'Giá đã phá vỡ đường xu hướng tại {recent_price:.2f}'
                }
            else:
                return {
                    'retest_status': 'pending',
                    'retest_description': 'Đang chờ retest đường xu hướng'
                }
        except Exception as e:
            print(f"Error checking triangle retest: {e}")
        return None

    def check_wedge_retest(self, df, pattern):
        """Check retest for wedge patterns"""
        return self.check_triangle_retest(df, pattern)  # Similar logic to triangles

    def check_flag_retest(self, df, pattern):
        """Check retest for flag patterns"""
        return self.check_triangle_retest(df, pattern)  # Similar logic to triangles
        
    def calculate_pattern_height(self, high, low):
        """Calculate pattern height"""
        return abs(high - low)
        
    def calculate_risk_reward_ratio(self, entry, tp, sl):
        """Calculate risk/reward ratio"""
        if sl == entry:  # Avoid division by zero
            return 0
        reward = abs(tp - entry)
        risk = abs(sl - entry)
        return round(reward / risk, 2) if risk > 0 else 0
        
    def validate_price_levels(self, df, entry, tp, sl, pattern_type):
        """Validate and adjust price levels based on recent volatility"""
        recent_high = df['high'].iloc[-10:].max()
        recent_low = df['low'].iloc[-10:].min()
        atr = self.calculate_atr(df)
        
        # Adjust based on pattern type and ATR
        if 'top' in pattern_type or pattern_type == 'head_and_shoulders':
            sl = min(sl, recent_high + atr)
        elif 'bottom' in pattern_type or pattern_type == 'inverse_head_and_shoulders':
            sl = max(sl, recent_low - atr)
            
        # Ensure minimum distance between levels
        min_distance = atr * 0.5
        if abs(entry - sl) < min_distance:
            sl = entry - min_distance if entry > sl else entry + min_distance
            
        if abs(entry - tp) < min_distance:
            tp = entry - min_distance if entry > tp else entry + min_distance
            
        return entry, tp, sl
        
    def calculate_atr(self, df, period=14):
        """Calculate Average True Range"""
        high = df['high']
        low = df['low']
        close = df['close']
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return tr.rolling(period).mean().iloc[-1]

    def analyze_all_patterns(self, df):
        """Analyze all patterns for a given dataframe"""
        results = []
        trend = self.get_market_trend(df)
        
        for pattern_name, pattern_func in self.patterns.items():
            pattern = pattern_func(df)
            if pattern:
                # Enhance confidence based on trend alignment
                pattern['confidence'] = self.adjust_confidence_by_trend(pattern, trend)
                # Add volume confirmation
                pattern['confidence'] = self.adjust_confidence_by_volume(df, pattern)
                # Add technical indicator confirmation
                pattern['confidence'] = self.confirm_with_indicators(df, pattern)
                # Check for retest
                pattern = self.check_retest(df, pattern, pattern['pattern_type'])
                results.append(pattern)
                
        return results

    def get_local_extrema(self, data, window=20):
        """Find local maxima and minima"""
        maxima = []
        minima = []
        
        for i in range(window, len(data) - window):
            if all(data[i] > data[i-j] for j in range(1, window+1)) and \
               all(data[i] > data[i+j] for j in range(1, window+1)):
                maxima.append(i)
            if all(data[i] < data[i-j] for j in range(1, window+1)) and \
               all(data[i] < data[i+j] for j in range(1, window+1)):
                minima.append(i)
                
        return np.array(maxima), np.array(minima)

    def get_market_trend(self, df, ma_short=20, ma_long=50):
        """Determine market trend using multiple methods"""
        # Method 1: Moving Average Analysis
        df['SMA_short'] = df['close'].rolling(window=ma_short).mean()
        df['SMA_long'] = df['close'].rolling(window=ma_long).mean()
        ma_trend = "bullish" if df['SMA_short'].iloc[-1] > df['SMA_long'].iloc[-1] else "bearish"
        
        # Method 2: Higher Highs and Lower Lows
        highs = df['high'].rolling(window=5).max()
        lows = df['low'].rolling(window=5).min()
        price_trend = "bullish" if (highs.diff() > 0).sum() > (lows.diff() < 0).sum() else "bearish"
        
        # Method 3: Price vs SMA
        price_vs_sma = "bullish" if df['close'].iloc[-1] > df['SMA_long'].iloc[-1] else "bearish"
        
        # Combine all methods
        trends = [ma_trend, price_trend, price_vs_sma]
        return max(set(trends), key=trends.count)  # Return most common trend

    def detect_head_and_shoulders(self, df, window=20):
        """Detect Head and Shoulders pattern with enhanced analysis"""
        try:
            highs = df['high'].values
            lows = df['low'].values
            peaks, _ = self.get_local_extrema(highs, window)
            
            if len(peaks) < 5:
                return None
            
            for i in range(len(peaks)-4):
                p1, p2, p3, p4, p5 = highs[peaks[i:i+5]]
                
                # Check pattern criteria with precise measurements
                if (p3 > max(p1, p5) and  # Head higher than shoulders
                    abs(p1 - p5) / p1 < 0.03 and  # Shoulders at similar levels (3% tolerance)
                    min(p2, p4) < min(p1, p5) and  # Neckline validation
                    p3 > p1 * 1.02):  # Head at least 2% higher than shoulders
                    
                    # Calculate neckline
                    neckline_start = (p1 + lows[peaks[i]:peaks[i+1]].min()) / 2
                    neckline_end = (p5 + lows[peaks[i+3]:peaks[i+4]].min()) / 2
                    neckline_slope = (neckline_end - neckline_start) / (peaks[i+4] - peaks[i])
                    neckline_angle = np.degrees(np.arctan(neckline_slope))
                    
                    # Calculate price levels
                    pattern_height = p3 - min(neckline_start, neckline_end)
                    entry_price = neckline_end
                    is_inverse = df['close'].iloc[-1] > p3
                    
                    if is_inverse:
                        stop_loss = entry_price - pattern_height * 0.1  # 10% of height
                        take_profit = entry_price + pattern_height
                    else:
                        stop_loss = entry_price + pattern_height * 0.1
                        take_profit = entry_price - pattern_height
                    
                    # Validate levels
                    entry_price, take_profit, stop_loss = self.validate_price_levels(
                        df, entry_price, take_profit, stop_loss, 
                        'inverse_head_and_shoulders' if is_inverse else 'head_and_shoulders'
                    )
                    
                    # Validate with volume
                    vol_head = df['volume'].iloc[peaks[i+2]]
                    vol_shoulders = (df['volume'].iloc[peaks[i]] + df['volume'].iloc[peaks[i+4]]) / 2
                    vol_confirms = vol_head > vol_shoulders
                    
                    risk_reward = self.calculate_risk_reward_ratio(entry_price, take_profit, stop_loss)
                    
                    pattern = {
                        'pattern_type': 'head_and_shoulders',
                        'confidence': 0.8 if vol_confirms else 0.6,
                        'price': df['close'].iloc[-1],
                        'entry_price': entry_price,
                        'take_profit': take_profit,
                        'stop_loss': stop_loss,
                        'risk_reward_ratio': risk_reward,
                        'description': (
                            f'Mô hình Vai-Đầu-Vai {"đảo ngược" if is_inverse else "chuẩn"} '
                            f'{"với xác nhận khối lượng" if vol_confirms else "cần theo dõi thêm"}. '
                            f'Entry: {entry_price:.2f}, TP: {take_profit:.2f}, SL: {stop_loss:.2f}, R/R: {risk_reward}'
                            f'Góc neckline: {neckline_angle:.1f}°'
                        )
                    }
                    return pattern
                    
        except Exception as e:
            print(f"Error in head and shoulders detection: {e}")
        return None

    def detect_double_top(self, df, window=20, tolerance=0.02):
        """Detect Double Top pattern with enhanced validation"""
        try:
            highs = df['high'].values
            peaks, _ = self.get_local_extrema(highs, window)
            
            if len(peaks) < 2:
                return None
            
            # Analyze last two peaks
            peak1, peak2 = highs[peaks[-2:]]
            peak1_idx, peak2_idx = peaks[-2:]
            
            # Validate pattern criteria
            if (abs(peak1 - peak2) / peak1 < tolerance and  # Peaks at similar levels
                peak2_idx - peak1_idx > window * 2 and  # Minimum distance between peaks
                min(df['low'].iloc[peak1_idx:peak2_idx]) < min(peak1, peak2) * 0.97):  # Valid trough
                
                # Volume analysis
                vol1 = df['volume'].iloc[peak1_idx]
                vol2 = df['volume'].iloc[peak2_idx]
                vol_trend = "bearish" if vol2 < vol1 else "neutral"
                
                # Price momentum comparison
                momentum1 = highs[peak1_idx] - highs[peak1_idx-5]
                momentum2 = highs[peak2_idx] - highs[peak2_idx-5]
                weakening = momentum2 < momentum1
                
                confidence = 0.8
                if vol_trend == "bearish":
                    confidence += 0.1
                if weakening:
                    confidence += 0.1
                    
                # Calculate price levels
                pattern_height = self.calculate_pattern_height(peak1, min(df['low'].iloc[peak1_idx:peak2_idx]))
                entry_price = min(df['low'].iloc[peak1_idx:peak2_idx])
                stop_loss = peak2 + pattern_height * 0.1  # 10% above peak2
                take_profit = entry_price - pattern_height  # Full height projection
                
                # Validate levels
                entry_price, take_profit, stop_loss = self.validate_price_levels(
                    df, entry_price, take_profit, stop_loss, 'double_top'
                )
                
                risk_reward = self.calculate_risk_reward_ratio(entry_price, take_profit, stop_loss)
                
                pattern = {
                    'pattern_type': 'double_top',
                    'confidence': min(confidence, 1.0),
                    'price': df['close'].iloc[-1],
                    'entry_price': entry_price,
                    'take_profit': take_profit,
                    'stop_loss': stop_loss,
                    'risk_reward_ratio': risk_reward,
                    'description': (
                        f'Double Top với khoảng cách {peak2_idx - peak1_idx} nến. '
                        f'{"Động lượng giảm ở đỉnh 2. " if weakening else ""}'
                        f'{"Khối lượng giảm dần." if vol_trend == "bearish" else ""}'
                        f'Entry: {entry_price:.2f}, TP: {take_profit:.2f}, SL: {stop_loss:.2f}, R/R: {risk_reward}'
                    )
                }
                return pattern
                
        except Exception as e:
            print(f"Error in double top detection: {e}")
        return None

    def detect_double_bottom(self, df, window=20, tolerance=0.02):
        """Detect Double Bottom pattern with enhanced validation"""
        try:
            lows = df['low'].values
            _, troughs = self.get_local_extrema(lows, window)
            
            if len(troughs) < 2:
                return None
            
            # Analyze last two troughs
            trough1, trough2 = lows[troughs[-2:]]
            trough1_idx, trough2_idx = troughs[-2:]
            
            # Validate pattern criteria
            if (abs(trough1 - trough2) / trough1 < tolerance and  # Troughs at similar levels
                trough2_idx - trough1_idx > window * 2 and  # Minimum distance between troughs
                max(df['high'].iloc[trough1_idx:trough2_idx]) > max(trough1, trough2) * 1.03):  # Valid peak
                
                # Volume analysis
                vol1 = df['volume'].iloc[trough1_idx]
                vol2 = df['volume'].iloc[trough2_idx]
                vol_trend = "bullish" if vol2 > vol1 else "neutral"
                
                # Price momentum comparison
                momentum1 = lows[trough1_idx] - lows[trough1_idx-5]
                momentum2 = lows[trough2_idx] - lows[trough2_idx-5]
                strengthening = momentum2 > momentum1
                
                confidence = 0.8
                if vol_trend == "bullish":
                    confidence += 0.1
                if strengthening:
                    confidence += 0.1
                    
                # Calculate price levels
                pattern_height = self.calculate_pattern_height(max(df['high'].iloc[trough1_idx:trough2_idx]), trough1)
                entry_price = max(df['high'].iloc[trough1_idx:trough2_idx])
                stop_loss = trough2 - pattern_height * 0.1  # 10% below trough2
                take_profit = entry_price + pattern_height  # Full height projection
                
                # Validate levels
                entry_price, take_profit, stop_loss = self.validate_price_levels(
                    df, entry_price, take_profit, stop_loss, 'double_bottom'
                )
                
                risk_reward = self.calculate_risk_reward_ratio(entry_price, take_profit, stop_loss)
                
                pattern = {
                    'pattern_type': 'double_bottom',
                    'confidence': min(confidence, 1.0),
                    'price': df['close'].iloc[-1],
                    'entry_price': entry_price,
                    'take_profit': take_profit,
                    'stop_loss': stop_loss,
                    'risk_reward_ratio': risk_reward,
                    'description': (
                        f'Double Bottom với khoảng cách {trough2_idx - trough1_idx} nến. '
                        f'{"Động lượng tăng ở đáy 2. " if strengthening else ""}'
                        f'{"Khối lượng tăng dần." if vol_trend == "bullish" else ""}'
                        f'Entry: {entry_price:.2f}, TP: {take_profit:.2f}, SL: {stop_loss:.2f}, R/R: {risk_reward}'
                    )
                }
                return pattern
                
        except Exception as e:
            print(f"Error in double bottom detection: {e}")
        return None

    def detect_triple_top(self, df, window=20, tolerance=0.02):
        """Detect Triple Top pattern"""
        try:
            highs = df['high'].values
            peaks, _ = self.get_local_extrema(highs, window)
            
            if len(peaks) < 3:
                return None
            
            # Check last three peaks
            peak1, peak2, peak3 = highs[peaks[-3:]]
            peak1_idx, peak2_idx, peak3_idx = peaks[-3:]
            
            if (abs(peak1 - peak2) / peak1 < tolerance and
                abs(peak2 - peak3) / peak2 < tolerance and
                abs(peak1 - peak3) / peak1 < tolerance):
                
                # Volume analysis
                vols = [df['volume'].iloc[idx] for idx in [peak1_idx, peak2_idx, peak3_idx]]
                decreasing_volume = all(vols[i] > vols[i+1] for i in range(len(vols)-1))
                
                confidence = 0.85
                if decreasing_volume:
                    confidence += 0.1
                    
                # Calculate price levels
                lowest_point = min(df['low'].iloc[peak1_idx:peak3_idx])
                pattern_height = self.calculate_pattern_height(peak1, lowest_point)
                entry_price = lowest_point
                stop_loss = peak3 + pattern_height * 0.1  # 10% above last peak
                take_profit = entry_price - pattern_height  # Full height projection
                
                # Validate levels
                entry_price, take_profit, stop_loss = self.validate_price_levels(
                    df, entry_price, take_profit, stop_loss, 'triple_top'
                )
                
                risk_reward = self.calculate_risk_reward_ratio(entry_price, take_profit, stop_loss)
                
                pattern = {
                    'pattern_type': 'triple_top',
                    'confidence': confidence,
                    'price': df['close'].iloc[-1],
                    'entry_price': entry_price,
                    'take_profit': take_profit,
                    'stop_loss': stop_loss,
                    'risk_reward_ratio': risk_reward,
                    'description': (
                        f'Triple Top với đỉnh tương đương. '
                        f'{"Khối lượng giảm dần qua các đỉnh." if decreasing_volume else ""}'
                        f'Entry: {entry_price:.2f}, TP: {take_profit:.2f}, SL: {stop_loss:.2f}, R/R: {risk_reward}'
                    )
                }
                return pattern
                
        except Exception as e:
            print(f"Error in triple top detection: {e}")
        return None

    def detect_triple_bottom(self, df, window=20, tolerance=0.02):
        """Detect Triple Bottom pattern"""
        try:
            lows = df['low'].values
            _, troughs = self.get_local_extrema(lows, window)
            
            if len(troughs) < 3:
                return None
            
            # Check last three troughs
            trough1, trough2, trough3 = lows[troughs[-3:]]
            trough1_idx, trough2_idx, trough3_idx = troughs[-3:]
            
            if (abs(trough1 - trough2) / trough1 < tolerance and
                abs(trough2 - trough3) / trough2 < tolerance and
                abs(trough1 - trough3) / trough1 < tolerance):
                
                # Volume analysis
                vols = [df['volume'].iloc[idx] for idx in [trough1_idx, trough2_idx, trough3_idx]]
                increasing_volume = all(vols[i] < vols[i+1] for i in range(len(vols)-1))
                
                confidence = 0.85
                if increasing_volume:
                    confidence += 0.1
                    
                # Calculate price levels
                highest_point = max(df['high'].iloc[trough1_idx:trough3_idx])
                pattern_height = self.calculate_pattern_height(highest_point, trough1)
                entry_price = highest_point
                stop_loss = trough3 - pattern_height * 0.1  # 10% below last trough
                take_profit = entry_price + pattern_height  # Full height projection
                
                # Validate levels
                entry_price, take_profit, stop_loss = self.validate_price_levels(
                    df, entry_price, take_profit, stop_loss, 'triple_bottom'
                )
                
                risk_reward = self.calculate_risk_reward_ratio(entry_price, take_profit, stop_loss)
                
                pattern = {
                    'pattern_type': 'triple_bottom',
                    'confidence': confidence,
                    'price': df['close'].iloc[-1],
                    'entry_price': entry_price,
                    'take_profit': take_profit,
                    'stop_loss': stop_loss,
                    'risk_reward_ratio': risk_reward,
                    'description': (
                        f'Triple Bottom với đáy tương đương. '
                        f'{"Khối lượng tăng dần qua các đáy." if increasing_volume else ""}'
                        f'Entry: {entry_price:.2f}, TP: {take_profit:.2f}, SL: {stop_loss:.2f}, R/R: {risk_reward}'
                    )
                }
                return pattern
                
        except Exception as e:
            print(f"Error in triple bottom detection: {e}")
        return None

    def detect_triangle(self, df, window=20):
        """Detect Triangle patterns with trend line analysis"""
        try:
            highs = df['high'].values[-30:]  # Last 30 periods
            lows = df['low'].values[-30:]
            
            # Calculate trend lines using least squares
            x = np.arange(len(highs))
            high_slope, high_intercept = np.polyfit(x, highs, 1)
            low_slope, low_intercept = np.polyfit(x, lows, 1)
            
            if abs(high_slope - low_slope) > 0.0001:  # Avoid division by zero
                x_intersect = (low_intercept - high_intercept) / (high_slope - low_slope)
                y_intersect = high_slope * x_intersect + high_intercept
                
                if 0 < x_intersect < len(highs) * 2:  # Convergence within reasonable range
                    if high_slope < -0.0001 and low_slope > 0.0001:
                        pattern_type = 'symmetric_triangle'
                        confidence = 0.85
                    elif high_slope < -0.0001 and abs(low_slope) < 0.0001:
                        pattern_type = 'descending_triangle'
                        confidence = 0.8
                    elif abs(high_slope) < 0.0001 and low_slope > 0.0001:
                        pattern_type = 'ascending_triangle'
                        confidence = 0.8
                    else:
                        return None
                        
                    # Calculate compression
                    initial_range = highs[0] - lows[0]
                    final_range = highs[-1] - lows[-1]
                    compression = 1 - (final_range / initial_range)
                    
                    if compression > 0.2:
                        confidence += 0.1
                        
                    # Calculate price levels based on pattern type
                    if pattern_type == 'ascending_triangle':
                        entry_price = max(highs)
                        pattern_height = max(highs) - min(lows)
                        stop_loss = min(lows[-5:])  # Use recent low
                        take_profit = entry_price + pattern_height
                    elif pattern_type == 'descending_triangle':
                        entry_price = min(lows)
                        pattern_height = max(highs) - min(lows)
                        stop_loss = max(highs[-5:])  # Use recent high
                        take_profit = entry_price - pattern_height
                    else:  # symmetric_triangle
                        current_price = df['close'].iloc[-1]
                        pattern_height = max(highs) - min(lows)
                        if current_price > y_intersect:  # Bullish breakout
                            entry_price = max(highs)
                            stop_loss = min(lows[-5:])
                            take_profit = entry_price + pattern_height
                        else:  # Bearish breakout
                            entry_price = min(lows)
                            stop_loss = max(highs[-5:])
                            take_profit = entry_price - pattern_height
                    
                    # Validate levels
                    entry_price, take_profit, stop_loss = self.validate_price_levels(
                        df, entry_price, take_profit, stop_loss, pattern_type
                    )
                    
                    risk_reward = self.calculate_risk_reward_ratio(entry_price, take_profit, stop_loss)
                    
                    pattern = {
                        'pattern_type': pattern_type,
                        'confidence': min(confidence, 1.0),
                        'price': df['close'].iloc[-1],
                        'entry_price': entry_price,
                        'take_profit': take_profit,
                        'stop_loss': stop_loss,
                        'risk_reward_ratio': risk_reward,
                        'description': (
                            f'{pattern_type.replace("_", " ").title()} '
                            f'với độ nén giá {compression:.1%}. '
                            f'Entry: {entry_price:.2f}, TP: {take_profit:.2f}, SL: {stop_loss:.2f}, R/R: {risk_reward}. '
                            f'Điểm hội tụ sau {int(x_intersect)} nến.'
                        )
                    }
                    return pattern
                    
        except Exception as e:
            print(f"Error in triangle detection: {e}")
        return None

    def detect_wedge(self, df, window=20):
        """Detect Wedge patterns"""
        try:
            closes = df['close'].values[-30:]
            highs = df['high'].values[-30:]
            lows = df['low'].values[-30:]
            
            x = np.arange(len(closes))
            high_slope, _ = np.polyfit(x, highs, 1)
            low_slope, _ = np.polyfit(x, lows, 1)
            
            if (high_slope > 0 and low_slope > 0) or (high_slope < 0 and low_slope < 0):
                if high_slope > low_slope:
                    return None
                    
                pattern_type = 'rising_wedge' if high_slope > 0 else 'falling_wedge'
                angle = abs(np.degrees(np.arctan(high_slope) - np.arctan(low_slope)))
                
                confidence = 0.75
                if angle < 10:
                    confidence += 0.1
                    
                    # Calculate price levels
                    pattern_height = max(highs) - min(lows)
                    current_price = df['close'].iloc[-1]
                    
                    if pattern_type == 'rising_wedge':  # Bearish
                        entry_price = min(lows)
                        stop_loss = max(highs) + pattern_height * 0.1
                        take_profit = entry_price - pattern_height
                    else:  # falling_wedge - Bullish
                        entry_price = max(highs)
                        stop_loss = min(lows) - pattern_height * 0.1
                        take_profit = entry_price + pattern_height
                        
                    # Validate levels
                    entry_price, take_profit, stop_loss = self.validate_price_levels(
                        df, entry_price, take_profit, stop_loss, pattern_type
                    )
                    
                    risk_reward = self.calculate_risk_reward_ratio(entry_price, take_profit, stop_loss)
                    
                    pattern = {
                        'pattern_type': pattern_type,
                        'confidence': confidence,
                        'price': df['close'].iloc[-1],
                        'entry_price': entry_price,
                        'take_profit': take_profit,
                        'stop_loss': stop_loss,
                        'risk_reward_ratio': risk_reward,
                        'description': (
                            f'{pattern_type.replace("_", " ").title()} với góc {angle:.1f}°. '
                            f'Entry: {entry_price:.2f}, TP: {take_profit:.2f}, SL: {stop_loss:.2f}, R/R: {risk_reward}'
                        )
                    }
                return pattern
                
        except Exception as e:
            print(f"Error in wedge detection: {e}")
        return None

    def detect_flag(self, df, window=20):
        """Detect Flag patterns"""
        try:
            closes = df['close'].values
            trend_start = closes[-window*2:-window].mean()
            trend_end = closes[-window:].mean()
            trend_change = (trend_end - trend_start) / trend_start
            
            if abs(trend_change) > 0.05:
                x = np.arange(window)
                y = closes[-window:]
                slope, intercept = np.polyfit(x, y, 1)
                
                if (trend_change > 0 and slope < 0) or (trend_change < 0 and slope > 0):
                    pattern_type = 'bull_flag' if trend_change > 0 else 'bear_flag'
                    
                    residuals = y - (slope * x + intercept)
                    channel_quality = 1 - (np.std(residuals) / np.mean(y))
                    
                    confidence = 0.7
                    if channel_quality > 0.9:
                        confidence += 0.1
                        
                    # Calculate flag pole height and channel height
                    pole_start = closes[-window*2:-window].max() if trend_change > 0 else closes[-window*2:-window].min()
                    pole_end = closes[-window:].min() if trend_change > 0 else closes[-window:].max()
                    pole_height = abs(pole_end - pole_start)
                    channel_height = abs(max(y) - min(y))
                    
                    if pattern_type == 'bull_flag':
                        entry_price = max(closes[-window:])
                        stop_loss = min(closes[-window:]) - channel_height * 0.5
                        take_profit = entry_price + pole_height
                    else:  # bear_flag
                        entry_price = min(closes[-window:])
                        stop_loss = max(closes[-window:]) + channel_height * 0.5
                        take_profit = entry_price - pole_height
                        
                    # Validate levels
                    entry_price, take_profit, stop_loss = self.validate_price_levels(
                        df, entry_price, take_profit, stop_loss, pattern_type
                    )
                    
                    risk_reward = self.calculate_risk_reward_ratio(entry_price, take_profit, stop_loss)
                    
                    pattern = {
                        'pattern_type': pattern_type,
                        'confidence': confidence,
                        'price': df['close'].iloc[-1],
                        'entry_price': entry_price,
                        'take_profit': take_profit,
                        'stop_loss': stop_loss,
                        'risk_reward_ratio': risk_reward,
                        'description': (
                            f'{pattern_type.replace("_", " ").title()} '
                            f'sau xu hướng {abs(trend_change):.1%}. '
                            f'Entry: {entry_price:.2f}, TP: {take_profit:.2f}, SL: {stop_loss:.2f}, R/R: {risk_reward}'
                        )
                    }
                    return pattern
                    
        except Exception as e:
            print(f"Error in flag detection: {e}")
        return None

    def adjust_confidence_by_trend(self, pattern, trend):
        """Adjust pattern confidence based on trend alignment"""
        confidence = pattern['confidence']
        bullish_patterns = ['double_bottom', 'triple_bottom', 'ascending_triangle', 'falling_wedge']
        bearish_patterns = ['double_top', 'triple_top', 'descending_triangle', 'rising_wedge']
        
        if pattern['pattern_type'] in bullish_patterns and trend == 'bullish':
            confidence = min(confidence + 0.1, 1.0)
        elif pattern['pattern_type'] in bearish_patterns and trend == 'bearish':
            confidence = min(confidence + 0.1, 1.0)
        
        return confidence

    def adjust_confidence_by_volume(self, df, pattern):
        """Adjust pattern confidence based on volume confirmation"""
        confidence = pattern['confidence']
        vol_ma = df['volume'].rolling(window=20).mean()
        recent_vol = df['volume'].iloc[-5:].mean()
        
        if recent_vol > vol_ma.iloc[-1] * 1.2:
            confidence = min(confidence + 0.05, 1.0)
        elif recent_vol < vol_ma.iloc[-1] * 0.8:
            confidence = max(confidence - 0.05, 0.0)
            
        return confidence

    def confirm_with_indicators(self, df, pattern):
        """Confirm pattern with technical indicators"""
        confidence = pattern['confidence']
        
        # Calculate indicators
        df['SMA_20'] = df['close'].rolling(window=20).mean()
        df['SMA_50'] = df['close'].rolling(window=50).mean()
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = df['close'].ewm(span=12, adjust=False).mean()
        exp2 = df['close'].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        
        # Bollinger Bands
        df['BB_middle'] = df['close'].rolling(window=20).mean()
        std = df['close'].rolling(window=20).std()
        df['BB_upper'] = df['BB_middle'] + (2 * std)
        df['BB_lower'] = df['BB_middle'] - (2 * std)
        
        # Adjust confidence based on indicators
        last_rsi = rsi.iloc[-1]
        bb_position = (df['close'].iloc[-1] - df['BB_lower'].iloc[-1]) / \
                     (df['BB_upper'].iloc[-1] - df['BB_lower'].iloc[-1])
        macd_cross = (macd.iloc[-2] < signal.iloc[-2] and macd.iloc[-1] > signal.iloc[-1]) or \
                     (macd.iloc[-2] > signal.iloc[-2] and macd.iloc[-1] < signal.iloc[-1])
        
        if pattern['pattern_type'] in ['double_bottom', 'triple_bottom']:
            if last_rsi < 30 and bb_position < 0.2:
                confidence = min(confidence + 0.1, 1.0)
        elif pattern['pattern_type'] in ['double_top', 'triple_top']:
            if last_rsi > 70 and bb_position > 0.8:
                confidence = min(confidence + 0.1, 1.0)
        
        if macd_cross:
            confidence = min(confidence + 0.05, 1.0)
            
        return confidence
