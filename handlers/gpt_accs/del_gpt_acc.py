from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state, State, StatesGroup
from keyboards import tg_accs_btns, generate_gpt_accs_keyboard, gpt_accs_btns
from data.logger import logger
from aiogram.fsm.context import FSMContext
from states.states import DelTgAccState
from database.db_action import db_remove_tg_account, db_get_all_gpt_accounts, db_remove_gpt_account
router = Router()


@router.callback_query(F.data == 'gpt_accs_del')
async def del_gpt_acc(callback: CallbackQuery, state: FSMContext):
    api_keys = await db_get_all_gpt_accounts()
    #await callback.message.delete()
    await callback.message.answer('Выберите ключ, который будет удален: ',
                                  reply_markup=generate_gpt_accs_keyboard(api_keys))


@router.callback_query(F.data.startswith('gpt_del_'))
async def gpt_acc_deleted(callback: CallbackQuery, state: FSMContext):
    gpt_key = callback.data.split('_')[-1]
    await db_remove_gpt_account(gpt_key)
    #await message.delete()
    logger.info('gpt account deleted from db')
    await callback.message.answer('Аккаунт удален из базы данных')
    await callback.message.answer('Настройки ChatGPT аккаунтов:', reply_markup=gpt_accs_btns())
