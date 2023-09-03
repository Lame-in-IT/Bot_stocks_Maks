import time
from token_bot import TOKIN
from aiogram import Bot, Dispatcher, executor, types
import markups as nav
from aiofiles import os
# from  time import sleep
# import aioschedule
# import asyncio

from connect_bd import *
from markups import *

bot = Bot(token=TOKIN, parse_mode="HTML")
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    if message.chat.type == 'private':
        hello_user = read_user(message["from"])
        await bot.send_message(message.from_user.id, f'{hello_user} {message["from"]["first_name"]}'.format(message.from_user), reply_markup=nav.mainMenu)
        await bot.send_message(message.from_user.id, f'Уважаемый(ая) {message["from"]["first_name"]}.\n'
                               'В этом разделе вам необходимо предоставить ваш API токен под название "Статистика".\n'
                               'Инструкция для получения токена от WB.\n'
                               'Авторизация осуществляется по токенам API, которые владелец личного кабинета (главный пользователь) самостоятельно генерирует в разделе Профиль --> Настройки --> Доступ к API.\n'
                               'Существует три типа токенов:\n\n'
                               '1. Стандартный. Используется для работы с методами из разделов: Цены, Промокоды и скидки, Контент, Marketplace, Рекомендации, Отзывы, Вопросы.\n'
                               '2. Статистика. Используется для работы с методами из раздела Статистика.\n'
                               '3. Реклама. Используется для работы с методами из раздела Реклама.\n'
                               'Обратите внимание, что токен отображается ТОЛЬКО в момент создания. Его надо сохранить, потому что больше его отобразить будет нельзя.'.format(message.from_user), reply_markup=nav.mainMenu)
        await bot.send_message(message.from_user.id, 'Когда у вас будет токен "Статистика" вам неоходимо прочитать оферту.\n\n'
                               'Если вы отправили нам свой токен доступа до прочтения оферты будет считаться что вы согласны с её условиями.'.format(message.from_user), reply_markup=nav.mainMenu)
        await bot.send_message(message.from_user.id, 'Добавлять контакты, можно только после согласия с договором оферты.'.format(message.from_user), reply_markup=nav.mainMenu)


@dp.message_handler(commands=["help"])
async def command_start(message: types.Message):
    if message.chat.type == 'private':
        text_str = "help"
        updata_chapter(message.from_user.id, text_str)
        await bot.send_message(message.from_user.id, f'{message["from"]["first_name"]} вам нужна помощь?'.format(message.from_user), reply_markup=nav.mainMenu)
        await bot.send_message(message.from_user.id, f'Уважаемый(ая) {message["from"]["first_name"]}.\n'
                               'В этом разделе вам необходимо предоставить ваш API токен под название "Статистика".\n'
                               'Инструкция для получения токена от WB.\n'
                               'Авторизация осуществляется по токенам API, которые владелец личного кабинета (главный пользователь) самостоятельно генерирует в разделе Профиль --> Настройки --> Доступ к API.\n'
                               'Существует три типа токенов:\n\n'
                               '1. Стандартный. Используется для работы с методами из разделов: Цены, Промокоды и скидки, Контент, Marketplace, Рекомендации, Отзывы, Вопросы.\n'
                               '2. Статистика. Используется для работы с методами из раздела Статистика.\n'
                               '3. Реклама. Используется для работы с методами из раздела Реклама.\n'
                               'Обратите внимание, что токен отображается ТОЛЬКО в момент создания. Его надо сохранить, потому что больше его отобразить будет нельзя.'.format(message.from_user), reply_markup=nav.mainMenu)
        await bot.send_message(message.from_user.id, 'Когда у вас будет токен "Статистика" вам неоходимо прочитать оферту.\n\n'
                               'Если вы отправили нам свой токен доступа до прочтения оферты будет считаться что вы согласны с её условиями.'.format(message.from_user), reply_markup=nav.mainMenu)
        await bot.send_message(message.from_user.id, 'Добавлять контакты, можно только после согласия с договором оферты.'.format(message.from_user), reply_markup=nav.mainMenu)

@dp.message_handler(text="Передать API")
async def api_ststistica_wb(message: types.Message):
    if message.chat.type == 'private':
        text_str = "Передать API"
        updata_chapter(message.from_user.id, text_str)
        await bot.send_message(message.from_user.id, '1. Скопируйте свой токен\n'
                               '2. Вставьте его в чат и отправьте боту.\n'
                               'После этого к вам будут приходить уведомления о товарах которые долго не продаются.\n\n'
                               'Также вы можете добавить контакты для рассылки данной информации нажатием кнопки \n\n'
                               '"Добавить контакты для рассылки"\n'
                               'Добавлять контакты, можно только после согласия с договором оферты.'.format(message.from_user), reply_markup=nav.mainMenu)

@dp.message_handler(text="Оферта по предоставлению токена")
async def api_oferta_wb(message: types.Message):
    if message.chat.type == 'private':
        text_str = "Оферта по предоставлению токена"
        updata_chapter(message.from_user.id, text_str)
        await bot.send_message(message.from_user.id, 'Текст оферты'.format(message.from_user), reply_markup=nav.ofertaMenu)
        
@dp.message_handler(text="Согласен")
async def api_yes_wb(message: types.Message):
    if message.chat.type == 'private':
        text_str = "Согласен"
        updata_chapter(message.from_user.id, text_str)
        await bot.send_message(message.from_user.id, 'Вы согласились с офертой'.format(message.from_user), reply_markup=nav.mainMenu)
        
@dp.message_handler(text="Главное меню")
async def api_main_wb(message: types.Message):
    if message.chat.type == 'private':
        text_str = "Главное меню"
        updata_chapter(message.from_user.id, text_str)
        await bot.send_message(message.from_user.id, 'Главное меню'.format(message.from_user), reply_markup=nav.mainMenu)
        
@dp.message_handler(content_types=types.ContentType.USER_SHARED)
async def on_user_shared(message: types.Message):
    req_cont = create_comtact(message.from_user.id, message.user_shared.user_id)
    await bot.send_message(message.from_user.id, f"{req_cont}.".format(message.from_user), reply_markup=nav.mainMenu)

@dp.message_handler(text="sales")
async def get_no_sales_wb(message: types.Message):
    get_satat = get_satat_wb() #https://www.wildberries.ru/catalog/{satat}/detail.aspx\n
    for item_id_user in get_satat[6]:
        try:
            for index, satat in enumerate(get_satat[0]):
                await bot.send_message(item_id_user,
                                    f'Артикул - {get_satat[1][index]}\n'
                                    f'̶̶🤑  Название - {get_satat[2][index]}\n'
                                    f'💰̶̶  На складах {get_satat[3][index]} шт.\n'
                                    f'💸̶̶  Продано за неделю {get_satat[4][index]}\n'
                                    f'💵  Ссылка: {get_satat[5][index]}'.format(message.from_user))
            await bot.send_message(message.from_user.id, "Успешная рассылка")
        except Exception as ex:
                logging.exception(ex)
                await message.answer("Возникла ошибка. Попробуйте еще раз сделать запрос.")
    await bot.send_message(message.from_user.id, "Рассылка завершина")
        
        
@dp.message_handler(text="stocks")
async def get_add_stocks_wb(message: types.Message):
    get_add_stocks = created_xlsx_user()
    for index_id, id in enumerate(get_add_stocks[0]):
        for item_cont in id:
            try:
                await bot.send_document(chat_id=item_cont, document=open(get_add_stocks[1][index_id], 'rb'))
                await bot.send_message(message.from_user.id, "Успешная рассылка")
            except Exception as ex:
                logging.exception(ex)
                await message.answer("Возникла ошибка. Попробуйте еще раз сделать запрос.")
        await os.remove(get_add_stocks[1][index_id])
        time.sleep(0.3)
    await bot.send_message(message.from_user.id, "Рассылка завершина")
        
        
# @dp.message_handler()    
# async def noon_print():
#     await bot.send_message(chat_id=1323522063, text='Главное меню 111111')
#     # await bot.send_message(chat_id=1464515838, text='Главное меню 111111')
    
# async def scheduler():
#     aioschedule.every().day.at("18:00").do(noon_print)
#     aioschedule.every().day.at("18:01").do(noon_print)
#     while True:
#         await aioschedule.run_pending()

# async def on_startup(_):
#     asyncio.create_task(scheduler())  


@dp.message_handler()
async def bot_message_help(message: types.Message): 
    chapter_user = get_chapter_user(message.from_user.id)
    if chapter_user == "start":
        await bot.send_message(message.from_user.id, f'Уважаемый(ая) {message["from"]["first_name"]}.\n'
                               'Если вам нужна помощь, выберите команду /help после нажатия кнопки "Меню"', reply_markup=nav.mainMenu)
    elif chapter_user == "help":
        await bot.send_message(message.from_user.id, f'Уважаемый(ая) {message["from"]["first_name"]}.\n'
                               'Если вам нужна помощь, выберите команду /help после нажатия кнопки "Меню"', reply_markup=nav.mainMenu)
    elif chapter_user == "Оферта по предоставлению токена":
        await bot.send_message(message.from_user.id, f'Уважаемый(ая) {message["from"]["first_name"]}.\n'
                               'Если вам нужна помощь, выберите команду /help после нажатия кнопки "Меню"', reply_markup=nav.mainMenu)
    elif chapter_user == "Согласен":
        await bot.send_message(message.from_user.id, f'Уважаемый(ая) {message["from"]["first_name"]}.\n'
                               'Если вам нужна помощь, выберите команду /help после нажатия кнопки "Меню"', reply_markup=nav.mainMenu)
    elif chapter_user == "Главное меню":
        await bot.send_message(message.from_user.id, f'Уважаемый(ая) {message["from"]["first_name"]}.\n'
                               'Если вам нужна помощь, выберите команду /help после нажатия кнопки "Меню"', reply_markup=nav.mainMenu)
    elif chapter_user == "Передать API":
        api = get_api_wb(message.text)
        if api == 200:
            req = created_user_api(message.from_user.id, message.text)
            if req == "Да":
                await bot.send_message(message.from_user.id, 'Ваш токен принят. Ждите рассылки о ваших заказах.', reply_markup=nav.mainMenu)
            elif req == "Нет":
                await bot.send_message(message.from_user.id, 'Произошла ошибка записи. Попробуйте ещё раз, если это сообщение повторится, обратитесь в администрацию бота.', reply_markup=nav.mainMenu)
        elif api == 400:
            await bot.send_message(message.from_user.id, 'Ошибка запроса', reply_markup=nav.mainMenu)
        elif api == 401:
            await bot.send_message(message.from_user.id, 'Ваш токен содержит ошибку. Проверьте соответствие токена.', reply_markup=nav.mainMenu)
        elif api == 408:
            await bot.send_message(message.from_user.id, 'Не известная ошибка запроса.', reply_markup=nav.mainMenu)
        elif api == 429:
            await bot.send_message(message.from_user.id, 'Слишком много запростов', reply_markup=nav.mainMenu)
        else:
            await bot.send_message(message.from_user.id, 'Ваш токен содержит ошибку. Проверьте соответствие токена.', reply_markup=nav.mainMenu)
    else:
        await bot.send_message(message.from_user.id, 'Я не понял что вы хотите. Повторите запрос.', reply_markup=nav.mainMenu)        
    
if __name__ == '__main__':
    # executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    executor.start_polling(dp, skip_updates=True)