"""
AppleTrader Pro - Main Window
Central application window with all panels
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QStatusBar, QLabel, QMenuBar, QMenu
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QKeySequence

from config import settings
from utils.logger import logger
from core.mt5_connector import connector
from core.data_manager import data_manager

# Import panels (we'll create these next)
# from gui.chart_panel import ChartPanel
# from gui.dashboard_panel import DashboardPanel
# from gui.controls_panel import ControlsPanel
# from gui.commentary_panel import CommentaryPanel
# from gui.ml_panel import MLPanel
# from gui.orders_panel import OrdersPanel


class MainWindow(QMainWindow):
    """
    Main application window
    Manages all panels and coordinates data updates
    """

    # Signals
    data_updated = pyqtSignal()
    connection_status_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.title = settings.app.window_title
        self.connected = False

        # Setup UI
        self.init_ui()

        # Setup timers
        self.init_timers()

        # Connect to MT5
        self.connect_to_mt5()

        logger.info("Main window initialized")

    def init_ui(self):
        """Initialize user interface"""

        # Window properties
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, settings.app.window_width, settings.app.window_height)
        self.setMinimumSize(settings.app.window_min_width, settings.app.window_min_height)

        # Create menu bar
        self.create_menu_bar()

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout (vertical)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create main splitter (horizontal)
        main_splitter = QSplitter(Qt.Orientation.Horizontal)

        # ============================================================
        # LEFT PANEL: Controls
        # ============================================================
        left_panel = QWidget()
        left_panel.setFixedWidth(320)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 10, 10, 10)

        # Placeholder for controls panel
        controls_label = QLabel("⚙️ CONTROLS PANEL")
        controls_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                padding: 20px;
                background-color: #141B2D;
                border-radius: 6px;
            }
        """)
        left_layout.addWidget(controls_label)

        # Add controls panel here (when created)
        # self.controls_panel = ControlsPanel()
        # left_layout.addWidget(self.controls_panel)

        main_splitter.addWidget(left_panel)

        # ============================================================
        # CENTER PANEL: Chart + Commentary
        # ============================================================
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        center_layout.setContentsMargins(10, 10, 10, 10)

        # Center splitter (vertical)
        center_splitter = QSplitter(Qt.Orientation.Vertical)

        # Top: Chart
        chart_container = QWidget()
        chart_layout = QVBoxLayout(chart_container)
        chart_label = QLabel("📈 CHART PANEL")
        chart_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                padding: 20px;
                background-color: #141B2D;
                border-radius: 6px;
            }
        """)
        chart_layout.addWidget(chart_label)

        # Add chart panel here (when created)
        # self.chart_panel = ChartPanel()
        # chart_layout.addWidget(self.chart_panel)

        center_splitter.addWidget(chart_container)

        # Bottom: Commentary + ML
        bottom_panel = QWidget()
        bottom_layout = QHBoxLayout(bottom_panel)

        # Commentary panel
        commentary_container = QWidget()
        commentary_layout = QVBoxLayout(commentary_container)
        commentary_label = QLabel("💬 COMMENTARY")
        commentary_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                background-color: #141B2D;
                border-radius: 6px;
            }
        """)
        commentary_layout.addWidget(commentary_label)

        # Add commentary panel here (when created)
        # self.commentary_panel = CommentaryPanel()
        # commentary_layout.addWidget(self.commentary_panel)

        bottom_layout.addWidget(commentary_container)

        # ML panel
        ml_container = QWidget()
        ml_layout = QVBoxLayout(ml_container)
        ml_label = QLabel("🤖 ML INSIGHTS")
        ml_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                background-color: #141B2D;
                border-radius: 6px;
            }
        """)
        ml_layout.addWidget(ml_label)

        # Add ML panel here (when created)
        # self.ml_panel = MLPanel()
        # ml_layout.addWidget(self.ml_panel)

        bottom_layout.addWidget(ml_container)

        center_splitter.addWidget(bottom_panel)

        # Set initial sizes (70% chart, 30% commentary)
        center_splitter.setSizes([700, 300])

        center_layout.addWidget(center_splitter)
        main_splitter.addWidget(center_panel)

        # ============================================================
        # RIGHT PANEL: Dashboard + Orders
        # ============================================================
        right_panel = QWidget()
        right_panel.setFixedWidth(420)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)

        # Right splitter (vertical)
        right_splitter = QSplitter(Qt.Orientation.Vertical)

        # Top: Market Status
        dashboard_container = QWidget()
        dashboard_layout = QVBoxLayout(dashboard_container)
        dashboard_label = QLabel("📊 MARKET STATUS")
        dashboard_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                background-color: #141B2D;
                border-radius: 6px;
            }
        """)
        dashboard_layout.addWidget(dashboard_label)

        # Add dashboard panel here (when created)
        # self.dashboard_panel = DashboardPanel()
        # dashboard_layout.addWidget(self.dashboard_panel)

        right_splitter.addWidget(dashboard_container)

        # Bottom: Orders
        orders_container = QWidget()
        orders_layout = QVBoxLayout(orders_container)
        orders_label = QLabel("📋 ORDERS")
        orders_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                background-color: #141B2D;
                border-radius: 6px;
            }
        """)
        orders_layout.addWidget(orders_label)

        # Add orders panel here (when created)
        # self.orders_panel = OrdersPanel()
        # orders_layout.addWidget(self.orders_panel)

        right_splitter.addWidget(orders_container)

        # Set initial sizes (60% dashboard, 40% orders)
        right_splitter.setSizes([600, 400])

        right_layout.addWidget(right_splitter)
        main_splitter.addWidget(right_panel)

        # Set splitter sizes (300px left, expand center, 400px right)
        main_splitter.setStretchFactor(0, 0)  # Left fixed
        main_splitter.setStretchFactor(1, 1)  # Center expands
        main_splitter.setStretchFactor(2, 0)  # Right fixed

        # Add main splitter to layout
        main_layout.addWidget(main_splitter)

        # Create status bar
        self.create_status_bar()

    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        # Settings action
        settings_action = QAction("&Settings", self)
        settings_action.setShortcut(QKeySequence("Ctrl+,"))
        settings_action.triggered.connect(self.show_settings)
        file_menu.addAction(settings_action)

        file_menu.addSeparator()

        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("&View")

        # Toggle fullscreen
        fullscreen_action = QAction("&Fullscreen", self)
        fullscreen_action.setShortcut(QKeySequence("F11"))
        fullscreen_action.setCheckable(True)
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)

        # Trading menu
        trading_menu = menubar.addMenu("&Trading")

        # Connect/Disconnect
        self.connect_action = QAction("&Connect to MT5", self)
        self.connect_action.setShortcut(QKeySequence("Ctrl+K"))
        self.connect_action.triggered.connect(self.toggle_connection)
        trading_menu.addAction(self.connect_action)

        trading_menu.addSeparator()

        # Close all positions
        close_all_action = QAction("Close &All Positions", self)
        close_all_action.setShortcut(QKeySequence("Ctrl+Shift+C"))
        close_all_action.triggered.connect(self.close_all_positions)
        trading_menu.addAction(close_all_action)

        # ML menu
        ml_menu = menubar.addMenu("&ML")

        # Train model
        train_action = QAction("&Train Model", self)
        train_action.triggered.connect(self.train_ml_model)
        ml_menu.addAction(train_action)

        # Export data
        export_action = QAction("&Export Training Data", self)
        export_action.triggered.connect(self.export_ml_data)
        ml_menu.addAction(export_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        # About
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_status_bar(self):
        """Create status bar"""
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # Connection status
        self.connection_label = QLabel("⚫ Disconnected")
        self.connection_label.setStyleSheet("color: #EF4444; font-weight: bold;")
        self.statusBar.addPermanentWidget(self.connection_label)

        # Data status
        self.data_label = QLabel("📊 No data")
        self.statusBar.addPermanentWidget(self.data_label)

        # ML status
        self.ml_label = QLabel("🤖 ML: Off")
        self.statusBar.addPermanentWidget(self.ml_label)

        # Initial message
        self.statusBar.showMessage("Ready - Connect to MT5 to start", 5000)

    def init_timers(self):
        """Initialize update timers"""

        # Market data update timer (every 10 seconds as requested)
        self.market_data_timer = QTimer()
        self.market_data_timer.timeout.connect(self.update_market_data)
        self.market_data_timer.start(settings.app.market_data_update_interval)

        # UI refresh timer (250ms for smooth updates)
        self.ui_timer = QTimer()
        self.ui_timer.timeout.connect(self.update_ui)
        self.ui_timer.start(settings.app.ui_refresh_interval)

        logger.debug("Timers initialized")

    def connect_to_mt5(self):
        """Connect to MetaTrader 5"""
        if connector.initialize():
            self.connected = True
            self.connection_label.setText("🟢 Connected")
            self.connection_label.setStyleSheet("color: #10B981; font-weight: bold;")
            self.connect_action.setText("&Disconnect from MT5")
            self.statusBar.showMessage("✓ Connected to MT5", 3000)

            # Emit signal
            self.connection_status_changed.emit(True)

            logger.info("✓ MT5 connection established")
        else:
            self.connected = False
            self.connection_label.setText("⚫ Disconnected")
            self.connection_label.setStyleSheet("color: #EF4444; font-weight: bold;")
            self.statusBar.showMessage("Failed to connect to MT5", 5000)

            logger.error("MT5 connection failed")

    def toggle_connection(self):
        """Toggle MT5 connection"""
        if self.connected:
            connector.shutdown()
            self.connected = False
            self.connection_label.setText("⚫ Disconnected")
            self.connection_label.setStyleSheet("color: #EF4444; font-weight: bold;")
            self.connect_action.setText("&Connect to MT5")
            self.statusBar.showMessage("Disconnected from MT5", 3000)
            self.connection_status_changed.emit(False)
        else:
            self.connect_to_mt5()

    def update_market_data(self):
        """Update market data from MT5 (called every 10 seconds)"""
        if not self.connected:
            return

        try:
            # Try to read from IPC file first (sent by EA)
            market_data = connector.read_market_data_file()

            if market_data:
                # Update data manager with IPC data
                data_manager.update_from_mt5_data(market_data)
                self.data_label.setText(f"📊 Data: {data_manager.last_update.strftime('%H:%M:%S')}")
                logger.debug("Market data updated from IPC file")

            else:
                # Fallback: Get data directly from MT5 API
                candles = connector.get_candles(settings.trading.default_symbol,
                                               settings.trading.default_timeframe,
                                               200)
                if candles is not None:
                    data_manager.update_candles(candles,
                                               settings.trading.default_symbol,
                                               settings.trading.default_timeframe)

                # Get account info
                account = connector.get_account_info()
                if account:
                    data_manager.account.update(account)

                # Get positions
                positions = connector.get_positions()
                data_manager.positions = positions

                self.data_label.setText(f"📊 API: {len(positions)} pos")
                logger.debug("Market data updated from MT5 API")

            # Emit data updated signal
            self.data_updated.emit()

        except Exception as e:
            logger.exception(f"Error updating market data: {e}")

    def update_ui(self):
        """Update UI elements (called every 250ms)"""
        # Update ML status
        ml_status = data_manager.get_ml_status()
        if ml_status.get('enabled'):
            prob = ml_status.get('probability', 0) * 100
            self.ml_label.setText(f"🤖 ML: {prob:.0f}%")
        else:
            self.ml_label.setText("🤖 ML: Off")

    def toggle_fullscreen(self, checked):
        """Toggle fullscreen mode"""
        if checked:
            self.showFullScreen()
        else:
            self.showNormal()

    def show_settings(self):
        """Show settings dialog"""
        logger.info("Settings dialog (not yet implemented)")
        self.statusBar.showMessage("Settings dialog - Coming soon", 3000)

    def close_all_positions(self):
        """Close all open positions"""
        logger.info("Close all positions (not yet implemented)")
        self.statusBar.showMessage("Close all positions - Coming soon", 3000)

    def train_ml_model(self):
        """Train ML model"""
        logger.info("ML training (not yet implemented)")
        self.statusBar.showMessage("ML training - Coming soon", 3000)

    def export_ml_data(self):
        """Export ML training data"""
        logger.info("Export ML data (not yet implemented)")
        self.statusBar.showMessage("Export ML data - Coming soon", 3000)

    def show_about(self):
        """Show about dialog"""
        from PyQt6.QtWidgets import QMessageBox

        QMessageBox.about(
            self,
            "About AppleTrader Pro",
            f"""
            <h2>🍎 AppleTrader Pro v{settings.app.version}</h2>
            <p><b>Institutional Trading Platform for MT5</b></p>
            <p>
            A professional-grade trading dashboard that provides:<br>
            • Real-time charting with advanced overlays<br>
            • Machine Learning trade filtering<br>
            • Complete EA control from Python<br>
            • Institutional dark theme interface<br>
            </p>
            <p><i>Built with ❤️ for professional traders</i></p>
            <p>Clean charts. Clear decisions. Confident trading.</p>
            """
        )

    def closeEvent(self, event):
        """Handle window close event"""
        logger.info("Application shutting down...")

        # Save settings
        settings.save()

        # Disconnect MT5
        if self.connected:
            connector.shutdown()

        logger.info("Application closed")
        event.accept()
