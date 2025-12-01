# AppleTrader Pro - Code Sync Instructions

## 🚀 Quick Start

Two batch files are provided to sync the latest AppleTrader Pro code from GitHub:

### Option 1: Full Setup (First Time or Clean Start)
**File:** `pull_appletrader_code.bat`

This script will:
- Check if Git is installed
- Clone the repository if it doesn't exist
- Checkout the development branch
- Pull all latest code
- Show you what was updated

**Usage:**
1. Create a folder where you want the code (e.g., `C:\Projects\`)
2. Copy `pull_appletrader_code.bat` to that folder
3. Double-click `pull_appletrader_code.bat`
4. Wait for completion - code will be in `MagicBranch\` subfolder

### Option 2: Quick Update (If You Already Have the Repo)
**File:** `quick_update.bat`

This script will:
- Fetch latest changes
- Switch to the development branch
- Pull all updates

**Usage:**
1. Copy `quick_update.bat` into your existing `MagicBranch\` folder
2. Double-click `quick_update.bat`
3. Done!

---

## 📋 Requirements

- **Git for Windows** - Download from: https://git-scm.com/download/win
- **GitHub Access** - Make sure you can access: https://github.com/Superuser2025/MagicBranch

---

## 🌿 Branch Information

**Development Branch:** `claude/recover-appletrader-pro-01CDqrQt2QJVExCCkMbx7iqC`

This branch contains all 10 advanced improvements:
1. ✅ Multi-Symbol Correlation Heatmap
2. ✅ Volatility-Adjusted Position Sizing
3. ✅ Session Momentum Scanner
4. ✅ Institutional Order Flow Footprint
5. ✅ AI Pattern Quality Scorer
6. ✅ Multi-Timeframe Structure Map
7. ✅ News Event Impact Predictor
8. ✅ Risk-Reward Optimizer
9. ✅ Equity Curve & Drawdown Analyzer
10. ✅ Automated Trade Journal with AI Insights

---

## 📂 What You'll Get

After running the batch file, you'll have:

```
MagicBranch/
├── Apple/
│   └── python/
│       ├── widgets/          # All 10 improvement modules
│       │   ├── correlation_analyzer.py
│       │   ├── correlation_heatmap_widget.py
│       │   ├── equity_curve_analyzer.py
│       │   ├── equity_curve_widget.py
│       │   ├── mtf_structure_map.py
│       │   ├── mtf_structure_widget.py
│       │   ├── news_impact_predictor.py
│       │   ├── news_impact_widget.py
│       │   ├── order_flow_detector.py
│       │   ├── order_flow_widget.py
│       │   ├── pattern_scorer.py
│       │   ├── pattern_scorer_widget.py
│       │   ├── risk_reward_optimizer.py
│       │   ├── risk_reward_widget.py
│       │   ├── session_momentum_scanner.py
│       │   ├── session_momentum_widget.py
│       │   ├── trade_journal.py
│       │   ├── trade_journal_widget.py
│       │   ├── volatility_position_sizer.py
│       │   └── volatility_position_widget.py
│       ├── core/
│       │   ├── command_manager.py
│       │   ├── data_manager.py
│       │   └── risk_manager.py
│       └── gui/
│           ├── chart_panel_matplotlib.py
│           └── controls_panel.py
├── InstitutionalTradingRobot_v3.mq5
├── PROJECT_MEMORY.md         # Comprehensive project documentation
└── ... (other files)
```

---

## 🔧 Troubleshooting

### "Git is not recognized"
- Install Git from: https://git-scm.com/download/win
- Make sure to check "Add Git to PATH" during installation
- Restart your command prompt/terminal after installation

### "Failed to clone repository"
- Check your internet connection
- Verify you have access to the GitHub repository
- If repository is private, you may need to configure Git credentials

### "Branch not found"
- The batch file will automatically create and track the branch
- If issues persist, delete the `MagicBranch` folder and run `pull_appletrader_code.bat` again

### Permission Issues
- Run the batch file as Administrator (right-click → Run as administrator)
- Or run from a folder where you have write permissions

---

## 📞 Need Help?

If you encounter issues:
1. Check the error message in the command prompt
2. Ensure Git is properly installed
3. Verify internet connection
4. Try running as Administrator

---

## 🎯 Next Steps After Sync

1. **Review the Code**
   - Check `Apple/python/widgets/` for all improvement modules
   - Each module has a corresponding widget for GUI display

2. **Read Documentation**
   - Open `PROJECT_MEMORY.md` for comprehensive project overview
   - Each Python file has detailed docstrings

3. **Integration**
   - These modules are standalone and can be integrated into your main GUI
   - Each widget can be added to your PyQt6 application

4. **Testing**
   - Test each module independently
   - Connect to live/demo MT5 data for full functionality

---

## 📊 What's Included

All code is production-ready with:
- ✅ Professional dark themes (PyQt6)
- ✅ Error handling
- ✅ Real-time auto-refresh
- ✅ Signal/slot architecture
- ✅ Comprehensive docstrings
- ✅ Type hints
- ✅ Efficient algorithms

Enjoy your institutional-grade trading system! 🚀
