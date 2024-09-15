import api
import asyncio
from config import TOKEN
import markups
import database

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

dp = Dispatcher()

@dp.message(CommandStart())
async def welcome(message: Message) -> None:
     
    user_first = await database.new_user(message.from_user.id)
    
    balance = await database.get_balance(message.from_user.id)
    
    tarif = await database.price_month(message.from_user.id)
     
    welcome_text = f'''
Привет, {html.bold(message.from_user.full_name)}!

Я помогу тебе подключить самый лучший VPN на рынке!

Плюсы:
- доступ ко всем сайтам
- самая высокая скорость
- его можно даже не выключать
'''
    user_text = f'''
Привет, {html.bold(message.from_user.full_name)}!

{html.bold(f'Ваш баланс: {balance}₽')}
{tarif}

Вы можете получить свои конфигурации или купить новые, нажав на кнопку {html.bold("Мои Устройства")}
'''

    if user_first:
        await message.answer(welcome_text, reply_markup=markups.welcome_connect)
        print("LOG: main.py > Пользователь НЕ зарегистрирован")
        await database.register_user(message.from_user.id)
    else:
        await message.answer(user_text, reply_markup=markups.dashboard)
        print("LOG: main.py > Пользователь зарегистрирован")
    
    

    
@dp.callback_query()
async def callback(callback_query: CallbackQuery):
    callback_args = callback_query.data
    if callback_args == "dashboard":
        await callback_query.message.edit_text("тут будет личный кабинет(зареган)")
    elif callback_args == "welcome_connect":
        welcome_connect_text = '''
Выберите тариф:

🌐 Стандартный － для тех, кто хочет стабильный VPN:
1. 📺 Работает YouTube
2. 🇷🇺 Российские сайты не выдают ошибок
3. 🔒 Один из самых надежных протоколов, его не заблокируют
4. ⚡️ Задержка незначительна

🚀 Ускоренный － для тех, кто против цензуры:
1. 🎵 Работает ТикТок
2. 🌍 Сервер находится в стране с самым маленьким пингом
3. ⚡️ Задержки почти нет
4. 🛡️ Самый безопасный протокол VPN на данный момент
'''
        await callback_query.message.edit_text(welcome_connect_text,reply_markup=markups.tarif_choice)
    elif callback_args == "welcome_menu":
        welcome_text = f'''
Привет, {html.bold(callback_query.from_user.full_name)}!

Я помогу тебе подключить самый лучший VPN на рынке!

Плюсы:
- доступ ко всем сайтам
- самая высокая скорость
- его можно даже не выключать
'''
        await callback_query.message.edit_text(welcome_text, reply_markup=markups.welcome_connect)
    elif callback_args == "st_choice":
        await callback_query.message.edit_text("Выбран: Стандарт", reply_markup=markups.st_choice)
    elif callback_args == "ft_choice":
        await callback_query.message.edit_text("Выбран: Ускоренный", reply_markup=markups.ft_choice)
    
    
    elif callback_args.startswith("payment"):
        args = callback_args.split('_')
        sub_period = args[1]
        tarif_type = args[2]
        
        print(f"Payment Type: {sub_period}")
        print(f"Tarif Type: {tarif_type}")
        sublink = await api.addClient(tarif_type, sub_period, callback_query.from_user.id)
        await callback_query.message.edit_text(f"Ваша ссылка для входа в VPN: \n<code>{sublink}</code>")
        
        
    await callback_query.answer()    
    


    
async def main() -> None:
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await database.recreate_db()
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())