from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButtonRequestUser

# --- Main Menu ---
btnapisogl = KeyboardButton('Оферта по предоставлению токена', resize_keyboard=True) # type: ignore
btnapi = KeyboardButton('Передать API', resize_keyboard=True) # type: ignore
request_button = KeyboardButton(text="Добавить контакты для рассылки", request_user=KeyboardButtonRequestUser(request_id=1))
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnapisogl).add(btnapi).add(request_button) # type: ignore

# --- Oferta Menu ---
apisogl = KeyboardButton('Согласен', resize_keyboard=True) # type: ignore
btnback = KeyboardButton('Главное меню', resize_keyboard=True) # type: ignore
ofertaMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(apisogl).add(btnback) # type: ignore