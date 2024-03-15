from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_action import db
from filters.sub_types import BasicSub
from keyboards import kb_admin

router = Router()
router.message.filter(
)





@router.callback_query(F.data == 'pro_settings', ~BasicSub())
async def process_pro_settings(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    uid = callback.from_user.id
    groups = await db.db_get_all_telegram_channels(uid)
    grp_dict = {}
    for grp in groups:
        triggers = await db.db_get_triggers_for_group(grp)
        promts = await db.db_get_promts_for_group(grp)
        grp_dict[grp] = ['🟢' if triggers else '🔴', '🟢' if promts else '🔴']

    string = ''
    for k, v in grp_dict.items():
        string += '\n' + k + f'\n<b>Триггеры:</b> {v[0]} <b>Промт:</b> {v[1]}'
    channels = '\n'.join(await db.db_get_all_telegram_channels(uid))
    await callback.message.answer(text=f'<b>Pro Настройки</b>\n\n'
                                       f'<b>Каналы:</b>\n'
                                       f'{string}\n\n'
                                       f'Информация: /help_promts',
                                  reply_markup=kb_admin.pro_settings_btns(),
                                  parse_mode='HTML')

@router.callback_query(F.data == 'pro_settings')
async def process_pro_settings_basic(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer('Извините, этот раздел не доступен для пользователей с бесплатной подпиской')
