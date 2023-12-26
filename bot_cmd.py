import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from bybit_api import *
from generate_keyboards import get_menu_keyboard, generate_positions_keyboard
from mozart_deal import create_trade, cancel_trade, cancel_add_orders, set_sl_breakeven

env = Env()
env.read_env()

dp = Dispatcher()


class CommandState(StatesGroup):
    state_none = State()
    create_trade = State()
    cancel_trade = State()
    cancel_add_orders = State()
    set_sl_breakeven = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext):
    await bot.send_message(text='Добро пожаловать в панель управления сделками.\n\n Выбери нужную команду',
                           chat_id=telegram_chat_id, reply_markup=get_menu_keyboard())
    await state.set_state(CommandState.state_none)


@dp.callback_query()
async def handle_callback(callback: CallbackQuery, state: FSMContext):
    [action, symbol] = callback.data.split('|')
    message = callback.message
    if action == 'cancel_trade':
        await state_cancel_trade(message, state, symbol=symbol)
    if action == 'set_sl_breakeven':
        await state_set_sl_breakeven(message, state, symbol=symbol)
    if action == 'cancel_add_orders':
        await state_cancel_add_orders(message, state, symbol=symbol)
    await callback.answer()


@dp.message(Command('set_sl_breakeven'))
async def cmd_set_sl_breakeven(message: Message, state: FSMContext, command: CommandObject, ):
    if command.args:
        await state_set_sl_breakeven(message, state, symbol=command.args)
    else:
        positions_keyboard = generate_positions_keyboard(action='set_sl_breakeven')
        await message.answer(text='Введите или выбирите торговую пару', reply_markup=positions_keyboard)
        await state.set_state(CommandState.set_sl_breakeven)


@dp.message(Command('create_trade'))
async def cmd_create_trade(message: Message, state: FSMContext, command: CommandObject, ):
    if command.args:
        trade = command.args
        await state_create_trade(message, state, trade)
    else:
        await message.answer(text='Введите данные для создания сделки', )
        await state.set_state(CommandState.create_trade)


@dp.message(Command('cancel_trade'))
async def cmd_cancel_trade(message: Message, command: CommandObject, state: FSMContext, ):
    if command.args:
        await state_cancel_trade(message, state, symbol=command.args)
    else:
        positions_keyboard = generate_positions_keyboard(action='cancel_trade')
        await message.answer(text='Введите или выбирите торговую пару', reply_markup=positions_keyboard)

        await state.set_state(CommandState.cancel_trade)


@dp.message(Command('show_positions'))
async def cmd_cancel_add_orders(message: Message, command: CommandObject, state: FSMContext, ):
    if command.args:
        await state_cancel_add_orders(message, state, symbol=command.args)
    else:
        positions_keyboard = generate_positions_keyboard(action='show_positions')
        await message.answer(text='Статистика по парам', reply_markup=positions_keyboard)
        await state.set_state(CommandState.state_none)


@dp.message(Command('cancel_add_orders'))
async def cmd_cancel_add_orders(message: Message, command: CommandObject, state: FSMContext, ):
    if command.args:
        await state_cancel_add_orders(message, state, symbol=command.args)
    else:
        positions_keyboard = generate_positions_keyboard(action='cancel_add_orders')
        await message.answer(text='Введите торговую пару', reply_markup=positions_keyboard)
        await state.set_state(CommandState.cancel_add_orders)


@dp.message(CommandState.cancel_trade)
async def state_cancel_trade(message: Message, state: FSMContext, symbol=None):
    symbol = symbol if symbol else message.text
    await message.answer(text=f'Отменяю сделку по паре {symbol}')
    cancel_trade_status = cancel_trade(symbol)

    if 'ErrCode' in str(cancel_trade_status):
        await message.answer(text=cancel_trade_status)
    if cancel_trade_status is True:
        await message.answer(text=f'Сделка успешно отменена {symbol}')
    if not cancel_trade_status:
        await message.answer(text=f'Нет открытых сделок по паре {symbol}')

    await state.set_state(CommandState.state_none)


@dp.message(CommandState.cancel_add_orders)
async def state_cancel_add_orders(message: Message, state: FSMContext, symbol=None):
    symbol = symbol if symbol else message.text
    await message.answer(text=f'Отменяю добавочные ордера по паре {symbol}')
    cancel_add_orders_status = cancel_add_orders(symbol)
    if cancel_add_orders_status is True:
        await message.answer(text=f'Добавочные ордера по паре отменены {symbol}')
        return True
    if not cancel_add_orders_status:
        await message.answer(text=f'Нет открытых сделок по паре {symbol}')
    if 'ErrCode' in cancel_add_orders_status:
        await message.answer(text=cancel_add_orders_status)
        return cancel_add_orders_status
    await state.set_state(CommandState.state_none)


@dp.message(CommandState.create_trade)
async def state_create_trade(message: Message, state: FSMContext, trade=None):
    try:
        trade = eval(trade if trade else message.text)
        symbol = trade['symbol']
        await message.answer(text=f'Создаю трейд')
        create_trade_status = create_trade(trade)
        if create_trade_status is True:
            await message.answer(text=f'Трейд успешно создан {symbol}')
        else:
            await message.answer(text=f'Ошибка при создании трейда\n\n{create_trade_status}')
    except Exception as e:
        await message.answer(text=f'Ошибка при создании трейда {e}')
    await state.set_state(CommandState.state_none)


@dp.message(CommandState.set_sl_breakeven)
async def state_set_sl_breakeven(message: Message, state: FSMContext, symbol=None):
    symbol = symbol if symbol else message.text
    cancel_add_orders_status = await state_cancel_add_orders(message, state, symbol=symbol)
    if cancel_add_orders_status is True:
        await message.answer(text=f'Ставлю стоп-лосс в безубыток {symbol}')
        set_sl_breakeven_status = set_sl_breakeven(symbol)
    else:
        set_sl_breakeven_status = False
    if set_sl_breakeven_status is True:
        await message.answer(text=f'Стоп-лосс в безубыток установлен {symbol}')
    if 'ErrCode' in str(set_sl_breakeven_status):
        await message.answer(text=set_sl_breakeven_status)
    await state.set_state(CommandState.state_none)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    telegram_token = env('TELEGRAM_API_KEY')
    telegram_chat_id = env('TELEGRAM_CHAT_ID')
    bot = Bot(telegram_token, parse_mode=ParseMode.HTML)
    asyncio.run(main())
