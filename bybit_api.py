from environs import Env
from pybit.unified_trading import HTTP

env = Env()
env.read_env()
api_key = env('API_KEY')
api_secret = env('API_SECRET')

session = HTTP(testnet=False, api_key=api_key, api_secret=api_secret)


def open_order(symbol, side, quantity, order_type, price=None, category='linear'):
    return session.place_order(category=category, symbol=symbol, order_type=order_type, side=side, qty=quantity,
                               price=price)


def cancel_all_orders(symbol, category='linear'):
    return session.cancel_all_orders(category=category, symbol=symbol, )


def cancel_order(symbol, order_id, category='linear'):
    return session.cancel_order(category=category, symbol=symbol, orderId=order_id, )


def get_open_orders(symbol=None, category='linear'):
    return session.get_open_orders(category=category, symbol=symbol, )


def get_position_info(symbol=None, category='linear', settle_coin=None):
    return session.get_positions(category=category, symbol=symbol, settleCoin=settle_coin)


def get_tickers(symbol, category='linear'):
    return session.get_tickers(symbol=symbol, category=category)


def get_instruments_info(symbol, category='linear'):
    return session.get_instruments_info(symbol=symbol, category=category)


def switch_margin_mode(symbol, category="linear", buy_leverage="3", sell_leverage="3", trade_mode=1):
    # tradeMode = 1 -> Isolated margin mode
    # tradeMode = 0 -> Cross margin mode
    session.switch_margin_mode(symbol=symbol, category=category, buyLeverage=buy_leverage, sellLeverage=sell_leverage,
                               tradeMode=trade_mode)


def set_leverage(symbol, category="linear", buy_leverage="3", sell_leverage="3"):
    session.set_leverage(symbol=symbol, category=category, buyLeverage=buy_leverage, sellLeverage=sell_leverage)


def amend_order(symbol, order_id, stop_loss, category='linear', ):
    return session.amend_order(category=category, symbol=symbol, orderId=order_id, stopLoss=stop_loss)


def trading_stop(symbol, sl_price, sl_size, tpsl_mode='Full', category='linear', position_idx=0):
    return session.set_trading_stop(category=category, symbol=symbol, tpslMode=tpsl_mode, stopLoss=str(sl_price),
                                    slSize=str(sl_size), positionIdx=position_idx, )


def trading_tp(symbol, tp_price, tp_size, tpsl_mode='Partial', category='linear', position_idx=0):
    return session.set_trading_stop(category=category, symbol=symbol, tpslMode=tpsl_mode, takeProfit=str(tp_price),
                                    tpSize=str(tp_size), position_idx=position_idx, )
