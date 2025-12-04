"""
💎 CRYPTO PRICE TRACKER v1.0
Compact cryptocurrency price tracker with modern UI

Controls:
- Left click + drag = Move window
- Right click = Open settings
- Double click = Close application
- ESC = Close application
"""

import customtkinter as ctk
import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Optional
from price_fetcher import PriceFetcher
import threading
import tkinter.font as tkfont  # For system fonts
from tkinter import colorchooser  # For color picker


# ================================================================================================
# 🎨 COLOR SCHEME
# ================================================================================================

COLORS = {
    # Backgrounds
    'bg_dark': '#0f1729',      # Dark blue
    'bg_medium': '#1a2332',
    'bg_light': '#243044',
    'bg_section': '#1e2a3a',   # For settings sections
    'bg_section_hover': '#253545',
    
    # Text
    'text_primary': '#ffffff',
    'text_secondary': '#b0b0c0',
    'text_dim': '#7a8a9a',
    'text_header': '#e0f0ff',  # For section headers
    
    # Accents
    'accent': '#00d4ff',       # Bright cyan
    'accent_hover': '#00aacc',
    'accent_bright': '#0ff',   # Neon for important elements
    'positive': '#00ff88',     # Bright green
    'positive_hover': '#00cc66',
    'negative': '#ff4477',     # Bright red
    'negative_hover': '#cc3355',
    
    # Buttons
    'button_bg': '#2a3a4e',
    'button_hover': '#3a4a5e',
    'button_active': '#4a5a6e',
    
    # Dividers
    'divider': '#2a3545',
    'border': '#3a4a5e',
}

# Currency symbols
CURRENCY_SYMBOLS = {
    'USD': '$',
    'EUR': '€',
    'RUB': '₽',
    'UAH': '₴',
    'KZT': 'T',
}


# ================================================================================================
# 🚀 MAIN WINDOW
# ================================================================================================

class CryptoTrackerApp(ctk.CTk):
    """Minimalist crypto tracker window"""

    def __init__(self):
        super().__init__()

        print("=" * 50)
        print("💎 CRYPTO PRICE TRACKER v1.0")
        print("=" * 50)

        # Load configuration
        self.load_config()

        # Window setup
        self.title("")

        # Background color from config
        bg_color = self.config.get('bg_color', COLORS['bg_dark'])
        self.configure(fg_color=bg_color)

        # Keep title bar for resizing!
        # self.overrideredirect(True)

        # Flags
        self.is_updating = False
        self.price_data: Dict[str, float] = {}
        self.token_labels: Dict[str, Dict] = {}

        # Drag & drop
        self._drag_start_x = 0
        self._drag_start_y = 0

        # Create UI
        self.create_widgets()

        # Set window size
        self.update_window_size()

        # Transparency and always on top
        self.attributes('-alpha', self.config.get('transparency', 0.95))
        if self.config.get('always_on_top', False):
            self.attributes('-topmost', True)

        # Event bindings
        self.bind("<Button-1>", self.start_drag)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<Button-2>", lambda e: self.open_settings())  # macOS
        self.bind("<Button-3>", lambda e: self.open_settings())  # Windows/Linux
        self.bind("<Control-Button-1>", lambda e: self.open_settings())  # macOS alternative
        self.bind("<Double-Button-1>", lambda e: self.on_closing())
        self.bind("<Escape>", lambda e: self.on_closing())

        # Start update loop
        self.start_update_loop()

        print(f"📊 Tokens: {', '.join(self.config['tokens'])}")
        print(f"💱 Currency: {self.config.get('currency', 'USD')}")
        print(f"⏱️  Interval: {self.config.get('update_interval', 60)} sec")
        print("-" * 50)
        print("🖱️  Right click = settings | Double click = close")
        print("=" * 50)

    def load_config(self):
        """Load configuration from file"""
        default = {
            "tokens": ["ETH", "BTC", "SOL"],
            "currency": "USD",
            "update_interval": 60,
            "transparency": 0.95,
            "always_on_top": False,
            "font_size": 12,
            "font_family": "Arial",
            "bg_color": "#0f1729",
            "text_color": "#ffffff"
        }

        if os.path.exists('config.json'):
            try:
                with open('config.json', 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    default.update(loaded)
                print("✅ Configuration loaded")
            except Exception as e:
                print(f"⚠️ Config load error: {e}")
        else:
            print("📝 Created default config")

        self.config = default
        self.save_config()

    def save_config(self):
        """Save configuration to file"""
        try:
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(self.config, indent=4, fp=f)
        except Exception as e:
            print(f"❌ Save error: {e}")

    def update_window_size(self):
        """Update window size for tokens"""
        # FIXED size for stability!
        self.geometry("180x90")
        self.minsize(180, 90)

    def create_widgets(self):
        """Create UI elements"""
        font_size = self.config.get('font_size', 12)
        font_family = self.config.get('font_family', 'Arial')
        text_color = self.config.get('text_color', '#ffffff')

        self.table_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.table_frame.pack(fill="both", expand=True, padx=5, pady=5)

        for token in self.config['tokens']:
            self.create_token_row(token, font_family, font_size, text_color)

    def create_token_row(self, token: str, font_family: str, font_size: int, text_color: str):
        """Create token row"""
        row = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        row.pack(fill="x", pady=1)

        ticker = ctk.CTkLabel(
            row, text=token.upper(),
            font=ctk.CTkFont(family=font_family, size=font_size, weight="bold"),
            text_color=text_color, width=45, anchor="w"
        )
        ticker.pack(side="left")

        price = ctk.CTkLabel(
            row, text="...",
            font=ctk.CTkFont(family=font_family, size=font_size),
            text_color=text_color, anchor="e"
        )
        price.pack(side="right", fill="x", expand=True)

        self.token_labels[token.upper()] = {'ticker': ticker, 'price': price}

    def rebuild_ui(self):
        """Rebuild UI after settings change"""
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.token_labels.clear()

        font_size = self.config.get('font_size', 12)
        font_family = self.config.get('font_family', 'Arial')
        text_color = self.config.get('text_color', '#ffffff')

        for token in self.config['tokens']:
            self.create_token_row(token, font_family, font_size, text_color)

        self.update_window_size()

        bg_color = self.config.get('bg_color', COLORS['bg_dark'])
        self.configure(fg_color=bg_color)

    def start_drag(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def on_drag(self, event):
        x = self.winfo_x() + (event.x - self._drag_start_x)
        y = self.winfo_y() + (event.y - self._drag_start_y)
        self.geometry(f"+{x}+{y}")

    def open_settings(self):
        """Open settings window"""
        SettingsWindow(self)

    def start_update_loop(self):
        """Start price update loop"""
        self.loop = asyncio.new_event_loop()

        def run_loop():
            asyncio.set_event_loop(self.loop)
            self.loop.run_forever()

        self.loop_thread = threading.Thread(target=run_loop, daemon=True)
        self.loop_thread.start()

        asyncio.run_coroutine_threadsafe(self.update_loop(), self.loop)

    async def update_loop(self):
        """Main update loop"""
        while True:
            try:
                await self.update_prices()
                await asyncio.sleep(self.config['update_interval'])
            except Exception as e:
                print(f"❌ Loop error: {e}")
                await asyncio.sleep(10)

    async def update_prices(self):
        """Update token prices"""
        if self.is_updating:
            return

        self.is_updating = True
        print(f"\n🔄 [{datetime.now().strftime('%H:%M:%S')}] Updating prices...")

        try:
            async with PriceFetcher() as fetcher:
                await fetcher.update_exchange_rates()
                prices_usd = await fetcher.get_multiple_prices(self.config['tokens'])

                currency = self.config.get('currency', 'USD')

                for token, price_usd in prices_usd.items():
                    if token in self.token_labels:
                        price = fetcher.convert_price(price_usd, currency)

                        # Format price
                        if price >= 1000:
                            price_str = f"{price:,.0f}"
                        elif price >= 1:
                            price_str = f"{price:.2f}"
                        elif price >= 0.01:
                            price_str = f"{price:.4f}"
                        else:
                            price_str = f"{price:.6f}"
                        
                        # Currency symbol: $ for USD, letters for others
                        if currency == 'USD':
                            text = f"${price_str}"
                        else:
                            text = f"{price_str} {currency}"

                        self.after(0, lambda t=token, p=text:
                                  self.token_labels[t]['price'].configure(text=p))

                print(f"✅ Updated {len(prices_usd)} tokens")

        except Exception as e:
            print(f"❌ Update error: {e}")
        finally:
            self.is_updating = False

    def on_closing(self):
        """Close application"""
        print("\n👋 Closing application...")
        if hasattr(self, 'loop') and self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)
        self.destroy()


# ================================================================================================
# ⚙️ SETTINGS WINDOW
# ================================================================================================

class SettingsWindow(ctk.CTkToplevel):
    """Settings window - compact and modern"""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.title("⚙ Settings")
        self.configure(fg_color=COLORS['bg_dark'])
        self.resizable(False, False)

        self.create_widgets()
        self.after(10, self.center_window)
        self.grab_set()

    def center_window(self):
        self.update_idletasks()
        x = self.parent.winfo_x() + 50
        y = self.parent.winfo_y() + 50
        self.geometry(f"+{x}+{y}")

    def create_widgets(self):
        """Create MODERN settings interface"""
        
        # === SECTION 1: TOKENS ===
        section1 = self.create_section_frame("💎 TOKENS", top_margin=8)
        
        self.tokens_entry = ctk.CTkEntry(
            section1, width=250, height=36,
            font=ctk.CTkFont(size=13),
            fg_color=COLORS['bg_light'],
            border_color=COLORS['accent'],
            border_width=2,
            corner_radius=8
        )
        self.tokens_entry.insert(0, ", ".join(self.parent.config['tokens']))
        self.tokens_entry.pack(padx=15, pady=(8, 12))
        
        # === SECTION 2: MARKET ===
        section2 = self.create_section_frame("📈 MARKET")
        
        # Currency + Interval in one row
        market_row = ctk.CTkFrame(section2, fg_color="transparent")
        market_row.pack(padx=15, pady=8, fill="x")
        
        # Currency
        curr_frame = ctk.CTkFrame(market_row, fg_color="transparent")
        curr_frame.pack(side="left", expand=True, fill="x")
        ctk.CTkLabel(curr_frame, text="💱 Currency", 
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color=COLORS['text_header']).pack(anchor="w")
        self.currency_var = ctk.StringVar(value=self.parent.config.get('currency', 'USD'))
        self.currency_var.trace_add('write', lambda *a: self.apply_currency())
        ctk.CTkOptionMenu(
            curr_frame, variable=self.currency_var,
            values=["USD", "EUR", "RUB", "UAH", "KZT"],
            width=100, height=32,
            fg_color=COLORS['accent'],
            button_color=COLORS['accent'],
            button_hover_color=COLORS['accent_hover'],
            dropdown_fg_color=COLORS['bg_light'],
            text_color="#000000",  # Black text on cyan!
            font=ctk.CTkFont(size=12, weight="bold"),
            dropdown_font=ctk.CTkFont(size=11)
        ).pack(pady=(4, 0))
        
        # Interval
        interval_frame = ctk.CTkFrame(market_row, fg_color="transparent")
        interval_frame.pack(side="right", expand=True, fill="x", padx=(10, 0))
        ctk.CTkLabel(interval_frame, text="⏱ Update", 
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color=COLORS['text_header']).pack(anchor="w")
        interval_row = ctk.CTkFrame(interval_frame, fg_color="transparent")
        interval_row.pack(pady=(4, 0))
        self.interval_var = ctk.StringVar(value=str(self.parent.config.get('update_interval', 60)))
        self.interval_var.trace_add('write', lambda *a: self.apply_interval())
        ctk.CTkOptionMenu(
            interval_row, variable=self.interval_var,
            values=["10", "30", "60", "120", "300"],
            width=70, height=32,
            fg_color=COLORS['button_bg'],
            button_color=COLORS['button_bg'],
            button_hover_color=COLORS['button_hover'],
            dropdown_fg_color=COLORS['bg_light'],
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left", padx=(0, 4))
        ctk.CTkLabel(interval_row, text="sec",
                    font=ctk.CTkFont(size=10),
                    text_color=COLORS['text_dim']).pack(side="left")
        
        # === SECTION 3: APPEARANCE ===
        section3 = self.create_section_frame("🎨 APPEARANCE")
        
        # Font + Size
        font_row = ctk.CTkFrame(section3, fg_color="transparent")
        font_row.pack(padx=15, pady=8, fill="x")
        
        # Font
        font_frame = ctk.CTkFrame(font_row, fg_color="transparent")
        font_frame.pack(side="left", expand=True, fill="x")
        ctk.CTkLabel(font_frame, text="🔤 Font", 
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color=COLORS['text_header']).pack(anchor="w")
        self.font_var = ctk.StringVar(value=self.parent.config.get('font_family', 'Arial'))
        self.font_var.trace_add('write', lambda *a: self.apply_font())
        
        # Get ALL system fonts!
        try:
            all_fonts = list(tkfont.families())
            # Filter: remove @-fonts and sort
            fonts = sorted([f for f in all_fonts if not f.startswith('@')])
            if not fonts:
                # Fallback to popular
                fonts = ["Arial", "Segoe UI", "Tahoma", "Verdana", "Consolas"]
        except:
            # Fallback to popular
            fonts = ["Arial", "Segoe UI", "Tahoma", "Verdana", "Consolas"]
        
        ctk.CTkOptionMenu(
            font_frame, variable=self.font_var, values=fonts,
            width=130, height=32,
            fg_color=COLORS['button_bg'],
            button_hover_color=COLORS['button_hover'],
            dropdown_fg_color=COLORS['bg_light'],
            font=ctk.CTkFont(size=11)
        ).pack(pady=(4, 0))
        
        # Size
        size_frame = ctk.CTkFrame(font_row, fg_color="transparent")
        size_frame.pack(side="right", padx=(10, 0))
        ctk.CTkLabel(size_frame, text="📏 Size", 
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color=COLORS['text_header']).pack(anchor="w")
        self.fontsize_var = ctk.StringVar(value=str(self.parent.config.get('font_size', 12)))
        self.fontsize_var.trace_add('write', lambda *a: self.apply_font())
        ctk.CTkOptionMenu(
            size_frame, variable=self.fontsize_var,
            values=["9", "10", "11", "12", "13", "14", "16", "18"],
            width=70, height=32,
            fg_color=COLORS['button_bg'],
            button_hover_color=COLORS['button_hover'],
            dropdown_fg_color=COLORS['bg_light'],
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=(4, 0))
        
        # Transparency
        trans_frame = ctk.CTkFrame(section3, fg_color="transparent")
        trans_frame.pack(padx=15, pady=(8, 12), fill="x")
        
        trans_header = ctk.CTkFrame(trans_frame, fg_color="transparent")
        trans_header.pack(fill="x")
        ctk.CTkLabel(trans_header, text="🎭 Transparency", 
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color=COLORS['text_header']).pack(side="left")
        self.transparency_label = ctk.CTkLabel(
            trans_header,
            text=f"{int(self.parent.config.get('transparency', 0.95)*100)}%",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLORS['accent_bright']
        )
        self.transparency_label.pack(side="right")
        
        self.transparency_slider = ctk.CTkSlider(
            trans_frame, from_=0.0, to=1.0, number_of_steps=20,
            width=230, height=20,
            fg_color=COLORS['bg_light'],
            progress_color=COLORS['accent'],
            button_color=COLORS['accent_bright'],
            button_hover_color=COLORS['accent'],
            command=self.apply_transparency
        )
        self.transparency_slider.set(self.parent.config.get('transparency', 0.95))
        self.transparency_slider.pack(pady=(8, 0))
        
        # === SECTION 4: COLORS ===
        section4 = self.create_section_frame("🌈 COLOR SCHEME")
        
        # Background color
        bg_frame = ctk.CTkFrame(section4, fg_color="transparent")
        bg_frame.pack(padx=15, pady=8, fill="x")
        
        ctk.CTkLabel(bg_frame, text="🎨 Background", 
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color=COLORS['text_header']).pack(anchor="w")
        
        bg_controls = ctk.CTkFrame(bg_frame, fg_color="transparent")
        bg_controls.pack(pady=(4, 0), fill="x")
        
        current_bg = self.parent.config.get('bg_color', '#0f1729')
        self.bg_preview = ctk.CTkFrame(
            bg_controls, width=50, height=36,
            fg_color=current_bg,
            corner_radius=8,
            border_width=2,
            border_color=COLORS['border']
        )
        self.bg_preview.pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            bg_controls, text="🎨 Choose color", width=170, height=36,
            fg_color=COLORS['button_bg'],
            hover_color=COLORS['button_active'],
            border_width=2,
            border_color=COLORS['border'],
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=8,
            command=self.choose_bg_color
        ).pack(side="left")
        
        # Text color
        text_frame = ctk.CTkFrame(section4, fg_color="transparent")
        text_frame.pack(padx=15, pady=(8, 12), fill="x")
        
        ctk.CTkLabel(text_frame, text="✏️ Text color", 
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color=COLORS['text_header']).pack(anchor="w")
        
        text_controls = ctk.CTkFrame(text_frame, fg_color="transparent")
        text_controls.pack(pady=(4, 0), fill="x")
        
        current_text = self.parent.config.get('text_color', '#ffffff')
        self.text_preview = ctk.CTkFrame(
            text_controls, width=50, height=36,
            fg_color=current_text,
            corner_radius=8,
            border_width=2,
            border_color=COLORS['border']
        )
        self.text_preview.pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            text_controls, text="✏️ Choose color", width=170, height=36,
            fg_color=COLORS['button_bg'],
            hover_color=COLORS['button_active'],
            border_width=2,
            border_color=COLORS['border'],
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=8,
            command=self.choose_text_color
        ).pack(side="left")
        
        # === SECTION 5: ADDITIONAL ===
        section5 = self.create_section_frame("⚡ ADDITIONAL")
        
        self.ontop_var = ctk.BooleanVar(value=self.parent.config.get('always_on_top', False))
        self.ontop_var.trace_add('write', lambda *a: self.apply_always_on_top())
        
        ontop_cb = ctk.CTkCheckBox(
            section5, text="📌 Always on top",
            variable=self.ontop_var,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS['text_primary'],
            fg_color=COLORS['accent'],
            hover_color=COLORS['accent_hover'],
            border_color=COLORS['accent'],
            corner_radius=6,
            border_width=2,
            height=32
        )
        ontop_cb.pack(padx=15, pady=12)
        
        # === ACTION BUTTONS ===
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=12, pady=(15, 12))
        
        ctk.CTkButton(
            btn_frame, text="✅ Save and close",
            width=130, height=40,
            fg_color=COLORS['positive'],
            hover_color=COLORS['positive_hover'],
            text_color="#000000",
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=10,
            border_width=0,
            command=self.save_and_close
        ).pack(side="left", padx=4)
        
        ctk.CTkButton(
            btn_frame, text="❌ Cancel",
            width=100, height=40,
            fg_color=COLORS['negative'],
            hover_color=COLORS['negative_hover'],
            text_color="#ffffff",
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=10,
            border_width=0,
            command=self.destroy
        ).pack(side="right", padx=4)

    def create_section_frame(self, title: str, top_margin: int = 4):
        """Create beautiful section with header"""
        # Section header
        header = ctk.CTkFrame(self, fg_color="transparent", height=32)
        header.pack(fill="x", padx=12, pady=(top_margin, 0))
        
        ctk.CTkLabel(
            header, text=title,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLORS['text_header'],
            anchor="w"
        ).pack(side="left", padx=4)
        
        # Divider
        ctk.CTkFrame(
            header, height=2,
            fg_color=COLORS['divider']
        ).pack(side="left", fill="x", expand=True, padx=(8, 4))
        
        # Section frame with background
        section = ctk.CTkFrame(
            self,
            fg_color=COLORS['bg_section'],
            corner_radius=10,
            border_width=1,
            border_color=COLORS['border']
        )
        section.pack(fill="x", padx=12, pady=(4, 8))
        
        return section

    def apply_tokens(self):
        """Apply tokens"""
        tokens_text = self.tokens_entry.get().strip()
        if tokens_text:
            new_tokens = [t.strip().upper() for t in tokens_text.split(',') if t.strip()]
            if new_tokens and new_tokens != self.parent.config['tokens']:
                self.parent.config['tokens'] = new_tokens
                self.parent.save_config()
                self.parent.rebuild_ui()
                asyncio.run_coroutine_threadsafe(self.parent.update_prices(), self.parent.loop)
                print(f"✅ Tokens changed: {', '.join(new_tokens)}")

    def apply_currency(self):
        """Apply currency"""
        self.parent.config['currency'] = self.currency_var.get()
        self.parent.save_config()
        asyncio.run_coroutine_threadsafe(self.parent.update_prices(), self.parent.loop)

    def apply_interval(self):
        """Apply update interval"""
        self.parent.config['update_interval'] = int(self.interval_var.get())
        self.parent.save_config()

    def apply_font(self):
        """Apply font"""
        font_family = self.font_var.get()
        font_size = int(self.fontsize_var.get())
        self.parent.config['font_family'] = font_family
        self.parent.config['font_size'] = font_size
        self.parent.save_config()

        for token_data in self.parent.token_labels.values():
            token_data['ticker'].configure(font=ctk.CTkFont(family=font_family, size=font_size, weight="bold"))
            token_data['price'].configure(font=ctk.CTkFont(family=font_family, size=font_size))

        self.parent.update_window_size()

    def apply_transparency(self, value):
        """Apply transparency"""
        self.transparency_label.configure(text=f"{int(value*100)}%")
        self.parent.attributes('-alpha', value)
        self.parent.config['transparency'] = value
        self.parent.save_config()

    def apply_always_on_top(self):
        """Apply always on top"""
        self.parent.attributes('-topmost', self.ontop_var.get())
        self.parent.config['always_on_top'] = self.ontop_var.get()
        self.parent.save_config()

    def choose_bg_color(self):
        """Open color picker for background"""
        current_color = self.parent.config.get('bg_color', '#0f1729')
        
        # Open system color picker
        color = colorchooser.askcolor(
            color=current_color,
            title="Choose background color"
        )
        
        # color returns ((R,G,B), '#RRGGBB')
        if color and color[1]:
            new_color = color[1]  # HEX format
            
            # Update preview
            self.bg_preview.configure(fg_color=new_color)
            
            # Apply color
            self.parent.configure(fg_color=new_color)
            self.parent.config['bg_color'] = new_color
            self.parent.save_config()
            
            print(f"✅ Background color changed: {new_color}")

    def choose_text_color(self):
        """Open color picker for text"""
        current_color = self.parent.config.get('text_color', '#ffffff')
        
        # Open system color picker
        color = colorchooser.askcolor(
            color=current_color,
            title="Choose text color"
        )
        
        # color returns ((R,G,B), '#RRGGBB')
        if color and color[1]:
            new_color = color[1]  # HEX format
            
            # Update preview
            self.text_preview.configure(fg_color=new_color)
            
            # Apply color to all labels
            for token_data in self.parent.token_labels.values():
                token_data['ticker'].configure(text_color=new_color)
                token_data['price'].configure(text_color=new_color)
            
            self.parent.config['text_color'] = new_color
            self.parent.save_config()
            
            print(f"✅ Text color changed: {new_color}")

    def save_and_close(self):
        """Save and close"""
        self.apply_tokens()
        self.parent.save_config()
        print("✅ Settings saved")
        self.destroy()


# ================================================================================================
# 🚀 LAUNCH
# ================================================================================================

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = CryptoTrackerApp()
    app.mainloop()


if __name__ == '__main__':
    main()
