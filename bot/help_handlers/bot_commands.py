from datetime import datetime
from aiogram.filters import Command
from aiogram import types, F, Router
from typing import Union
from aiogram.fsm.context import FSMContext
from bot.keyboards.kbs import kbs_menu

commands_router = Router()


@commands_router.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    time_now = datetime.now().strftime('%H:%M, %d-%m-%Y')
    kb = types.InlineKeyboardMarkup(inline_keyboard=kbs_menu())
    await message.answer(f"Привет!\nСейчас <b>{time_now}</b>\nВыбери, что будем делать:",
                         reply_markup=kb,
                         )


@commands_router.callback_query(F.data.lower() == "menu")
async def cmd_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    time_now = datetime.now().strftime('%H:%M, %d-%m-%Y')
    kb = types.InlineKeyboardMarkup(inline_keyboard=kbs_menu())
    await callback.message.answer(f"Привет!\nСейчас <b>{time_now}</b>\nВыбери, что будем делать:",
                                  reply_markup=kb
                                  )


@commands_router.message(Command("show_cmds"))
@commands_router.callback_query(F.data.lower() == 'show_cmds')
async def show_all_cmds(event: Union[types.Message, types.CallbackQuery], state: FSMContext):
    await state.clear()
    cmds_dict = {
        '/start': 'Меню. ',
        '/show_cmds': 'Показать все команды.',
    }
    result = []
    for command, description in cmds_dict.items():
        result.append(f'{command} : {description}')
    if isinstance(event, types.Message):
        await event.answer('\n'.join(result))
    elif isinstance(event, types.CallbackQuery):
        await event.message.answer('\n'.join(result))

