
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import requests
import pandas as pd

class CoinApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.result_label = Label(text='Yükselecek coinler burada listelenecek.')
        check_button = Button(text='Coinleri Kontrol Et')
        check_button.bind(on_press=self.check_coins)
        layout.add_widget(self.result_label)
        layout.add_widget(check_button)
        return layout

    def get_data(self, symbol="BTCUSDT"):
        url = "https://api.binance.com/api/v3/klines"
        params = {"symbol": symbol, "interval": "1h", "limit": 50}
        response = requests.get(url, params=params)
        data = response.json()
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
        ])
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        return df

    def detect_bos(self, df):
        if float(df["high"].iloc[-1]) > float(df["high"].iloc[-2]):
            return "Bullish BoS"
        elif float(df["low"].iloc[-1]) < float(df["low"].iloc[-2]):
            return "Bearish BoS"
        return None

    def check_coins(self, instance):
        coins = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT"]
        result = []
        for coin in coins:
            try:
                df = self.get_data(coin)
                signal = self.detect_bos(df)
                if signal:
                    result.append(f"{coin} - {signal}")
            except:
                continue
        if result:
            self.result_label.text = "\n".join(result)
        else:
            self.result_label.text = "Yükselme sinyali yok."

if __name__ == '__main__':
    CoinApp().run()
