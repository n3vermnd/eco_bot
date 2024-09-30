from aiogram import html

def tariff_choice_text():
    return '''
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

def first_login_text(full_name):
    return f'''
Привет, {html.bold(full_name)}!

Я помогу тебе подключить самый лучший VPN на рынке!

Плюсы:
- доступ ко всем сайтам
- самая высокая скорость
- его можно даже не выключать
'''

def main_menu_text(balance, tarif, full_name):
    return f'''
Привет, {html.bold(full_name)}!

{html.bold(f'Ваш баланс: {balance}₽')}
{tarif}

Вы можете получить свои конфигурации или купить новые, нажав на кнопку {html.bold("Мои Устройства")}
'''