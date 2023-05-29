from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pyrogram import Client




api_id = 23503205
api_hash = '5041f11524ad88a9e4c04f8d88e25a7d'
app = Client("my_account", api_id=api_id, api_hash=api_hash)
app.start()
members = []



from aiogram.utils import executor
import sqlite3 as sq

storage=MemoryStorage()

TOKEN='5539712264:AAFegV7fK-6-3QcWxpevB8p8GRBm-HhtSMk'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

async def main():
    await bot.set_webhook(url="https://optkz4.vercel.app/")

async def on_startup(_):

    print('Бот онлайн')
    sql_start()

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('/Автозапчасти')
b2 = KeyboardButton('/Техника')
b3 = KeyboardButton('/Хозтовары')
b4 = KeyboardButton('/IT')
b5 = KeyboardButton('/Одежда')
b6 = KeyboardButton('/Одежда(дешево)')
b7 = KeyboardButton('/Продукты')
b8 = KeyboardButton('/Строительство')
b9 = KeyboardButton('/Поиск')


kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(b1).add(b2).add(b3).add(b4).add(b5).add(b6).add(b7).add(b8).add(b9)

class Search(StatesGroup):
    search1 = State()


@dp.message_handler(commands={'start', 'help'})
async def command_start(message: types.message):

    async for member in app.get_chat_members(chat_id=-1001889000253):
        members.append(member.user.first_name)
    if message.from_user.first_name in members:
            await bot.send_message(message.from_user.id, 'Выберите категорию', reply_markup=kb_client)
    else:
            await bot.send_message(message.from_user.id, 'Подпишись на мой канал')




@dp.message_handler(commands=['Автозапчасти'])
async def avtozapchasti(message : types.message):
    await sql_avtozapchasti(message)

@dp.message_handler(commands={'Техника'})
async def technika(message : types.message):
    await sql_technika(message)

@dp.message_handler(commands={'Хозтовары'})
async def hoztovary(message : types.message):
    await sql_hoztovary(message)

@dp.message_handler(commands={'IT'})
async def it(message: types.message):
    await sql_it(message)

@dp.message_handler(commands={'Одежда'})
async def odezhda(message: types.message):
    await sql_odezhda(message)

@dp.message_handler(commands={'Одежда(дешево)'})
async def odezhdalow(message: types.message):
    await sql_odezhdalow(message)

@dp.message_handler(commands={'Продукты'})
async def product(message: types.message):
    await sql_product(message)

@dp.message_handler(commands={'Строительство'})
async def stroi(message: types.message):
    await sql_stroi(message)

@dp.message_handler(commands={'Поиск'})
async def search(message: types.message):
    await Search.search1.set()
    await message.reply("Что хотите найти?")


@dp.message_handler(state=Search.search1)
async def process_name(message: types.Message, state: FSMContext):

         async with state.proxy() as data:
            data = message.text

            async def sql_search(message):
                    row = f"Select name, adress, contact, site From poisk where search LIKE '%{data}%'"
                    keyw = f'Select distinct search From poisk'
                    rom = cur.execute(row).fetchall()
                    key =cur.execute(keyw).fetchall()

                    if rom == []:
                        for key1 in key:
                            await bot.send_message(message.from_user.id, f'{key1[0]}')

                    for ret in rom:
                        if ret is not None:
                            await bot.send_message(message.from_user.id, f'{ret[0]}, {ret[1]}, {ret[2]}, {ret[3]}')



                    base.commit()


         await state.finish()
         await sql_search(message)




def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands={'start', 'help'})
    dp.register_message_handler(avtozapchasti, commands={'Автозапчасти'})
    dp.register_message_handler(technika, commands={'Техника'})
    dp.register_message_handler(hoztovary, commands={'Хозтовары'})
    dp.register_message_handler(it, commands={'IT'})
    dp.register_message_handler(odezhda, commands={'Одежда'})
    dp.register_message_handler(odezhdalow, commands={'Одежда(дешево)'})
    dp.register_message_handler(product, commands={'Продукты'})
    dp.register_message_handler(stroi, commands={'Строительство'})
    dp.register_message_handler(search, commands={'Поиск'})

def sql_start():
    global base, cur
    base = sq.connect('avtozapchasti.db')
    cur = base.cursor()
    if base:
        print('data ok')


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO avtozapchasti VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()

async def sql_avtozapchasti(message):
    for ret in cur.execute('Select * From avtozapchasti').fetchall():
        await bot.send_message(message.from_user.id, f'{ret[0]}, {ret[1]}, {ret[2]}, {ret[3]}')
        base.commit()

async def sql_technika(message):
    for ret in cur.execute('Select * From technika').fetchall():
        await bot.send_message(message.from_user.id, f'{ret[0]}, {ret[1]}, {ret[2]}, {ret[3]}')
        base.commit()

async def sql_hoztovary(message):
    for ret in cur.execute('Select * From hoztovary').fetchall():
        await bot.send_message(message.from_user.id, f'{ret[0]}, {ret[1]}, {ret[2]}, {ret[3]}')
        base.commit()

async def sql_it(message):
    for ret in cur.execute('Select * From it').fetchall():
        await bot.send_message(message.from_user.id, f'{ret[0]}, {ret[1]}, {ret[2]}, {ret[3]}')
        base.commit()

async def sql_odezhda(message):
    for ret in cur.execute('Select * From odezhda').fetchall():
        await bot.send_message(message.from_user.id, f'{ret[0]}, {ret[1]}, {ret[2]}, {ret[3]}')
        base.commit()

async def sql_odezhdalow(message):
    for ret in cur.execute('Select * From odezhdalow').fetchall():
        await bot.send_message(message.from_user.id, f'{ret[0]}, {ret[1]}, {ret[2]}, {ret[3]}')
        base.commit()

async def sql_product(message):
    for ret in cur.execute('Select * From product').fetchall():
        await bot.send_message(message.from_user.id, f'{ret[0]}, {ret[1]}, {ret[2]}, {ret[3]}')
        base.commit()

async def sql_stroi(message):
    for ret in cur.execute('Select * From stroi').fetchall():
        await bot.send_message(message.from_user.id, f'{ret[0]}, {ret[1]}, {ret[2]}, {ret[3]}')
        base.commit()




executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
