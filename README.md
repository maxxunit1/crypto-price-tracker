# 💎 Crypto Price Tracker

**Real-time cryptocurrency price tracker with modern UI and customizable appearance**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

Track cryptocurrency prices in real-time with a sleek, customizable desktop widget. Monitor multiple tokens, switch currencies, and personalize the appearance to match your desktop theme.

---

## ✨ Features

⚡ **One-click launcher** - No Python knowledge required

💎 **Real-time prices** - Updates every 10-300 seconds (configurable)

💱 **Multi-currency** - USD, EUR, RUB, UAH, KZT support

🎨 **Fully customizable** - Colors, fonts, transparency, size

🌐 **Multiple price sources** - CoinGecko + 12 exchanges (Binance, MEXC, OKX, etc.)

📊 **Unlimited tokens** - Track as many cryptocurrencies as you want

🖥️ **Cross-platform** - Works on Windows, macOS, Linux

🔒 **No signup required** - No API keys, no registration

---

## 🎯 Perfect for

- Crypto traders monitoring multiple assets
- Investors tracking portfolio holdings
- Developers testing market data
- Anyone wanting a clean desktop price widget

---

## 🚀 Quick Start

### Windows Users

1. **Download the project** (clone or ZIP)
2. **Double-click** `start_windows.bat`
3. **Done!** ✅

### Mac/Linux Users

1. **Download the project**
2. **Make executable**: `chmod +x start_mac_linux.sh`
3. **Run**: `./start_mac_linux.sh`
4. **Done!** ✅

The launcher will automatically:
- ✅ Check Python (show download link if missing)
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Run the application

---

## 📖 Manual Setup

If you prefer manual installation:

### 1. Download the project

```bash
git clone https://github.com/YOUR_USERNAME/crypto-price-tracker.git
cd crypto-price-tracker
```

### 2. Install Python 3.8+

- Download from [python.org](https://www.python.org/downloads/)
- During installation, **CHECK "Add Python to PATH"**

### 3. Create virtual environment

```bash
python -m venv venv
```

### 4. Activate virtual environment

**Windows:**
```bash
venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run

```bash
python crypto_tracker.py
```

---

## 🎮 Usage

### First Launch

1. **Launch the application** using quick start or manual method
2. A small window will appear showing **ETH, BTC, SOL** prices (default)
3. **Right-click** anywhere on the window to open settings

### Window Controls

| Action | Result |
|--------|--------|
| **Left click + drag** | Move window around desktop |
| **Right click** | Open settings menu |
| **Double click** | Close application |
| **ESC** | Close application |

### Configuration

Edit tokens, currencies, colors, and more via the **settings menu** (right-click):

#### 💎 **Tokens Section**
- Add/remove tokens (comma-separated)
- Example: `BTC, ETH, SOL, ADA, LINK`

#### 📈 **Market Section**
- **Currency**: USD, EUR, RUB, UAH, KZT
- **Update interval**: 10, 30, 60, 120, 300 seconds

#### 🎨 **Appearance Section**
- **Font**: Choose from all system fonts
- **Size**: 9-18px
- **Transparency**: 0-100%

#### 🌈 **Color Scheme Section**
- **Background color**: Color picker
- **Text color**: Color picker

#### ⚡ **Additional Section**
- **Always on top**: Keep window above other apps

All changes are **saved automatically** and **applied in real-time**!

---

## 💾 Configuration File

Settings are stored in `config.json`:

```json
{
    "tokens": ["ETH", "BTC", "SOL"],
    "currency": "USD",
    "update_interval": 60,
    "transparency": 0.95,
    "always_on_top": false,
    "font_size": 12,
    "font_family": "Arial",
    "bg_color": "#0f1729",
    "text_color": "#ffffff"
}
```

You can edit this file directly if preferred.

---

## 📊 Price Sources

### Primary Source: **CoinGecko**
- Aggregated data from multiple exchanges
- Most reliable for mainstream tokens

### Fallback Sources (12 exchanges):
1. Binance
2. MEXC
3. OKX
4. Bybit
5. Gate.io
6. KuCoin
7. HTX (Huobi)
8. Coinbase
9. Bitget
10. Bitfinex
11. Kraken
12. Upbit

If CoinGecko is unavailable, the app automatically tries exchanges **in order** until finding a price.

---

## 🎨 Customization Examples

### Themes

**Classic Blue** (default)
- Background: `#0f1729`
- Text: `#ffffff`

**Matrix Green**
- Background: `#000000`
- Text: `#00ff00`

**Neon Purple**
- Background: `#1a0033`
- Text: `#ff00ff`

**Light Mode**
- Background: `#f0f0f0`
- Text: `#000000`

All customizable via settings → color picker!

---

## 🛠️ Troubleshooting

### Application won't start
- **Check Python**: Must be 3.8 or higher
- **Reinstall dependencies**: Delete `venv` folder and run launcher again

### Prices not updating
- **Check internet**: App requires connection for price data
- **Firewall**: Ensure Python is allowed through firewall

### Settings not opening (macOS)
- **Use alternative**: Hold **Control** and left-click instead of right-click
- Or: Right-click with two-finger tap on trackpad

### Window too small/large
- **Resize**: Drag window edges
- **Font size**: Adjust in settings → appearance → size

---

## 📦 Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows 10+, macOS 10.14+, Linux (any modern distro)
- **Internet**: Required for price updates
- **Dependencies**: 
  - `customtkinter==5.2.2`
  - `aiohttp>=3.11.0`

All dependencies are installed automatically by the launcher.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit pull requests

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🌟 Support

If you find this project useful, please consider:
- ⭐ **Starring** the repository
- 🔄 **Sharing** with others
- 🐛 **Reporting** issues

---

## 📞 Contact

For questions or suggestions:
- **GitHub Issues**: [Open an issue](https://github.com/YOUR_USERNAME/crypto-price-tracker/issues)

---

## ⚠️ Disclaimer

This tool is for **informational purposes only**. Price data is provided "as is" without warranty. Always verify prices on official exchanges before making trading decisions.

---

**Made with ❤️ for the crypto community**
