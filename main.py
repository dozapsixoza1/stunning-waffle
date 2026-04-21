import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

BOT_TOKEN = "8506975337:AAHyVsAJcdKklAVwj9UppgJb4lzeyL3bqcw"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Каналы: первый — инвайт-ссылка (приват), остальные — username или ссылки
CHANNELS = [
    {"name": "Разгром Комьюнити", "link": "https://t.me/+FpLyK1VmsRNhNjYy", "id": "@неизвестно"},
    {"name": "MirrorWorld", "link": "https://t.me/+KZPRxxk2r8I5MTRi", "id": "@неизвестно"},
    {"name": "Fly Scam-Base", "link": "https://t.me/flysbase", "id": "@flysbase"},
    {"name": "Эриния Карающая", "link": "https://t.me/+Y_egu5MOnyliMDFi", "id": "@неизвестно"},
]

def subscription_keyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for ch in CHANNELS:
        kb.inline_keyboard.append([InlineKeyboardButton(text=ch["name"], url=ch["link"])])
    kb.inline_keyboard.append([InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_sub")])
    return kb

async def is_subscribed(user_id: int) -> tuple[bool, list]:
    not_subbed = []
    for ch in CHANNELS:
        # Для приватных каналов с инвайт-ссылками нельзя просто взять username.
        # Но можно получить chat_id через бота, если бот добавлен в канал.
        # Упростим: будем проверять только каналы, где есть username.
        if ch["id"] != "@неизвестно":
            try:
                member = await bot.get_chat_member(ch["id"], user_id)
                if member.status in ["left", "kicked"]:
                    not_subbed.append(ch["name"])
            except:
                not_subbed.append(ch["name"])
        else:
            # Приватный канал без username — проверка только через инвайт? Нельзя.
            # Считаем, что пользователь сам должен вступить по ссылке, а бот не может проверить.
            # Добавим заглушку: не проверяем приватные каналы.
            pass
    return len(not_subbed) == 0, not_subbed

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    text = (
        "БЕСПЛАТНЫЙ Б#ТН3Т\n\n"
        "🕵 Функции:\n"
        "「 Просто отправьте username для сн0са. (С НАЧАЛА ПОДПИШИТЕСЬ НА КАНАЛЫ.) \n\n"
        "🔻Подпишитесь на каналы ниже чтобы продолжить:"
    )
    await message.answer(text, reply_markup=subscription_keyboard())

@dp.callback_query(lambda c: c.data == "check_sub")
async def check_sub(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    ok, not_subbed = await is_subscribed(user_id)
    if not ok:
        text = f"❌ Ты не подписан на: {', '.join(not_subbed)}\n\nПодпишись и нажми снова."
        await callback.message.edit_text(text, reply_markup=subscription_keyboard())
    else:
        await callback.message.edit_text("✅ Доступ открыт. Теперь просто отправь мне username (например, @username).")
        # Здесь можно установить состояние, что пользователь прошёл проверку
        # и дальше обрабатывать обычные сообщения.

@dp.message()
async def handle_username(message: types.Message):
    # Проверим, что пользователь уже прошёл подписку.
    # Для простоты будем проверять каждый раз (можно кэшировать).
    ok, _ = await is_subscribed(message.from_user.id)
    if not ok:
        await message.answer("Сначала подпишись на каналы! Напиши /start")
        return
    username = message.text.strip()
    if username.startswith("@"):
        await message.answer(f"✅ Username {username} принят. Снос начат... (демо-режим)")
        # Здесь ты сам добавишь реальный снос, если надо.
    else:
        await message.answer("Отправь username в формате @username")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
