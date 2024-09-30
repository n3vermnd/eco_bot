from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


first_login = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Подключить", callback_data="first_login")]
])

dashboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Пополнить баланс", callback_data="topup_balance")],
    [InlineKeyboardButton(text="✅ Мои устройства", callback_data="dashboard")],
    [InlineKeyboardButton(text="Поделиться с другом", callback_data="referal_dashboard"),
     InlineKeyboardButton(text="Инструкция", callback_data="instruction")]
])


tarif_choice = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Стандартный", callback_data="st_choice"),
    InlineKeyboardButton(text="Ускоренный", callback_data="ft_choice")],
     [InlineKeyboardButton(text="Назад", callback_data="back_to_welcome")]
])


st_choice = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Месяц | 150₽", callback_data="payment_m_st")],
    [InlineKeyboardButton(text="Полгода | 855₽(-5%)", callback_data="payment_6m_st"),
    InlineKeyboardButton(text="Год | 1 530₽(-15%)", callback_data="payment_y_st")],
    [InlineKeyboardButton(text="Навсегда | 10 000₽", callback_data="payment_lt_st")],
    [InlineKeyboardButton(text="Назад", callback_data="first_login")]
    
])

ft_choice = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Месяц | 300₽", callback_data="payment_m_ft")],
    [InlineKeyboardButton(text="Полгода | 1 710₽(-5%)", callback_data="payment_6m_ft"),
     InlineKeyboardButton(text="Год | 3 060₽(-15%)", callback_data="payment_y_ft")],
    [InlineKeyboardButton(text="Навсегда | 20 000₽", callback_data="payment_lt_ft")],
    [InlineKeyboardButton(text="Назад", callback_data="first_login")]
])