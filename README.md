# mozart-trade
An telegram bot for manage signals from Mozart Trade telegram channel

Work about bot in process
Python 3.10
## How to run
1. Clone the project
2. Install requirements.txt
```sh
pip install -r requirements.txt
```
3. Create and fill .env file
```
BYBIT_API_KEY=bybit_api_key
BYBIT_API_SECRET=bybit_api_secret
TELEGRAM_API_KEY=telegram_bot_key
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

4. Run bot
```sh
python3 bot_cmd.py
```

## How to make signal for trade
![2023-12-21 16 39 04](https://github.com/originalmalek/mozart-trade/assets/56593369/29575dad-0cfa-4fa5-9363-bd36bd224301)

1. Go to the [google sheet](https://docs.google.com/spreadsheets/d/1natldn_OdGTObRMEMCLbTaAvGc6fpmKdpT16dAtBkkc/edit?usp=sharing)
2. Fill the columns
example:
```
Symbol: BTCUSDT
Side: Buy or Sell
Market_entry: 1 or 0
Stop Loss Type: ST or Fix
Stop Loss Price: 30000
Add orders: 31000,32000,33000
Position Quantity: your position amount for all orders(enter and add orders). The value ignores if Risk > 0
Take Profit Orders: 39000, 40000, 41000
Risk: 50. Risk ignores if value is 0, then uses Position Quantity
```  
Copy dictionary with trading data  
4. In the bot menu click /create_deal  
5. Send your dict as a message  

## How to manage
1. Send /start to the bot
2. You will see menu with commands
3. Choice menu option


my telegram @originalmalek

