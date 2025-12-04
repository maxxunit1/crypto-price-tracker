"""
🔥 Price Fetcher Module
Retrieves cryptocurrency prices from multiple sources
Uses logic from balance checker with multiple exchange support
"""

import aiohttp
import asyncio
from typing import Optional, Dict
from datetime import datetime


class PriceFetcher:
    """Class for fetching token prices from various sources"""

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None

        # Token mapping for CoinGecko (ID differs from ticker)
        self.coingecko_ids = {
            'IRYS': 'irys',
            'BTC': 'bitcoin',
            'ETH': 'ethereum',
            'BNB': 'binancecoin',
            'SOL': 'solana',
            'USDT': 'tether',
            'USDC': 'usd-coin',
            'XRP': 'ripple',
            'ADA': 'cardano',
            'AVAX': 'avalanche-2',
            'DOT': 'polkadot',
            'MATIC': 'matic-network',
            'LINK': 'chainlink',
            'UNI': 'uniswap',
            'ATOM': 'cosmos',
        }

        # Exchange rates (updated on request)
        self.exchange_rates = {
            'USD': 1.0,
            'EUR': 0.92,
            'RUB': 92.0,
            'UAH': 41.0,  # Ukrainian hryvnia
            'KZT': 480.0  # Kazakh tenge
        }

    async def __aenter__(self):
        """Create session on context enter"""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close session on context exit"""
        if self.session:
            await self.session.close()

    async def update_exchange_rates(self) -> None:
        """Обновление курсов валют через API с fallback на несколько источников"""

        print("\n" + "=" * 50)
        print("💱 ОБНОВЛЕНИЕ КУРСОВ ВАЛЮТ")
        print("=" * 50)

        # Список БЕСПЛАТНЫХ источников без регистрации (обновляются раз в сутки)
        sources = [
            ('ExchangeRate-API', 'https://api.exchangerate-api.com/v4/latest/USD', 'rates'),
            ('Frankfurter', 'https://api.frankfurter.app/latest?from=USD', 'rates'),
            ('ExchangeRate.host', 'https://api.exchangerate.host/latest?base=USD', 'rates'),
            ('Open.er-api', 'https://open.er-api.com/v6/latest/USD', 'rates'),
        ]

        for source_name, url, rates_key in sources:
            print(f"🔄 Пробуем {source_name}...")

            try:
                async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()

                        # Проверяем наличие ключа с курсами
                        if rates_key in data:
                            rates = data[rates_key]

                            # Обновляем курсы
                            self.exchange_rates['EUR'] = rates.get('EUR', self.exchange_rates['EUR'])
                            self.exchange_rates['RUB'] = rates.get('RUB', self.exchange_rates['RUB'])
                            self.exchange_rates['UAH'] = rates.get('UAH', self.exchange_rates['UAH'])
                            self.exchange_rates['KZT'] = rates.get('KZT', self.exchange_rates['KZT'])

                            print(f"✅ Курсы получены от {source_name}!")
                            print(f"   EUR: {self.exchange_rates['EUR']:.4f}")
                            print(f"   RUB: {self.exchange_rates['RUB']:.2f}")
                            print(f"   UAH: {self.exchange_rates['UAH']:.2f}")
                            print(f"   KZT: {self.exchange_rates['KZT']:.2f}")
                            print("=" * 50)
                            return  # Успешно получили - выходим
                        else:
                            print(f"⚠️ {source_name}: неверный формат ответа (нет ключа '{rates_key}')")
                    else:
                        print(f"⚠️ {source_name}: HTTP {response.status}")

            except asyncio.TimeoutError:
                print(f"⚠️ {source_name}: таймаут (>10 сек)")
            except Exception as e:
                print(f"⚠️ {source_name}: ошибка - {e}")

        # Если ВСЕ источники упали
        print(f"\n❌ ВСЕ ИСТОЧНИКИ НЕДОСТУПНЫ!")
        print(f"📦 Используются кэшированные значения:")
        print(f"   EUR: {self.exchange_rates['EUR']:.4f}")
        print(f"   RUB: {self.exchange_rates['RUB']:.2f}")
        print(f"   UAH: {self.exchange_rates['UAH']:.2f}")
        print(f"   KZT: {self.exchange_rates['KZT']:.2f}")
        print("=" * 50)

    async def get_token_price(self, token_symbol: str) -> Optional[float]:
        """
        Get token price in USD.
        Priority: CoinGecko → Exchanges (13 sources)

        Args:
            token_symbol: Token symbol (e.g., 'ETH', 'BTC')

        Returns:
            Price in USD or None if failed to retrieve
        """

        if not self.session:
            raise RuntimeError("Session not initialized. Use 'async with PriceFetcher()' context manager.")

        # 1. PRIORITY: CoinGecko (aggregator)
        coingecko_id = self.coingecko_ids.get(token_symbol.upper(), token_symbol.lower())
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd'

        try:
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    if coingecko_id in data and 'usd' in data[coingecko_id]:
                        price = data[coingecko_id]['usd']
                        print(f"✅ {token_symbol}: ${price} (CoinGecko)")
                        return price
        except Exception as e:
            print(f"⚠️ CoinGecko unavailable for {token_symbol}: {e}")

        # 2. FALLBACK: Exchange iteration
        exchanges = [
            ('Binance', f'https://api.binance.com/api/v3/ticker/price?symbol={token_symbol}USDT'),
            ('MEXC', f'https://www.mexc.com/open/api/v2/market/ticker?symbol={token_symbol}_USDT'),
            ('OKX', f'https://www.okx.com/api/v5/market/ticker?instId={token_symbol}-USDT'),
            ('Bybit', f'https://api.bybit.com/v5/market/tickers?category=spot&symbol={token_symbol}USDT'),
            ('Gate.io', f'https://api.gateio.ws/api/v4/spot/tickers?currency_pair={token_symbol}_USDT'),
            ('KuCoin', f'https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={token_symbol}-USDT'),
            ('HTX', f'https://api.huobi.pro/market/detail/merged?symbol={token_symbol.lower()}usdt'),
            ('Coinbase', f'https://api.coinbase.com/v2/prices/{token_symbol}-USD/spot'),
            ('Bitget', f'https://api.bitget.com/api/spot/v1/market/ticker?symbol={token_symbol}USDT_SPBL'),
            ('Bitfinex', f'https://api-pub.bitfinex.com/v2/ticker/t{token_symbol}USD'),
            ('Kraken', f'https://api.kraken.com/0/public/Ticker?pair={token_symbol}USD'),
            ('Upbit', f'https://api.upbit.com/v1/ticker?markets=KRW-{token_symbol}'),
        ]

        for exchange_name, url in exchanges:
            try:
                async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()

                        # Parse response depending on exchange
                        price = None
                        if exchange_name == 'Binance':
                            price = float(data['price'])
                        elif exchange_name == 'MEXC':
                            price = float(data['data'][0]['last']) if 'data' in data and len(data['data']) > 0 else None
                        elif exchange_name == 'OKX':
                            price = float(data['data'][0]['last']) if 'data' in data and len(data['data']) > 0 else None
                        elif exchange_name == 'Bybit':
                            price = float(data['result']['list'][0]['lastPrice']) if 'result' in data else None
                        elif exchange_name == 'Gate.io':
                            price = float(data[0]['last']) if len(data) > 0 else None
                        elif exchange_name == 'KuCoin':
                            price = float(data['data']['price']) if 'data' in data else None
                        elif exchange_name == 'HTX':
                            price = float(data['tick']['close']) if 'tick' in data else None
                        elif exchange_name == 'Coinbase':
                            price = float(data['data']['amount'])
                        elif exchange_name == 'Bitget':
                            price = float(data['data']['close']) if 'data' in data else None
                        elif exchange_name == 'Bitfinex':
                            price = float(data[6]) if len(data) > 6 else None
                        elif exchange_name == 'Kraken':
                            pair_key = list(data['result'].keys())[0]
                            price = float(data['result'][pair_key]['c'][0])
                        elif exchange_name == 'Upbit':
                            price = float(data[0]['trade_price']) / 1300 if len(data) > 0 else None  # KRW -> USD

                        if price:
                            print(f"✅ {token_symbol}: ${price} ({exchange_name})")
                            return price

            except Exception as e:
                # Silently skip unavailable exchanges
                continue

        print(f"❌ Failed to get price for {token_symbol}")
        return None

    async def get_multiple_prices(self, token_symbols: list) -> Dict[str, Optional[float]]:
        """
        Get prices for multiple tokens simultaneously

        Args:
            token_symbols: List of token symbols

        Returns:
            Dictionary {token: price_in_usd}
        """
        tasks = [self.get_token_price(symbol) for symbol in token_symbols]
        prices = await asyncio.gather(*tasks)
        return dict(zip(token_symbols, prices))

    def convert_price(self, price_usd: float, currency: str) -> float:
        """
        Convert price from USD to another currency

        Args:
            price_usd: Price in USD
            currency: Target currency ('USD', 'EUR', 'RUB')

        Returns:
            Price in target currency
        """
        if currency not in self.exchange_rates:
            return price_usd

        return price_usd * self.exchange_rates[currency]

    def format_price(self, price: float, currency: str) -> str:
        """
        Format price for display

        Args:
            price: Price value
            currency: Currency

        Returns:
            Formatted string with currency symbol
        """
        currency_symbols = {
            'USD': '$',
            'EUR': '€',
            'RUB': '₽',
            'UAH': '₴',
            'KZT': '₸'
        }

        symbol = currency_symbols.get(currency, '$')

        if price >= 1000:
            return f"{symbol}{price:,.2f}"
        elif price >= 1:
            return f"{symbol}{price:.2f}"
        elif price >= 0.01:
            return f"{symbol}{price:.4f}"
        else:
            return f"{symbol}{price:.8f}"


# Example usage
async def test_price_fetcher():
    """Test price fetcher module"""
    async with PriceFetcher() as fetcher:
        # Update exchange rates
        await fetcher.update_exchange_rates()

        # Get prices for multiple tokens
        tokens = ['ETH', 'BTC', 'IRYS']
        prices = await fetcher.get_multiple_prices(tokens)

        print("\n" + "=" * 50)
        print("📊 PRICE RETRIEVAL RESULTS")
        print("=" * 50)

        for token, price_usd in prices.items():
            if price_usd:
                print(f"\n🔹 {token}:")
                print(f"   USD: {fetcher.format_price(price_usd, 'USD')}")
                print(f"   EUR: {fetcher.format_price(fetcher.convert_price(price_usd, 'EUR'), 'EUR')}")
                print(f"   RUB: {fetcher.format_price(fetcher.convert_price(price_usd, 'RUB'), 'RUB')}")
            else:
                print(f"\n❌ {token}: Price unavailable")


if __name__ == '__main__':
    # Run test
    asyncio.run(test_price_fetcher())
