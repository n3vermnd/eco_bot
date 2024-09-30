import api
import asyncio
from config import TOKEN
import markups
import database
import strings

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

dp = Dispatcher()


@dp.message(CommandStart())
async def welcome(message: Message) -> None:
    full_name = message.from_user.full_name
     
    user_first = await database.new_user(message.from_user.id)
    
    check_devices = await database.check_devices(message.from_user.id)
    print(check_devices)
    

    balance = await database.get_balance(message.from_user.id)
    
    tarif = await database.price_month(message.from_user.id)

    if user_first:
        await message.answer(strings.first_login_text(full_name), reply_markup=markups.first_login)
        print("LOG: main.py > Пользователь НЕ зарегистрирован")
        await database.register_user(message.from_user.id)
    else:
        if check_devices:
            await message.answer(strings.main_menu_text(balance, tarif, full_name), reply_markup=markups.dashboard)
            print("LOG: main.py > Пользователь зарегистрирован, устройства есть")
        else:
            await message.answer(strings.first_login_text(full_name), reply_markup=markups.first_login)
            print("LOG: main.py > Пользователь зарегистрирован, устройств нет")        
    

@dp.callback_query()
async def menu(callback_query: CallbackQuery):
    callback_args = callback_query.data
    if callback_args == "back_to_welcome":
        await callback_query.message.edit_text(strings.first_login_text(callback_query.message.from_user.full_name), reply_markup=markups.first_login)
    elif callback_args == "first_login":
        await callback_query.message.edit_text(strings.tariff_choice_text(), reply_markup=markups.tarif_choice)
    elif callback_args == "topup_balance":
        await callback_query.message.edit_text("Тут будет пополнение баланса")
    elif callback_args == "dashboard":
        await callback_query.message.edit_text("Тут будет дэшборд со всеми конфигами")
    elif callback_args == "referal_dashboard":
        await callback_query.message.edit_text("Тут будет реферальная дэшборда со всеми рефералами")
    elif callback_args == "instruction":
        await callback_query.message.edit_text("Тут будет инструкция")
    elif callback_args in ["st_choice", "ft_choice"]:  # Проверяем выбор тарифа
        await tariff_handler(callback_query)
    elif callback_args.startswith("payment"):
        await payments(callback_query)

    await callback_query.answer()  # Подтверждаем обработку

async def tariff_handler(callback_query: CallbackQuery):
    callback_args = callback_query.data
    if callback_args == "st_choice":
        await callback_query.message.edit_text("Выбран: Стандарт", reply_markup=markups.st_choice)
    elif callback_args == "ft_choice":
        await callback_query.message.edit_text("Выбран: Ускоренный", reply_markup=markups.ft_choice)

async def payments(callback_query: CallbackQuery):
    callback_args = callback_query.data.split('_')
    sub_period = callback_args[1]
    tariff_type = callback_args[2]
    
    print(f'Payment Type: {sub_period}')
    print(f'Tarif Type: {tariff_type}')
    sublink = await api.addClient(tariff_type, sub_period, callback_query.from_user.id)
    await callback_query.message.edit_text(f"Ваша ссылка для входа в VPN: \n<code>{sublink}</code>")

    
async def main() -> None:
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await database.recreate_db()
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())