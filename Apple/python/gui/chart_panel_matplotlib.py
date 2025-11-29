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

    def init_chart(self):
        """Initialize chart with sample data"""

        # Generate sample candlestick data
        self.generate_sample_data()
        self.plot_candlesticks()

    def generate_sample_data(self):
        """Generate sample candlestick data for demonstration"""

        np.random.seed(42)
        num_candles = 50

        # Generate realistic price movement
        base_price = 1.32000
        prices = [base_price]

        for _ in range(num_candles - 1):
            change = np.random.randn() * 0.0005
            prices.append(prices[-1] + change)

        # Create OHLC data
        self.candle_data = []
        for i, close_price in enumerate(prices):
            high = close_price + abs(np.random.randn() * 0.0003)
            low = close_price - abs(np.random.randn() * 0.0003)
            open_price = low + np.random.random() * (high - low)

            self.candle_data.append({
                'time': i,
                'open': open_price,
                'high': high,
                'low': low,
                'close': close_price
            })

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

        # Adjust layout
        self.canvas.fig.tight_layout()
        self.canvas.draw()

    def update_chart(self):
        """Update chart with latest data"""

        try:
            # In a real implementation, get data from data_manager
            # For now, just update the sample data
            if self.candle_data:
                # Simulate new candle
                last_close = self.candle_data[-1]['close']
                change = np.random.randn() * 0.0005
                new_close = last_close + change

                new_candle = {
                    'time': len(self.candle_data),
                    'open': last_close,
                    'high': new_close + abs(np.random.randn() * 0.0003),
                    'low': new_close - abs(np.random.randn() * 0.0003),
                    'close': new_close
                }

                self.candle_data.append(new_candle)

                # Keep only last 50 candles
                if len(self.candle_data) > 50:
                    self.candle_data.pop(0)
                    # Adjust time indices
                    for i, c in enumerate(self.candle_data):
                        c['time'] = i

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

        # Regenerate data for new timeframe
        self.generate_sample_data()
        self.plot_candlesticks()

        logger.info(f"Timeframe changed to: {timeframe}")
