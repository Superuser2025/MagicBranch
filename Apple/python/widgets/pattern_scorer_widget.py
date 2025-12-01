"""
AppleTrader Pro - Pattern Scorer Widget
Visual display of pattern quality scores
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QProgressBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from widgets.pattern_scorer import pattern_scorer, PatternScore


class PatternScorerWidget(QWidget):
    """
    Visual display widget for pattern quality scores

    Shows:
    - Overall score (0-100)
    - Star rating (⭐⭐⭐⭐⭐)
    - Score breakdown by factor
    - Historical win rate
    - Recommendation
    """

    def __init__(self):
        super().__init__()

        self.current_score: PatternScore = None

        self.init_ui()

        logger.info("Pattern Scorer Widget initialized")

    def init_ui(self):
        """Initialize user interface"""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # ============================================================
        # HEADER
        # ============================================================
        header = QLabel("⭐ PATTERN QUALITY SCORER")
        header.setStyleSheet(f"""
            QLabel {{
                color: {settings.theme.text_primary};
                font-size: {settings.theme.font_size_lg}px;
                font-weight: 700;
                background: transparent;
                border: none;
            }}
        """)
        layout.addWidget(header)

        # ============================================================
        # PATTERN INFO
        # ============================================================
        self.pattern_label = QLabel("No pattern detected")
        self.pattern_label.setStyleSheet(f"""
            QLabel {{
                color: {settings.theme.text_secondary};
                font-size: {settings.theme.font_size_sm}px;
                background: transparent;
                border: none;
            }}
        """)
        layout.addWidget(self.pattern_label)

        # ============================================================
        # OVERALL SCORE CARD
        # ============================================================
        score_card = self.create_score_card()
        layout.addWidget(score_card)

        # ============================================================
        # SCORE BREAKDOWN
        # ============================================================
        breakdown_frame = self.create_breakdown_section()
        layout.addWidget(breakdown_frame)

        # ============================================================
        # RECOMMENDATION
        # ============================================================
        recommendation_frame = self.create_recommendation_section()
        layout.addWidget(recommendation_frame)

        layout.addStretch()

    def create_score_card(self) -> QFrame:
        """Create overall score display card"""

        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {settings.theme.surface};
                border: 2px solid {settings.theme.border_color};
                border-radius: 12px;
                padding: 20px;
            }}
        """)

        layout = QVBoxLayout(frame)
        layout.setSpacing(8)

        # Score number
        self.score_number = QLabel("0")
        self.score_number.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_number.setStyleSheet(f"""
            QLabel {{
                color: {settings.theme.text_secondary};
                font-size: 48px;
                font-weight: 700;
                background: transparent;
                border: none;
            }}
        """)
        layout.addWidget(self.score_number)

        # Score label
        score_label = QLabel("/100")
        score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_label.setStyleSheet(f"""
            QLabel {{
                color: {settings.theme.text_secondary};
                font-size: {settings.theme.font_size_md}px;
                background: transparent;
                border: none;
            }}
        """)
        layout.addWidget(score_label)

        # Stars
        self.stars_label = QLabel("☆☆☆☆☆")
        self.stars_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stars_label.setStyleSheet(f"""
            QLabel {{
                color: {settings.theme.warning};
                font-size: {settings.theme.font_size_xl}px;
                background: transparent;
                border: none;
            }}
        """)
        layout.addWidget(self.stars_label)

        # Tier label
        self.tier_label = QLabel("NOT RATED")
        self.tier_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tier_label.setStyleSheet(f"""
            QLabel {{
                color: {settings.theme.text_secondary};
                font-size: {settings.theme.font_size_md}px;
                font-weight: 600;
                padding: 8px;
                background-color: {settings.theme.surface_light};
                border-radius: 6px;
            }}
        """)
        layout.addWidget(self.tier_label)

        return frame

    def create_breakdown_section(self) -> QFrame:
        """Create score breakdown section"""

        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {settings.theme.surface};
                border: 1px solid {settings.theme.border_color};
                border-radius: 12px;
                padding: 16px;
            }}
        """)

        layout = QVBoxLayout(frame)
        layout.setSpacing(10)

        # Title
        title = QLabel("── SCORE BREAKDOWN ──")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"""
            QLabel {{
                color: {settings.theme.accent};
                font-size: {settings.theme.font_size_sm}px;
                font-weight: 600;
                background: transparent;
                border: none;
            }}
        """)
        layout.addWidget(title)

        # Score factors
        self.score_bars = {}

        factors = [
            ('zone_alignment', 'Zone Alignment', 20),
            ('volume', 'Volume Confirmation', 25),
            ('liquidity', 'Liquidity Context', 15),
            ('mtf', 'MTF Confluence', 15),
            ('session', 'Session Quality', 10),
            ('structure', 'Structure Alignment', 10),
            ('historical', 'Historical Performance', 5),
        ]

        for key, label, max_score in factors:
            bar_widget = self.create_score_bar(label, max_score)
            self.score_bars[key] = bar_widget.findChild(QProgressBar)
            layout.addWidget(bar_widget)

        return frame

    def create_score_bar(self, label: str, max_score: int) -> QWidget:
        """Create individual score bar"""

        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Label
        label_widget = QLabel(f"{label} (0/{max_score})")
        label_widget.setObjectName(f"{label}_label")
        label_widget.setStyleSheet(f"""
            QLabel {{
                color: {settings.theme.text_primary};
                font-size: {settings.theme.font_size_xs}px;
                background: transparent;
                border: none;
            }}
        """)
        layout.addWidget(label_widget)

        # Progress bar
        progress = QProgressBar()
        progress.setRange(0, max_score)
        progress.setValue(0)
        progress.setTextVisible(False)
        progress.setFixedHeight(8)
        progress.setStyleSheet(f"""
            QProgressBar {{
                background-color: {settings.theme.surface_light};
                border: none;
                border-radius: 4px;
            }}
            QProgressBar::chunk {{
                background-color: {settings.theme.accent};
                border-radius: 4px;
            }}
        """)
        layout.addWidget(progress)

        return widget

    def create_recommendation_section(self) -> QFrame:
        """Create recommendation section"""

        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {settings.theme.surface};
                border: 1px solid {settings.theme.border_color};
                border-radius: 12px;
                padding: 16px;
            }}
        """)

        layout = QVBoxLayout(frame)
        layout.setSpacing(10)

        # Title
        title = QLabel("── RECOMMENDATION ──")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"""
            QLabel {{
                color: {settings.theme.accent};
                font-size: {settings.theme.font_size_sm}px;
                font-weight: 600;
                background: transparent;
                border: none;
            }}
        """)
        layout.addWidget(title)

        # Recommendation text
        self.recommendation_text = QLabel("Waiting for pattern...")
        self.recommendation_text.setWordWrap(True)
        self.recommendation_text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.recommendation_text.setStyleSheet(f"""
            QLabel {{
                color: {settings.theme.text_primary};
                font-size: {settings.theme.font_size_sm}px;
                font-family: {settings.theme.font_family_mono};
                padding: 12px;
                background-color: {settings.theme.surface_light};
                border-radius: 8px;
                line-height: 1.6;
            }}
        """)
        layout.addWidget(self.recommendation_text)

        # Historical stats
        self.historical_label = QLabel("")
        self.historical_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.historical_label.setStyleSheet(f"""
            QLabel {{
                color: {settings.theme.text_secondary};
                font-size: {settings.theme.font_size_xs}px;
                background: transparent;
                border: none;
            }}
        """)
        layout.addWidget(self.historical_label)

        return frame

    def update_score(self, score: PatternScore):
        """Update display with new pattern score"""

        self.current_score = score

        # Update pattern info
        self.pattern_label.setText(
            f"{score.pattern_type} @ {score.price_level:.5f} | "
            f"{score.timestamp.strftime('%H:%M:%S')}"
        )

        # Update overall score
        self.score_number.setText(str(score.total_score))

        # Color based on tier
        color_map = {
            "MUST TAKE": settings.theme.success,
            "STRONG": settings.theme.bullish,
            "GOOD": settings.theme.accent,
            "WEAK": settings.theme.warning,
            "SKIP": settings.theme.danger
        }
        score_color = color_map.get(score.quality_tier, settings.theme.text_secondary)

        self.score_number.setStyleSheet(f"""
            QLabel {{
                color: {score_color};
                font-size: 48px;
                font-weight: 700;
                background: transparent;
                border: none;
            }}
        """)

        # Update stars
        filled_stars = "⭐" * score.stars
        empty_stars = "☆" * (5 - score.stars)
        self.stars_label.setText(filled_stars + empty_stars)

        # Update tier
        self.tier_label.setText(score.quality_tier)
        self.tier_label.setStyleSheet(f"""
            QLabel {{
                color: {score_color};
                font-size: {settings.theme.font_size_md}px;
                font-weight: 600;
                padding: 8px;
                background-color: {settings.theme.surface_light};
                border-radius: 6px;
                border: 2px solid {score_color};
            }}
        """)

        # Update score breakdown bars
        self.score_bars['zone_alignment'].setValue(score.zone_alignment_score)
        self.score_bars['volume'].setValue(score.volume_score)
        self.score_bars['liquidity'].setValue(score.liquidity_score)
        self.score_bars['mtf'].setValue(score.mtf_score)
        self.score_bars['session'].setValue(score.session_score)
        self.score_bars['structure'].setValue(score.structure_score)
        self.score_bars['historical'].setValue(score.historical_score)

        # Update recommendation
        self.recommendation_text.setText(score.recommendation)

        # Update historical stats
        if score.historical_sample_size > 0:
            self.historical_label.setText(
                f"Historical: {score.historical_win_rate*100:.0f}% Win Rate | "
                f"{score.historical_avg_rr:.1f}R Avg | "
                f"{score.historical_sample_size} Samples"
            )
        else:
            self.historical_label.setText("No historical data available")

        logger.info(f"Pattern score updated: {score.pattern_type} = {score.total_score}/100 ({score.quality_tier})")
