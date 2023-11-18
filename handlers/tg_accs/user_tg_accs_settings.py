from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram import Router, F
from keyboards import kb_admin
from filters.is_admin import IsAdmin
from filters.known_user import KnownUser
from filters.sub_types import BasicSub
from aiogram.fsm.context import FSMContext
from states.states import EditAccInfo
from data.config_telethon_scheme import AuthTelethon
from database import db
from typing import List, Tuple
from data.config_telethon_scheme import TelethonConnect
from data import logger
router = Router()
router.message.filter(
    KnownUser()
)


async def get_info(accounts: list) -> List[Tuple[str]]:
    accs_info = []
    for session in accounts:
        try:
            sess = TelethonConnect(session)
            accs_info.append(await sess.get_info())
        except Exception as e:
            print(e)
    return accs_info


@router.callback_query(F.data == 'user_tg_accs_settings', ~BasicSub())
async def tg_accs_settings(callback: CallbackQuery):
    #await callback.message.delete()
    await callback.message.answer('<b>Настройки телеграм аккаунтов</b>\n\n'
                                  'Здесь можно настроить инфо аккаунта, такое как:\n'
                                  '<b>Имя, Фамилия, Bio, Аватар</b>\n\n'
                                  'Информация: /help_accs', reply_markup=kb_admin.users_tg_accs_btns(),
                                  parse_mode='HTML')

@router.callback_query(F.data == 'choose_acc_user')
async def choose_acc_user(callback: CallbackQuery, state: FSMContext):
    uid = callback.from_user.id
    operation = 'change_info'
    accounts = await db.get_user_accounts(uid)
    await callback.message.answer('Выберите аккаунт:', reply_markup=kb_admin.generate_accs_keyboard_users(accounts,
                                                                                                     operation))

@router.callback_query(F.data.startswith('account_change_info_'))
async def change_info_menu(callback: CallbackQuery, state: FSMContext):
    print(callback.data)
    account = callback.data.split('_')[-1]
    print(account)
    await callback.message.answer('<b>Что вы хотите изменить?</b>', reply_markup=kb_admin.edit_acc_info(account),
                                  parse_mode='HTML')

# name
@router.callback_query(F.data.startswith('acc_edit_name_'))
async def acc_change_name(callback: CallbackQuery, state: FSMContext):
    account = callback.data.split('_')[-1]
    await callback.message.answer('Введите новое имя:')
    await state.set_state(EditAccInfo.change_name)
    await state.update_data(account=account)

@router.message(EditAccInfo.change_name)
async def name_changed(message: Message, state: FSMContext):
    account = (await state.get_data())['account']
    session = AuthTelethon(account)
    res = await session.change_first_name(message.text)
    if res:
        await message.answer('Имя изменено')
        await message.answer('<b>Настройки телеграм аккаунтов</b>\n\n'
                              'Здесь можно настроить инфо аккаунта, такое как:\n'
                              '<b>Имя, Фамилия, Bio, Аватар</b>\n\n'
                              'Информация: /help_accs', reply_markup=kb_admin.users_tg_accs_btns(),
                              parse_mode='HTML')
    else:
        await message.answer('Произошла ошибка, попробуйте позже')
    await state.clear()


# surname
@router.callback_query(F.data.startswith('acc_edit_surname_'))
async def acc_edit_surname(callback: CallbackQuery, state: FSMContext):
    account = callback.data.split('_')[-1]
    await callback.message.answer('Введите новую фамилию:')
    await state.set_state(EditAccInfo.change_surname)
    await state.update_data(account=account)


@router.message(EditAccInfo.change_surname)
async def name_changed(message: Message, state: FSMContext):
    account = (await state.get_data())['account']
    session = AuthTelethon(account)
    res = await session.change_last_name(message.text)
    if res:
        await message.answer('Фамилия изменена')
        await message.answer('<b>Настройки телеграм аккаунтов</b>\n\n'
                              'Здесь можно настроить инфо аккаунта, такое как:\n'
                              '<b>Имя, Фамилия, Bio, Аватар</b>\n\n'
                              'Информация: /help_accs', reply_markup=kb_admin.users_tg_accs_btns(),
                              parse_mode='HTML')
    else:
        await message.answer('Произошла ошибка, попробуйте позже')
    await state.clear()


# bio
@router.callback_query(F.data.startswith('acc_edit_bio_'))
async def acc_edit_bio(callback: CallbackQuery, state: FSMContext):
    account = callback.data.split('_')[-1]
    await callback.message.answer('Введите новую информацию для размещения в био:')
    await state.set_state(EditAccInfo.change_bio)
    await state.update_data(account=account)


@router.message(EditAccInfo.change_bio)
async def name_changed(message: Message, state: FSMContext):
    account = (await state.get_data())['account']
    session = AuthTelethon(account)
    res = await session.change_bio(message.text)
    if res:
        await message.answer('Био изменено')
        await message.answer('<b>Настройки телеграм аккаунтов</b>\n\n'
                             'Здесь можно настроить инфо аккаунта, такое как:\n'
                             '<b>Имя, Фамилия, Bio, Аватар</b>\n\n'
                             'Информация: /help_accs', reply_markup=kb_admin.users_tg_accs_btns(),
                             parse_mode='HTML')
    else:
        await message.answer('Произошла ошибка, попробуйте позже')
    await state.clear()


@router.callback_query(F.data == 'users_accs_get_info')
async def user_accs_get_info(callback: CallbackQuery):
    await callback.message.answer('Запрашиваю информацию о подключенных аккаунтах...')
    uid = callback.from_user.id
    try:
        accounts = await db.get_user_accounts(uid)
        displayed_accounts = '\n'.join(accounts)
        if accounts:
            accs_info = await get_info(accounts)
            accounts_formatted = '\n\n'.join([
                f'<b>Тел:</b> {phone}'
                f'\n<b>ID:</b> {id}'
                f'\n<b>Имя:</b> {name}'
                f'\n<b>Фамилия:</b> {surname}'
                f'\n<b>Ник:</b> {username}'
                f'\n<b>Био:</b> {about}'
                f'\n<b>Ограничения:</b> {restricted}'
                for phone, id, name, surname, username, restricted, about in accs_info])

            await callback.message.answer(text=f'<b>Аккануты:</b>\n{displayed_accounts}\n\n<b>Инфо:</b>\n'
                                               f'{accounts_formatted}', parse_mode='HTML')

        else:
            await callback.message.answer('Нет подключенных аккаунтов.')
    except Exception as e:
        logger.error(e)


@router.callback_query(F.data.startswith('acc_edit_avatar_'))
async def acc_edit_avatar(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Функция временно не доступна.')
    await state.clear()


@router.callback_query(F.data == 'back_to_users_accs')
async def back_to_accs(callback: CallbackQuery, state: FSMContext):
    #await callback.message.delete()
    await callback.message.answer('Настройки телеграм аккаунтов:', reply_markup=kb_admin.users_tg_accs_btns())
    await state.clear()

@router.callback_query(F.data == 'user_tg_accs_settings')
async def tg_accs_settings(callback: CallbackQuery):
    #await callback.message.delete()
    await callback.message.answer('Извините, этот раздел не доступен для пользователей с бесплатной подпиской')

