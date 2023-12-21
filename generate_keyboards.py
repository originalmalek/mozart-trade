from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bybit_api import get_position_info

def get_menu_keyboard():
	buttons = [
		[KeyboardButton(text='/create_trade'), KeyboardButton(text='/cancel_trade')],
		[KeyboardButton(text='/cancel_add_orders'), KeyboardButton(text='/set_sl_breakeven')],
		[KeyboardButton(text='/cancel_add_set_breakeven')],
		[KeyboardButton(text='/show_positions')],
	]
	keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True,
	                               input_field_placeholder='Выбрать команду')
	return keyboard


def generate_positions_keyboard(action):
	positions = get_position_info(settle_coin='USDT')['result']['list']

	builder = InlineKeyboardBuilder()

	for position in positions:
		unrealised_pnl = round(float(position['unrealisedPnl']), 2)
		side = position['side']
		symbol = position['symbol']
		side_emoji = '📈' if side == 'Buy' else '📉'
		pnl_emoji = '🟢' if unrealised_pnl > 0 else '🔴'
		builder.add(InlineKeyboardButton(text=f'{symbol.replace("USDT", "")} {side_emoji} {unrealised_pnl} {pnl_emoji}',
										 callback_data=f'{action}|{symbol}'))
	builder.adjust(2)
	return builder.as_markup()

def generate_orders_keyboard():
	pass