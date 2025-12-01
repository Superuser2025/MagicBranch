"""
AppleTrader Pro - Main Application Window
Integrates all 10 improvements into a unified trading dashboard
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QTabWidget, QLabel, QComboBox, QPushButton,
                            QStatusBar, QMenuBar, QMenu, QSplitter, QGroupBox)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QFont
from datetime import datetime

# Import all improvement widgets
from widgets.correlation_heatmap_widget import CorrelationHeatmapWidget
from widgets.volatility_position_widget import VolatilityPositionWidget
from widgets.session_momentum_widget import SessionMomentumWidget
from widgets.order_flow_widget import InstitutionalOrderFlowWidget
from widgets.pattern_scorer_widget import PatternScorerWidget
from widgets.mtf_structure_widget import MTFStructureWidget
from widgets.news_impact_widget import NewsImpactWidget
from widgets.risk_reward_widget import RiskRewardWidget
from widgets.equity_curve_widget import EquityCurveWidget
from widgets.trade_journal_widget import TradeJournalWidget
from gui.chart_panel_matplotlib import ChartPanel
from gui.controls_panel import ControlsPanel


class MainWindow(QMainWindow):
    """
    AppleTrader Pro Main Window

    Combines all 10 improvements into a cohesive trading dashboard
    """

    def __init__(self):
        super().__init__()
        self.current_symbol = "EURUSD"
        self.current_timeframe = "H4"
        self.init_ui()

        # Start data update timer
        self.data_timer = QTimer()
        self.data_timer.timeout.connect(self.update_all_data)
        self.data_timer.start(1000)  # Update every 1 second

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("AppleTrader Pro - Institutional Trading Dashboard")
        self.setGeometry(100, 100, 1600, 1000)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        # === TOP TOOLBAR ===
        toolbar_layout = self.create_toolbar()
        main_layout.addLayout(toolbar_layout)

        # === MAIN CONTENT (3 COLUMNS) ===
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # LEFT COLUMN: Chart + Controls
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)

        # CENTER COLUMN: Analysis Tabs
        center_panel = self.create_center_panel()
        splitter.addWidget(center_panel)

        # RIGHT COLUMN: Performance Tabs
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)

        # Set column widths (40% left, 35% center, 25% right)
        splitter.setSizes([640, 560, 400])

        main_layout.addWidget(splitter)

        # === STATUS BAR ===
        self.create_status_bar()

        # === MENU BAR ===
        self.create_menu_bar()

        # Apply dark theme
        self.apply_dark_theme()

    def create_toolbar(self) -> QHBoxLayout:
        """Create top toolbar with symbol/timeframe selectors"""
        layout = QHBoxLayout()

        # Title
        title = QLabel("📊 AppleTrader Pro")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #00aaff;")
        layout.addWidget(title)

        layout.addStretch()

        # Symbol selector
        layout.addWidget(QLabel("Symbol:"))
        self.symbol_combo = QComboBox()
        self.symbol_combo.addItems([
            "EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD",
            "USDCAD", "NZDUSD", "EURGBP", "EURJPY", "GBPJPY"
        ])
        self.symbol_combo.currentTextChanged.connect(self.on_symbol_changed)
        self.symbol_combo.setMinimumWidth(120)
        layout.addWidget(self.symbol_combo)

        # Timeframe selector
        layout.addWidget(QLabel("Timeframe:"))
        self.timeframe_combo = QComboBox()
        self.timeframe_combo.addItems(["M15", "H1", "H4", "D1", "W1"])
        self.timeframe_combo.setCurrentText("H4")
        self.timeframe_combo.currentTextChanged.connect(self.on_timeframe_changed)
        self.timeframe_combo.setMinimumWidth(80)
        layout.addWidget(self.timeframe_combo)

        layout.addSpacing(20)

        # Connection status
        self.connection_label = QLabel("🔴 Disconnected")
        self.connection_label.setStyleSheet("color: #ff0000; font-weight: bold;")
        layout.addWidget(self.connection_label)

        return layout

    def create_left_panel(self) -> QWidget:
        """Create left panel with chart and controls"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Chart
        self.chart_panel = ChartPanel()
        layout.addWidget(self.chart_panel, 3)  # 75% height

        # Controls
        self.controls_panel = ControlsPanel()
        layout.addWidget(self.controls_panel, 1)  # 25% height

        return widget

    def create_center_panel(self) -> QWidget:
        """Create center panel with analysis tabs"""
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)

        # Tab 1: Momentum & Correlation
        momentum_tab = QWidget()
        momentum_layout = QVBoxLayout(momentum_tab)
        self.momentum_widget = SessionMomentumWidget()
        momentum_layout.addWidget(self.momentum_widget)
        tabs.addTab(momentum_tab, "⚡ Momentum")

        # Tab 2: Correlation Heatmap
        correlation_tab = QWidget()
        correlation_layout = QVBoxLayout(correlation_tab)
        self.correlation_widget = CorrelationHeatmapWidget()
        correlation_layout.addWidget(self.correlation_widget)
        tabs.addTab(correlation_tab, "🔥 Correlation")

        # Tab 3: Structure Map
        structure_tab = QWidget()
        structure_layout = QVBoxLayout(structure_tab)
        self.structure_widget = MTFStructureWidget()
        structure_layout.addWidget(self.structure_widget)
        tabs.addTab(structure_tab, "📊 Structure")

        # Tab 4: Order Flow
        orderflow_tab = QWidget()
        orderflow_layout = QVBoxLayout(orderflow_tab)
        self.orderflow_widget = InstitutionalOrderFlowWidget()
        orderflow_layout.addWidget(self.orderflow_widget)
        tabs.addTab(orderflow_tab, "💼 Order Flow")

        # Tab 5: News Events
        news_tab = QWidget()
        news_layout = QVBoxLayout(news_tab)
        self.news_widget = NewsImpactWidget()
        news_layout.addWidget(self.news_widget)
        tabs.addTab(news_tab, "📰 News")

        return tabs

    def create_right_panel(self) -> QWidget:
        """Create right panel with performance tabs"""
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)

        # Tab 1: Position Sizing
        sizing_tab = QWidget()
        sizing_layout = QVBoxLayout(sizing_tab)
        self.position_widget = VolatilityPositionWidget()
        sizing_layout.addWidget(self.position_widget)
        tabs.addTab(sizing_tab, "🎯 Position Size")

        # Tab 2: Risk-Reward
        rr_tab = QWidget()
        rr_layout = QVBoxLayout(rr_tab)
        self.rr_widget = RiskRewardWidget()
        rr_layout.addWidget(self.rr_widget)
        tabs.addTab(rr_tab, "🎯 Risk-Reward")

        # Tab 3: Pattern Scorer
        pattern_tab = QWidget()
        pattern_layout = QVBoxLayout(pattern_tab)
        self.pattern_widget = PatternScorerWidget()
        pattern_layout.addWidget(self.pattern_widget)
        tabs.addTab(pattern_tab, "⭐ Quality")

        # Tab 4: Equity Curve
        equity_tab = QWidget()
        equity_layout = QVBoxLayout(equity_tab)
        self.equity_widget = EquityCurveWidget()
        equity_layout.addWidget(self.equity_widget)
        tabs.addTab(equity_tab, "📊 Equity")

        # Tab 5: Trade Journal
        journal_tab = QWidget()
        journal_layout = QVBoxLayout(journal_tab)
        self.journal_widget = TradeJournalWidget()
        journal_layout.addWidget(self.journal_widget)
        tabs.addTab(journal_tab, "📝 Journal")

        return tabs

    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)

        self.status_bar.addPermanentWidget(QLabel(f"Last Update: {datetime.now().strftime('%H:%M:%S')}"))

    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("&File")

        export_action = QAction("Export Data", self)
        export_action.triggered.connect(self.on_export)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View Menu
        view_menu = menubar.addMenu("&View")

        refresh_action = QAction("Refresh All", self)
        refresh_action.triggered.connect(self.update_all_data)
        view_menu.addAction(refresh_action)

        # Help Menu
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def on_symbol_changed(self, symbol: str):
        """Handle symbol change"""
        self.current_symbol = symbol
        self.status_label.setText(f"Symbol changed to: {symbol}")

        # Update all widgets with new symbol
        self.orderflow_widget.set_symbol(symbol)
        self.update_all_data()

    def on_timeframe_changed(self, timeframe: str):
        """Handle timeframe change"""
        self.current_timeframe = timeframe
        self.status_label.setText(f"Timeframe changed to: {timeframe}")
        self.update_all_data()

    def update_all_data(self):
        """Update all widgets with latest data"""
        # This will be connected to MT5 connector
        # For now, just update status
        self.status_bar.showMessage(f"Updated: {datetime.now().strftime('%H:%M:%S')}", 2000)

    def on_export(self):
        """Handle export action"""
        self.status_label.setText("Exporting data...")
        # Export trade journal
        self.journal_widget.on_export_clicked()

    def show_about(self):
        """Show about dialog"""
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.about(
            self,
            "About AppleTrader Pro",
            "AppleTrader Pro v1.0\n\n"
            "Institutional-Grade Trading Dashboard\n\n"
            "Features:\n"
            "✓ 10 Advanced Trading Improvements\n"
            "✓ Real-time Market Analysis\n"
            "✓ AI-Powered Insights\n"
            "✓ Automated Trade Journal\n\n"
            "© 2025 AppleTrader Pro"
        )

    def apply_dark_theme(self):
        """Apply dark theme to main window"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QMenuBar {
                background-color: #2b2b2b;
                color: #ffffff;
                border-bottom: 1px solid #444;
            }
            QMenuBar::item:selected {
                background-color: #0d7377;
            }
            QMenu {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #444;
            }
            QMenu::item:selected {
                background-color: #0d7377;
            }
            QStatusBar {
                background-color: #2b2b2b;
                color: #ffffff;
                border-top: 1px solid #444;
            }
            QTabWidget::pane {
                border: 1px solid #444;
                background-color: #1e1e1e;
            }
            QTabBar::tab {
                background-color: #2b2b2b;
                color: #ffffff;
                padding: 8px 16px;
                border: 1px solid #444;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background-color: #0d7377;
            }
            QTabBar::tab:hover {
                background-color: #3a3a3a;
            }
            QComboBox {
                background-color: #2b2b2b;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
                color: #ffffff;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #ffffff;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #2b2b2b;
                color: #ffffff;
                selection-background-color: #0d7377;
                border: 1px solid #444;
            }
            QLabel {
                color: #ffffff;
            }
        """)

    def closeEvent(self, event):
        """Handle window close event"""
        from PyQt6.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self,
            "Confirm Exit",
            "Are you sure you want to exit AppleTrader Pro?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
