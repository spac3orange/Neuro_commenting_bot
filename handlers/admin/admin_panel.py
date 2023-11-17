from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from data import logger
from aiogram import Router, F
from keyboards import kb_admin
from filters.is_admin import IsAdmin
from utils.scheduler import monitor
from database import db
router = Router()
router.message.filter(
    IsAdmin(F)
)


@router.callback_query(F.data == 'admin_panel', IsAdmin(F))
async def process_admin_panel(callback: CallbackQuery):
    status = await monitor.get_status()
    today_users = await db.db_get_users_today()
    await callback.message.answer(f'<b>Панель Администратора</b>\n\n'
                                  f'<b>Глобальный Мониторинг:</b> {"Запущен 🟢" if status else "Выключен 🔴"}\n'
                                  f'<b>Пользователей сегодня:</b> {len(today_users)}\n',

                                  reply_markup=kb_admin.admin_panel(),
                                  parse_mode='HTML')



