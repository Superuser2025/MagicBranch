"""
AppleTrader Pro - Matplotlib Chart Panel
Professional candlestick charts without WebEngine dependencies
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QFrame
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd
from datetime import datetime
import MetaTrader5 as mt5

from config import settings, TIMEFRAMES
from core.data_manager import data_manager
from utils.logger import logger


class MplCanvas(FigureCanvasQTAgg):
    """Matplotlib canvas for embedding in PyQt"""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # Create figure with dark theme
        plt.style.use('dark_background')
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#0A0E27')
        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor('#0A0E27')
        super().__init__(self.fig)


class ChartPanel(QWidget):
    """
    Professional matplotlib-based charting panel
    No WebEngine dependencies - works on all systems
    """

    # Signals
    timeframe_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.current_symbol = settings.app.default_symbol
        self.current_timeframe = settings.app.default_timeframe

        # Sample data for demonstration
        self.candle_data = []

        # MT5 connection status
        self.mt5_initialized = False
        self.init_mt5_connection()

        self.init_ui()

        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_chart)
        self.update_timer.start(settings.app.chart_refresh_interval)

    def init_ui(self):
        """Initialize UI components"""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Toolbar
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)

        # Chart canvas
        self.canvas = MplCanvas(self, width=10, height=6, dpi=100)
        layout.addWidget(self.canvas)

        # Initialize chart
        self.init_chart()

    def create_toolbar(self) -> QFrame:
        """Create chart toolbar with controls"""

        toolbar = QFrame()
        toolbar.setFixedHeight(60)
        toolbar.setStyleSheet(f"""
            QFrame {{
                background-color: {settings.theme.surface};
                border-bottom: 1px solid {settings.theme.border_color};
                border-radius: 0;
            }}
        """)

        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(16, 8, 16, 8)

        # Symbol label
        symbol_label = QLabel(f"📈 {self.current_symbol}")
        symbol_label.setStyleSheet(f"""
            QLabel {{
                color: {settings.theme.text_primary};
                font-size: {settings.theme.font_size_xl}px;
                font-weight: 600;
                background: transparent;
                border: none;
            }}
        """)
        layout.addWidget(symbol_label)

        layout.addSpacing(20)

        # Timeframe selector
        tf_label = QLabel("Timeframe:")
        tf_label.setStyleSheet(f"""
            QLabel {{
                color: {settings.theme.text_secondary};
                font-size: {settings.theme.font_size_md}px;
                background: transparent;
                border: none;
            }}
        """)
        layout.addWidget(tf_label)

        self.timeframe_combo = QComboBox()
        self.timeframe_combo.addItems(['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1', 'W1'])
        self.timeframe_combo.setCurrentText(self.current_timeframe)
        self.timeframe_combo.currentTextChanged.connect(self.on_timeframe_changed)
        self.timeframe_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {settings.theme.surface_light};
                color: {settings.theme.text_primary};
                border: 1px solid {settings.theme.border_color};
                border-radius: 6px;
                padding: 8px 12px;
                min-width: 80px;
                font-size: {settings.theme.font_size_md}px;
                font-weight: 600;
            }}
            QComboBox:hover {{
                border-color: {settings.theme.accent};
            }}
            QComboBox QAbstractItemView {{
                background-color: {settings.theme.surface_light};
                color: {settings.theme.text_primary};
                selection-background-color: {settings.theme.accent};
                border: 1px solid {settings.theme.border_color};
                border-radius: 6px;
            }}
        """)
        layout.addWidget(self.timeframe_combo)

        layout.addStretch()

        # Status label
        self.status_label = QLabel("Chart Ready")
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: {settings.theme.success};
                font-size: {settings.theme.font_size_sm}px;
                background: transparent;
                border: none;
            }}
        """)
        layout.addWidget(self.status_label)

        return toolbar

    def init_mt5_connection(self):
        """Initialize connection to MetaTrader5"""
        try:
            if not mt5.initialize():
                logger.error("MT5 initialize() failed")
                self.mt5_initialized = False
                return

            self.mt5_initialized = True
            logger.info(f"✓ MT5 connection established: {mt5.terminal_info()}")

        except Exception as e:
            logger.error(f"Failed to initialize MT5: {e}")
            self.mt5_initialized = False

    def get_mt5_timeframe(self, timeframe_str: str):
        """Convert timeframe string to MT5 constant"""
        timeframe_map = {
            'M1': mt5.TIMEFRAME_M1,
            'M5': mt5.TIMEFRAME_M5,
            'M15': mt5.TIMEFRAME_M15,
            'M30': mt5.TIMEFRAME_M30,
            'H1': mt5.TIMEFRAME_H1,
            'H4': mt5.TIMEFRAME_H4,
            'D1': mt5.TIMEFRAME_D1,
            'W1': mt5.TIMEFRAME_W1,
        }
        return timeframe_map.get(timeframe_str, mt5.TIMEFRAME_M5)

    def load_historical_data(self, symbol: str = None, timeframe: str = None, count: int = 100):
        """Load historical candles from MT5"""
        if not self.mt5_initialized:
            logger.warning("MT5 not initialized, cannot load historical data")
            return False

        try:
            # Try to get symbol from data_manager (what EA is actually trading)
            if symbol is None:
                price_data = data_manager.get_latest_price()
                symbol = price_data.get('symbol', self.current_symbol)
                # Update current_symbol to match what EA is trading
                if symbol and symbol != self.current_symbol:
                    self.current_symbol = symbol
                    logger.info(f"Symbol updated to match EA: {symbol}")

            timeframe = timeframe or self.current_timeframe
            mt5_timeframe = self.get_mt5_timeframe(timeframe)

            # Get historical rates from MT5
            rates = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 0, count)

            if rates is None or len(rates) == 0:
                logger.warning(f"No historical data received from MT5 for {symbol} {timeframe}")
                return False

            # Convert to our candle format
            self.candle_data = []
            for i, rate in enumerate(rates):
                candle = {
                    'time': i,
                    'open': rate['open'],
                    'high': rate['high'],
                    'low': rate['low'],
                    'close': rate['close'],
                    'timestamp': rate['time']
                }
                self.candle_data.append(candle)

            logger.info(f"✓ Loaded {len(self.candle_data)} historical candles for {symbol} {timeframe}")
            return True

        except Exception as e:
            logger.exception(f"Error loading historical data: {e}")
            return False

    def init_chart(self):
        """Initialize chart with historical and live MT5 data"""

        # First, try to load historical data from MT5
        if self.mt5_initialized:
            success = self.load_historical_data()
            if success:
                logger.info(f"Chart initialized with {len(self.candle_data)} historical candles")
            else:
                # Fallback to live data if historical load fails
                logger.info("Historical data load failed, using live data only")
                self.candle_data = []
                self.get_live_mt5_data()
        else:
            # MT5 not available, use live data from JSON
            logger.info("MT5 not initialized, using live data from JSON")
            self.candle_data = []
            self.get_live_mt5_data()

        self.plot_candlesticks()

    def get_live_mt5_data(self):
        """Get live price from MT5 data manager"""

        try:
            # Get current price from data manager
            price_data = data_manager.get_latest_price()

            bid = price_data.get('bid', 1.32000)
            ask = price_data.get('ask', 1.32020)
            mid_price = (bid + ask) / 2

            # Create a simple candle from current price
            if len(self.candle_data) == 0:
                # First candle - use current price
                new_candle = {
                    'time': 0,
                    'open': mid_price,
                    'high': ask,
                    'low': bid,
                    'close': mid_price
                }
            else:
                # Add new candle
                new_candle = {
                    'time': len(self.candle_data),
                    'open': self.candle_data[-1]['close'],
                    'high': ask,
                    'low': bid,
                    'close': mid_price
                }

            self.candle_data.append(new_candle)

            # Keep only last 50 candles
            if len(self.candle_data) > 50:
                self.candle_data.pop(0)
                # Adjust time indices
                for i, c in enumerate(self.candle_data):
                    c['time'] = i

        except Exception as e:
            logger.warning(f"Could not get MT5 data, using defaults: {e}")

    def plot_candlesticks(self):
        """Plot candlestick chart"""

        self.canvas.axes.clear()

        if not self.candle_data:
            return

        # Extract data
        times = [c['time'] for c in self.candle_data]
        opens = [c['open'] for c in self.candle_data]
        highs = [c['high'] for c in self.candle_data]
        lows = [c['low'] for c in self.candle_data]
        closes = [c['close'] for c in self.candle_data]

        # Plot candlesticks
        for i, (t, o, h, l, c) in enumerate(zip(times, opens, highs, lows, closes)):
            color = '#10B981' if c >= o else '#EF4444'  # Green if bullish, red if bearish

            # Draw wick
            self.canvas.axes.plot([t, t], [l, h], color=color, linewidth=1)

            # Draw body
            body_height = abs(c - o)
            body_bottom = min(o, c)
            rect = Rectangle((t - 0.3, body_bottom), 0.6, body_height,
                           facecolor=color, edgecolor=color)
            self.canvas.axes.add_patch(rect)

        # Styling
        self.canvas.axes.set_facecolor('#0A0E27')
        self.canvas.axes.grid(True, alpha=0.2, color='#1E293B')
        self.canvas.axes.set_xlabel('Time', color='#94A3B8', fontsize=10)
        self.canvas.axes.set_ylabel('Price', color='#94A3B8', fontsize=10)
        self.canvas.axes.tick_params(colors='#94A3B8', labelsize=9)

        # Set title
        if self.candle_data:
            current_price = self.candle_data[-1]['close']
            self.canvas.axes.set_title(
                f'{self.current_symbol} - {self.current_timeframe} | Price: {current_price:.5f}',
                color='#F8FAFC',
                fontsize=12,
                fontweight='bold',
                pad=10
            )

        # Adjust layout with proper margins
        try:
            self.canvas.fig.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.08)
        except:
            pass  # Ignore layout warnings

        self.canvas.draw()

    def update_last_candle_only(self):
        """Update only the last (forming) candle with current price"""
        if not self.candle_data:
            return

        try:
            # Get current price from data_manager (EA's live data)
            price_data = data_manager.get_latest_price()
            bid = price_data.get('bid')
            ask = price_data.get('ask')

            if bid is None or ask is None:
                return

            mid_price = (bid + ask) / 2

            # Update the last candle (the forming one)
            last_candle = self.candle_data[-1]
            last_candle['close'] = mid_price
            last_candle['high'] = max(last_candle['high'], ask)
            last_candle['low'] = min(last_candle['low'], bid)

            # Note: We don't change 'open' - it stays as it was when candle started

        except Exception as e:
            logger.debug(f"Could not update last candle: {e}")

    def update_chart(self):
        """Update chart with latest price (only updates last candle, no reload)"""

        try:
            # Update only the last candle with current price
            # DO NOT reload all 100 candles - that causes the "morphing" issue!
            self.update_last_candle_only()

            if self.candle_data:
                self.plot_candlesticks()
                self.status_label.setText(f"Updated: {datetime.now().strftime('%H:%M:%S')}")
                self.status_label.setStyleSheet(f"""
                    QLabel {{
                        color: {settings.theme.success};
                        font-size: {settings.theme.font_size_sm}px;
                        background: transparent;
                    }}
                """)

        except Exception as e:
            logger.exception(f"Error updating chart: {e}")
            self.status_label.setText("Update Error")
            self.status_label.setStyleSheet(f"""
                QLabel {{
                    color: {settings.theme.danger};
                    font-size: {settings.theme.font_size_sm}px;
                    background: transparent;
                }}
            """)

    def on_timeframe_changed(self, timeframe: str):
        """Handle timeframe change"""

        self.current_timeframe = timeframe
        self.timeframe_changed.emit(timeframe)

        # Reload historical data for new timeframe
        if self.mt5_initialized:
            success = self.load_historical_data(timeframe=timeframe)
            if not success:
                # Fallback to live data if historical load fails
                self.candle_data = []
                self.get_live_mt5_data()
        else:
            # MT5 not available, use live data
            self.candle_data = []
            self.get_live_mt5_data()

        self.plot_candlesticks()

        logger.info(f"Timeframe changed to: {timeframe}")
