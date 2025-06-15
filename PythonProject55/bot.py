from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import aiohttp

TOKEN = ''  # Replace with your actual bot token
API_URL = ''  # Replace with your actual API URL

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class RegForm(StatesGroup):
    fio = State()
    tel = State()
    tarif = State()
    summa = State()


@dp.message_handler(commands=['start'])
async def start_handler(msg: types.Message):
    await msg.answer("👋 Salom! Ro'yxatdan o'tish jarayonini boshlash uchun ism-familiyangizni kiriting:")
    await RegForm.fio.set()


@dp.message_handler(state=RegForm.fio)
async def get_fio(msg: types.Message, state: FSMContext):
    await state.update_data(fio=msg.text)
    await msg.answer("📱 Telefon raqamingizni kiriting:(+998 94-123-45-67)")
    await RegForm.tel.set()


@dp.message_handler(state=RegForm.tel)
async def get_tel(msg: types.Message, state: FSMContext):
    await state.update_data(tel=msg.text)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{API_URL}/tariflar/") as resp:
                if resp.status != 200:
                    await msg.answer("❌ Tariflarni olishda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
                    return
                tariflar = await resp.json()

                markup = InlineKeyboardMarkup()
                for tarif in tariflar:
                    markup.add(InlineKeyboardButton(
                        text=f"{tarif['nomi']} ({tarif['narxi']} so'm)",
                        callback_data=f"tarif_{tarif['id']}"  # Store the tariff ID
                    ))
                await msg.answer("📋 Iltimos, tarifni tanlang:", reply_markup=markup)

        except Exception as e:
            await msg.answer(f"❌ Xatolik: {e}")


@dp.callback_query_handler(lambda c: c.data.startswith('tarif_'), state=RegForm.tel)
async def tarif_tanlandi(call: types.CallbackQuery, state: FSMContext):
    tarif_id = int(call.data.split('_')[1])  # Extract tariff ID
    await state.update_data(tarif=tarif_id)  # Store tariff ID in state
    await call.message.answer("💵 To'lov miqdorini kiriting:")
    await RegForm.summa.set()
    await call.answer()


@dp.message_handler(state=RegForm.summa)
async def get_summa(msg: types.Message, state: FSMContext):
    await state.update_data(summa=msg.text)
    data = await state.get_data()

    abonent_data = {
        "fio": data['fio'],
        "telefon_raqami": data['tel'],
        "tarif": data['tarif']  # Send tariff ID
    }

    # Debugging: Print the data to check
    print(f"Sending abonent data: {abonent_data}")

    # Send data to backend API
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{API_URL}/abonentlar/", json=abonent_data) as resp:
                if resp.status == 201:
                    abonent = await resp.json()

                    tolov_data = {
                        "abonent": abonent["id"],
                        "summa": data['summa']
                    }

                    async with session.post(f"{API_URL}/tolovlar/", json=tolov_data) as tol:
                        if tol.status == 201:
                            await msg.answer(
                                "✅ Ro'yxatdan o'tish muvaffaqiyatli amalga oshirildi!\n\n"
                                "Yangi abonent tizimga qo'shildi va to'lov saqlandi.\n\n"
                                "Sizning abonent raqamingiz va tarifingiz:\n\n"
                                f"📱 Telefon: {data['tel']}\n"
                                f"💼 Tarif: {data['tarif']}\n"
                                f"💰 To'lov miqdori: {data['summa']} so'm"
                            )
                        else:
                            await msg.answer("❌ To'lovni saqlashda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
                else:
                    error_message = await resp.text()
                    await msg.answer(f"❌ Abonentni saqlashda xatolik yuz berdi. Serverdan javob: {error_message}")
        except Exception as e:
            await msg.answer(f"❌ Xatolik: {e}")

    await state.finish()
    await msg.answer("🎉 Ro'yxatdan o'tish jarayoni yakunlandi!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
