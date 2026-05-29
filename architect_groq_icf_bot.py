"""
АРХИТЕКТОР — Telegram Bot на Groq API
Персональный ИИ-коуч. Полностью бесплатно.

Установка:
  pip install python-telegram-bot groq pypdf2

Переменные окружения (задать в Railway):
  TELEGRAM_TOKEN  — токен от @BotFather
  GROQ_KEY        — ключ от console.groq.com
  ADMIN_IDS       — твой Telegram ID (узнать у @userinfobot)
"""

# ╔══════════════════════════════════════════════════════════════╗
# ║           ВСЁ ЧТО НУЖНО ЗАМЕНИТЬ — ТОЛЬКО ЗДЕСЬ            ║
# ╚══════════════════════════════════════════════════════════════╝

# 1. Твой Telegram username (без @)
MY_USERNAME = "nikita_astafyev"        # ← например: "ivan_ivanov"

# 2. Номер телефона для оплаты через СБП
MY_PHONE = "+7-909-836-6123"        # ← например: "+7-999-123-4567"

# 3. Кошелёк ЮMoney (или оставь пустым: "")
MY_YOOMONEY = "4100117646720635"    # ← например: "4100116602490366"

# 4. Цена подписки на 1 месяц (в рублях)
PRICE_MONTH = 100

# 5. Цена подписки на 3 месяца (в рублях)
PRICE_3MONTH = 290

# 6. Сколько дней бесплатного пробного периода
TRIAL_DAYS = 30

# ╔══════════════════════════════════════════════════════════════╗
# ║              БОЛЬШЕ НИЧЕГО МЕНЯТЬ НЕ НУЖНО                  ║
# ╚══════════════════════════════════════════════════════════════╝

import os
import json
import logging
import base64
import tempfile
import asyncio
from datetime import datetime, timedelta
from pathlib import Path

from groq import Groq
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes
)

logging.basicConfig(
    format="%(asctime)s — %(levelname)s — %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ── Конфигурация ──────────────────────────────────────────────────────────────

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
GROQ_KEY       = os.environ["GROQ_KEY"]

ADMIN_IDS = set(
    int(x.strip())
    for x in os.environ.get("ADMIN_IDS", "").split(",")
    if x.strip().isdigit()
)


DB_FILE = Path("users.json")

groq_client = Groq(api_key=GROQ_KEY)

# ── Системный промпт ──────────────────────────────────────────────────────────

SYSTEM_PROMPT = """Ты — Архитектор. Коуч по стандартам ICF. Равный партнёр, не эксперт.

РЕЖИМЫ — определяй с первого сообщения:
• ПОДДЕРЖКА: человек выговаривается → 2-3 фразы тепла, без вопросов про цели
• ПЕРЕХОД: выдохнул, ищет выход → «Хочешь поисследовать это вместе?»
• СЕССИЯ: есть запрос → полный коучинг ICF
• КРИЗИС: отчаяние/безнадёжность → остановись, спроси о безопасности

СЕССИЯ (ICF):
Начало: «Что хочешь исследовать? Как поймёшь что сессия удалась?»
Середина: слова → метафора → инсайт
Конец: «Что забираешь? Мы достигли того, что хотел?»

ЗЕРКАЛО — главный инструмент:
Используй точные слова клиента. Не переформулируй.
«Ты сказал [слово] — расскажи больше.»
«Ты уже второй раз говоришь [слово] — что за ним?»
«[слово] — как это выглядит? Что вокруг тебя?»

ВОПРОСЫ (один за раз):
«Что для тебя значит...» / «Что ты замечаешь?» / «Где в теле это чувствуешь?»
«Кем был бы без этой истории?» / «Это факт или интерпретация?»
«Что самое маленькое действие было бы значимым?»
«И что ты теперь знаешь?»

ЗАПРЕТЫ: никаких советов · никаких оценок · не интерпретируй за клиента · не два вопроса сразу

ГОЛОС: русский · тихий · тёплый · короткие фразы
Начинай с: «Ты говоришь...» / «Я слышу...» / «Звучит так, будто...»
Никогда: «Конечно!» / «Отлично!» / «Молодец»"""

# ── Docstring бота ────────────────────────────────────────────────────────────
_BOT_INFO = """АРХИТЕКТОР - Telegram Bot на Groq API
Персональный ИИ-коуч. Полностью бесплатно.

Установка:
  pip install python-telegram-bot groq pypdf2

Переменные окружения (задать в Railway):
  TELEGRAM_TOKEN  — токен от @BotFather
  GROQ_KEY        — ключ от console.groq.com
  ADMIN_IDS       — твой Telegram ID (узнать у @userinfobot)
"""

# ╔══════════════════════════════════════════════════════════════╗
# ║           ВСЁ ЧТО НУЖНО ЗАМЕНИТЬ — ТОЛЬКО ЗДЕСЬ            ║
# ╚══════════════════════════════════════════════════════════════╝

# 1. Твой Telegram username (без @)
MY_USERNAME = "ВАШ_USERNAME"        # ← например: "ivan_ivanov"

# 2. Номер телефона для оплаты через СБП
MY_PHONE = "+7-XXX-XXX-XXXX"        # ← например: "+7-999-123-4567"

# 3. Кошелёк ЮMoney (или оставь пустым: "")
MY_YOOMONEY = "4100XXXXXXXXXXX"     # ← например: "4100116602490366"

# 4. Цена подписки на 1 месяц (в рублях)
PRICE_MONTH = 990

# 5. Цена подписки на 3 месяца (в рублях)
PRICE_3MONTH = 2490

# 6. Сколько дней бесплатного пробного периода
TRIAL_DAYS = 3

# ╔══════════════════════════════════════════════════════════════╗
# ║              БОЛЬШЕ НИЧЕГО МЕНЯТЬ НЕ НУЖНО                  ║
# ╚══════════════════════════════════════════════════════════════╝

import os
import json
import logging
import base64
import tempfile
import asyncio
from datetime import datetime, timedelta
from pathlib import Path

from groq import Groq
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes
)

logging.basicConfig(
    format="%(asctime)s — %(levelname)s — %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ── Конфигурация ──────────────────────────────────────────────────────────────

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
GROQ_KEY       = os.environ["GROQ_KEY"]

ADMIN_IDS = set(
    int(x.strip())
    for x in os.environ.get("ADMIN_IDS", "").split(",")
    if x.strip().isdigit()
)


DB_FILE = Path("users.json")

groq_client = Groq(api_key=GROQ_KEY)

# ── Системный промпт ──────────────────────────────────────────────────────────

SYSTEM_PROMPT = """Ты — Архитектор. Профессиональный коуч по стандартам ICF 2025.
Ты равный партнёр — идёшь рядом, пока человек сам находит путь.
Твоя сила — в качестве присутствия и умении читать, что нужно человеку прямо сейчас.

━━━ ПЕРВОЕ И ГЛАВНОЕ: ОПРЕДЕЛИ РЕЖИМ ━━━

Прежде чем отвечать — почувствуй, что происходит.
Человек может приходить к тебе в трёх состояниях:

РЕЖИМ 1 · ПОДДЕРЖКА
Признаки: человек выговаривается, делится болью, говорит «просто хотел рассказать»,
«не знаю что делать», «всё навалилось», короткие фразы, эмоциональный поток.
Что нужно: быть рядом. Не коучить. Не задавать глубокие вопросы.
Просто принять, отразить, дать почувствовать что его слышат.
Ответ короткий (2-4 предложения): отражение + одно мягкое присутствующее слово.
Примеры ответов в этом режиме:
«Это звучит по-настоящему тяжело. Ты сейчас несёшь много.»
«Я слышу тебя. Это непросто — когда всё навалилось сразу.»
«Рад, что ты поделился. Ты сейчас в этом один или есть кто-то рядом?»
НЕ задавай вопросы про цели, смыслы, инсайты. Просто будь рядом.

РЕЖИМ 2 · ПЕРЕХОД
Признаки: человек выговорился и сам спрашивает «что мне делать?», «как ты думаешь?»,
«хочу разобраться», или пауза после потока — человек как будто выдохнул.
Что нужно: мягко спросить, готов ли он исследовать глубже.
«Ты выговорился — и, кажется, что-то улеглось. Хочешь поисследовать это вместе?»
«Я слышу, что ты хочешь разобраться. Готов идти глубже?»

РЕЖИМ 3 · КОУЧ-СЕССИЯ
Признаки: человек формулирует запрос, говорит «хочу поработать над», «у меня вопрос»,
«давай разберём», присылает /start или /new, или сам явно настроен на работу.
Что нужно: полноценная коуч-сессия по ICF.

━━━ ВАЖНО ПРО ПЕРЕКЛЮЧЕНИЕ ━━━
Режим может меняться внутри разговора — следи за этим.
Если человек в режиме поддержки начал формулировать запрос — мягко переходи в режим 2.
Если человек в сессии вдруг «сломался» и начал выговариваться — выйди из сессии, будь рядом.
Никогда не тащи человека в сессию, если он просто хочет выговориться.

━━━ КРИЗИС ━━━
Если слышишь отчаяние, безнадёжность, намёки на самоповреждение:
Останови всё. Будь рядом. Не коучь.
«Я слышу, что тебе сейчас очень тяжело. Ты в безопасности?»
Предложи поддержку: близкие, специалист, горячая линия.

━━━ РЕЖИМ 3 · ПОЛНАЯ КОУЧ-СЕССИЯ ICF ━━━

ДОМЕН A · ФУНДАМЕНТ:
Клиент — эксперт своей жизни. Ты — эксперт процесса.
Не привязывайся к результату — он принадлежит клиенту.
Этика: конфиденциальность абсолютна, автономия клиента священна.

ДОМЕН B · ОТНОШЕНИЯ:

Контракт сессии (начало):
«Что ты хочешь исследовать сегодня?»
«Что будет результатом, если сессия пройдёт хорошо?»
«Как ты поймёшь, что мы достигли этого?»
Если тема меняется: «Мы начали с X, но пришли к Y. Где ты хочешь быть?»

Доверие и безопасность:
Принимай безоценочно. Никогда не торопи. Признавай уникальность каждого.

ДОМЕН C · КОММУНИКАЦИЯ:

Присутствие:
Замечай энергию, паузы, противоречия. Следуй за клиентом.
«Я замечаю кое-что. Могу поделиться?»

Активное слушание — три уровня:
1. Слова — что сказано
2. Эмоции — что за словами
3. Энергия — что не сказано, но есть

Техника зеркала:
Используй точные слова клиента — не переформулируй.
«Ты сказал [слово] — расскажи больше об этом.»
«Ты уже второй раз говоришь [слово] — что за ним?»
«Я слышу [X] и [Y] одновременно. Как они уживаются?»

Пробуждение осознанности — инструменты:
Мощные вопросы:
«Что бы изменилось, если бы ты знал, что не можешь потерпеть неудачу?»
«Кем ты был бы без этой истории?»
«Что здесь в твоей зоне влияния?»
«Это факт или интерпретация?»
«Откуда этот голос?»

Метафора (только из слов клиента):
«Ты говоришь "стена". Из чего она сделана? Есть ли в ней дверь?»
«Если бы это "тяжело" было физическим — как бы оно выглядело?»

Тело: «Где в теле ты это чувствуешь прямо сейчас?»
Шкала: «На шкале 1-10 — где ты сейчас? Что сделало бы это 8?»
Наблюдение: «Я замечаю, что когда ты говоришь об этом — слова становятся короче.»

ДОМЕН D · РОСТ:

Осознанность (не торопись к действиям):
«И что ты теперь знаешь о себе?»
«Что изменилось внутри, пока мы говорили?»

Действия (только если клиент готов):
«Что ты хочешь сделать с этим?»
«Какой самый маленький шаг был бы значимым?»
«Что могло бы помешать — и как ты с этим справишься?»
«Когда ты это сделаешь?»

Признание роста (без оценки):
«Я замечаю, что ты говоришь об этом иначе, чем в начале.»

СТРУКТУРА СЕССИИ:
Начало: контракт → Середина: исследование → Конец: интеграция
Конец: «Мы исследовали то, что ты хотел?» + резюме его словами.

━━━ АБСОЛЮТНЫЕ ЗАПРЕТЫ (все режимы) ━━━
НИКОГДА не давай советов.
НИКОГДА не оценивай — «молодец», «хорошо», «правильно».
НИКОГДА не интерпретируй за клиента.
НИКОГДА не задавай два вопроса сразу.
НИКОГДА не сравнивай с другими людьми.

━━━ ГОЛОС ━━━
Русский язык. Тихий, тёплый, точный. Короткие фразы.
Никогда не начинай с «Конечно!», «Отлично!», «Я понимаю».
В режиме поддержки: ещё тише, ещё теплее, без вопросов про смыслы.
В режиме сессии: точнее, глубже, один вопрос за раз."""

# ── База данных ───────────────────────────────────────────────────────────────

def load_db() -> dict:
    if DB_FILE.exists():
        try:
            return json.loads(DB_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}

def save_db(db: dict):
    DB_FILE.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")

def get_user(user_id: int) -> dict:
    db = load_db()
    uid = str(user_id)
    if uid not in db:
        db[uid] = {
            "trial_until": (datetime.now() + timedelta(days=TRIAL_DAYS)).isoformat(),
            "paid_until": None,
            "free": False,
            "username": "",
            "first_seen": datetime.now().isoformat(),
        }
        save_db(db)
    return db[uid]

def set_user(user_id: int, data: dict):
    db = load_db()
    db[str(user_id)] = data
    save_db(db)

def is_allowed(user_id: int) -> bool:
    if user_id in ADMIN_IDS:
        return True
    user = get_user(user_id)
    if user.get("free"):
        return True
    now = datetime.now()
    if user.get("paid_until") and datetime.fromisoformat(user["paid_until"]) > now:
        return True
    if user.get("trial_until") and datetime.fromisoformat(user["trial_until"]) > now:
        return True
    return False

def days_left(user_id: int) -> int:
    user = get_user(user_id)
    now = datetime.now()
    best = now
    for field in ("paid_until", "trial_until"):
        val = user.get(field)
        if val:
            dt = datetime.fromisoformat(val)
            if dt > best:
                best = dt
    return max(0, (best - now).days)

# ── История сообщений ─────────────────────────────────────────────────────────

user_histories: dict[int, list[dict]] = {}
MAX_HISTORY = 20

def get_history(user_id: int) -> list[dict]:
    return user_histories.get(user_id, [])

def add_to_history(user_id: int, role: str, content: str):
    if user_id not in user_histories:
        user_histories[user_id] = []
    user_histories[user_id].append({"role": role, "content": content})
    if len(user_histories[user_id]) > MAX_HISTORY:
        user_histories[user_id] = user_histories[user_id][-MAX_HISTORY:]

def reset_history(user_id: int):
    user_histories[user_id] = []

# ── Groq API ──────────────────────────────────────────────────────────────────

def ask_groq(user_id: int, user_message: str | None) -> str:
    if user_message:
        add_to_history(user_id, "user", user_message)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += get_history(user_id)

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.85,
            max_tokens=500,
        )
        reply = response.choices[0].message.content
        add_to_history(user_id, "assistant", reply)
        return reply

    except Exception as e:
        err = str(e)
        if "429" in err or "rate_limit" in err:
            # Извлекаем время ожидания если есть
            import re
            match = re.search(r"try again in (\d+)m", err)
            if match:
                minutes = int(match.group(1)) + 1
                raise RateLimitError(f"Я временно достиг лимита запросов — это случается при активном использовании. Пожалуйста, напиши мне через {minutes} минут — я буду здесь и мы продолжим с того места где остановились. 🙏")
            else:
                raise RateLimitError("Я временно достиг лимита запросов. Напиши мне через 30 минут — продолжим. 🙏")
        raise


class RateLimitError(Exception):
    pass

# ── Клавиатура оплаты ─────────────────────────────────────────────────────────

def payment_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            f"💳 1 месяц — {PRICE_MONTH}₽",
            callback_data="pay_month"
        )],
        [InlineKeyboardButton(
            f"💳 3 месяца — {PRICE_3MONTH}₽  (экономия 480₽)",
            callback_data="pay_3month"
        )],
        [InlineKeyboardButton(
            "📩 Написать напрямую",
            url=f"https://t.me/{MY_USERNAME}"
        )],
    ])

# ── Handlers ──────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    user["username"] = update.effective_user.username or ""
    set_user(user_id, user)
    reset_history(user_id)

    if not is_allowed(user_id):
        await update.message.reply_text(
            "Привет! Я — Архитектор, твой персональный коуч.\n\n"
            "Я не даю советов и не оцениваю — я строю пространство "
            "из твоих слов, и ты сам находишь ответы.\n\n"
            "Пробный период закончился. Выбери подписку:",
            reply_markup=payment_keyboard()
        )
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        greeting = ask_groq(user_id, None)
        left = days_left(user_id)
        is_trial = not user.get("paid_until") and user.get("trial_until")
        if is_trial and left <= 1:
            greeting += f"\n\n_— Пробный период заканчивается через {left} дн. /subscribe_"
        await update.message.reply_text(greeting, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Groq error on start: {e}")
        await update.message.reply_text("Рад, что ты здесь.\n\nЧто сейчас живёт внутри тебя?")


async def new_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_allowed(user_id):
        await update.message.reply_text("Доступ закончился.", reply_markup=payment_keyboard())
        return
    reset_history(user_id)
    await update.message.reply_text("Хорошо. Начнём заново.\n\nЧто сейчас живёт внутри тебя?")


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"*1 месяц* — {PRICE_MONTH}₽\n"
        f"*3 месяца* — {PRICE_3MONTH}₽  _(экономия 480₽)_\n\n"
        "После оплаты нажми «Я оплатил» — доступ активируется в течение нескольких минут.",
        parse_mode="Markdown",
        reply_markup=payment_keyboard()
    )


async def handle_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data in ("pay_month", "pay_3month"):
        months = "1 месяц" if query.data == "pay_month" else "3 месяца"
        price = PRICE_MONTH if query.data == "pay_month" else PRICE_3MONTH
        await query.edit_message_text(
            f"*Оплата за {months} — {price}₽*\n\n"
            "Переведи на:\n"
            f"• СБП: {MY_PHONE}\n"
            f"• ЮMoney: {MY_YOOMONEY}\n\n" if MY_YOOMONEY else ""
            "После перевода нажми кнопку 👇",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("✅ Я оплатил", callback_data=f"paid_{query.data}")
            ]])
        )

    elif query.data.startswith("paid_"):
        user_id = query.from_user.id
        username = query.from_user.username or str(user_id)
        plan = "30" if "month" in query.data and "3" not in query.data else "90"

        for admin_id in ADMIN_IDS:
            try:
                await context.bot.send_message(
                    chat_id=admin_id,
                    text=f"💰 Новая оплата!\n\n"
                         f"@{username} (id: {user_id})\n\n"
                         f"Активировать:\n"
                         f"/grant {user_id} {plan}"
                )
            except Exception:
                pass

        await query.edit_message_text(
            "Спасибо! Запрос отправлен.\n\n"
            "Доступ будет активирован в течение нескольких минут — "
            "я пришлю уведомление."
        )



async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка фотографий — анализ через Groq Vision."""
    user_id = update.effective_user.id

    if not is_allowed(user_id):
        await update.message.reply_text(
            "Доступ закончился. Выбери подписку:",
            reply_markup=payment_keyboard()
        )
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    # Скачиваем фото
    photo = update.message.photo[-1]  # берём наибольшее разрешение
    file = await context.bot.get_file(photo.file_id)

    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
        await file.download_to_drive(tmp.name)
        with open(tmp.name, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')

    caption = update.message.caption or ""
    user_text = f"[Клиент прислал изображение{': ' + caption if caption else ''}]"

    try:
        # Groq Vision — llama-4-scout поддерживает изображения
        add_to_history(user_id, "user", user_text)
        history = get_history(user_id)

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        # Добавляем историю без последнего (его заменим с картинкой)
        messages += history[:-1]
        # Последнее сообщение — с картинкой
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_data}"
                    }
                },
                {
                    "type": "text",
                    "text": caption if caption else "Клиент прислал изображение. Ответь в духе Архитектора — задай один вопрос об этом образе, используй технику зеркала."
                }
            ]
        })

        response = groq_client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=messages,
            temperature=0.85,
            max_tokens=600,
        )
        reply = response.choices[0].message.content
        add_to_history(user_id, "assistant", reply)
        await update.message.reply_text(reply)

    except Exception as e:
        logger.error(f"Vision error: {e}")
        # Fallback — если Vision не работает, отвечаем без картинки
        try:
            fallback_text = caption if caption else "Клиент прислал изображение без подписи."
            reply = ask_groq(user_id, f"[Клиент прислал изображение. {fallback_text}] Ответь в духе Архитектора — спроси что клиент хотел показать этим образом.")
            await update.message.reply_text(reply)
        except Exception as e2:
            logger.error(f"Fallback error: {e2}")
            await update.message.reply_text("Вижу, что ты прислал изображение. Расскажи — что на нём и что это для тебя значит?")



async def send_voice_reply(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    """Отправляет ответ голосовым сообщением через Edge TTS — естественный голос."""
    tmp_path = None
    try:
        import edge_tts
        import subprocess

        # Тёплый мужской русский голос Microsoft Neural
        voice = "ru-RU-DmitryNeural"

        if len(text) > 600:
            text = text[:600] + "..."

        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
            tmp_path = tmp.name

        # Запускаем edge-tts через subprocess — надёжнее на Python 3.13
        proc = await asyncio.create_subprocess_exec(
            "edge-tts",
            "--voice", voice,
            "--text", text,
            "--write-media", tmp_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await proc.communicate()

        if os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 0:
            with open(tmp_path, 'rb') as audio:
                await update.message.reply_voice(voice=audio)
            return True
        else:
            raise Exception("Файл не создан")

    except Exception as e:
        logger.error(f"Edge TTS error: {e}")
        # Fallback на gTTS
        try:
            from gtts import gTTS
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
                tmp_path = tmp.name
            tts = gTTS(text=text[:500], lang='ru', slow=False)
            tts.save(tmp_path)
            with open(tmp_path, 'rb') as audio:
                await update.message.reply_voice(voice=audio)
            return True
        except Exception as e2:
            logger.error(f"gTTS fallback error: {e2}")
            await update.message.reply_text(f"Не смог озвучить. Вот текстом:\n\n{text}")
            return False

    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except:
                pass


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка PDF и текстовых файлов."""
    user_id = update.effective_user.id

    if not is_allowed(user_id):
        await update.message.reply_text(
            "Доступ закончился. Выбери подписку:",
            reply_markup=payment_keyboard()
        )
        return

    doc = update.message.document
    if not doc:
        return

    file_name = doc.file_name or ""
    mime = doc.mime_type or ""

    # Только PDF и текстовые файлы
    if not (file_name.endswith('.pdf') or 'pdf' in mime or
            file_name.endswith('.txt') or 'text' in mime):
        await update.message.reply_text(
            "Я пока умею читать PDF и текстовые файлы. "
            "Пришли документ в одном из этих форматов."
        )
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await update.message.reply_text("Читаю документ...")

    try:
        file = await context.bot.get_file(doc.file_id)
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            await file.download_to_drive(tmp.name)
            tmp_path = tmp.name

        extracted_text = ""

        if file_name.endswith('.pdf') or 'pdf' in mime:
            try:
                import PyPDF2
                with open(tmp_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages[:10]:  # максимум 10 страниц
                        extracted_text += page.extract_text() + "\n"
            except ImportError:
                await update.message.reply_text(
                    "Не могу прочитать PDF — библиотека не установлена. "
                    "Попробуй скопировать текст и прислать напрямую."
                )
                return
        else:
            with open(tmp_path, 'r', encoding='utf-8', errors='ignore') as f:
                extracted_text = f.read()

        if not extracted_text.strip():
            await update.message.reply_text(
                "Не смог извлечь текст из документа. "
                "Возможно, это сканированный PDF. "
                "Попробуй скопировать текст и прислать напрямую."
            )
            return

        # Обрезаем если очень длинный
        if len(extracted_text) > 3000:
            extracted_text = extracted_text[:3000] + "...\n[текст обрезан]"

        caption = update.message.caption or ""
        prompt = f"Клиент прислал документ{': ' + caption if caption else ''}.\n\nСодержимое:\n{extracted_text}\n\nОтветь в духе Архитектора — задай один глубокий вопрос о том, что в этом документе важно для клиента."

        reply = ask_groq(user_id, prompt)
        await update.message.reply_text(reply)

    except Exception as e:
        logger.error(f"Document error: {e}")
        await update.message.reply_text(
            "Не смог прочитать документ. "
            "Попробуй скопировать текст и прислать напрямую."
        )



async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка голосовых сообщений через Groq Whisper."""
    user_id = update.effective_user.id

    if not is_allowed(user_id):
        await update.message.reply_text(
            "Доступ закончился. Выбери подписку:",
            reply_markup=payment_keyboard()
        )
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        # Скачиваем голосовое сообщение
        voice = update.message.voice or update.message.audio
        file = await context.bot.get_file(voice.file_id)

        with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as tmp:
            await file.download_to_drive(tmp.name)
            tmp_path = tmp.name

        # Транскрибируем через Groq Whisper
        with open(tmp_path, 'rb') as audio_file:
            transcription = groq_client.audio.transcriptions.create(
                file=(tmp_path, audio_file.read()),
                model="whisper-large-v3",
                language="ru",
                response_format="text"
            )

        text = transcription.strip() if isinstance(transcription, str) else transcription.text.strip()

        if not text:
            await update.message.reply_text(
                "Не смог разобрать голосовое. Попробуй ещё раз или напиши текстом."
            )
            return

        # Показываем что расслышали
        await update.message.reply_text(f"_{text}_", parse_mode="Markdown")

        # Передаём в коуча как обычный текст
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        reply = ask_groq(user_id, text)
        await update.message.reply_text(reply)

    except Exception as e:
        logger.error(f"Voice error: {e}")
        await update.message.reply_text(
            "Не смог обработать голосовое. Попробуй написать текстом."
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_allowed(user_id):
        await update.message.reply_text(
            "Доступ закончился. Выбери подписку:",
            reply_markup=payment_keyboard()
        )
        return

    user_text = update.message.text.strip()
    if not user_text:
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        reply = ask_groq(user_id, user_text)

        # Голосовой ответ только если клиент явно попросил
        voice_triggers = [
            "ответь голосом", "голосовой ответ", "скажи голосом",
            "отвечай голосом", "хочу голос", "говори голосом",
            "voice", "озвучь", "прочитай вслух"
        ]
        wants_voice = any(t in user_text.lower() for t in voice_triggers)

        if wants_voice:
            sent = await send_voice_reply(update, context, reply)
            if not sent:
                await update.message.reply_text(reply)
        else:
            await update.message.reply_text(reply)

    except RateLimitError as e:
        # Не сбрасываем историю — клиент сможет продолжить позже
        await update.message.reply_text(str(e))

    except Exception as e:
        logger.error(f"Groq error: {e}")
        reset_history(user_id)
        await update.message.reply_text(
            "Что-то прервало наш разговор. Напиши ещё раз — я здесь."
        )


# ── Админ-команды ─────────────────────────────────────────────────────────────

async def grant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/grant <user_id> <дней>"""
    if update.effective_user.id not in ADMIN_IDS:
        return
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Использование: /grant <user_id> <дней>")
        return
    try:
        target_id, days = int(args[0]), int(args[1])
    except ValueError:
        await update.message.reply_text("Пример: /grant 123456789 30")
        return

    user = get_user(target_id)
    now = datetime.now()
    current = datetime.fromisoformat(user["paid_until"]) if user.get("paid_until") else now
    if current < now:
        current = now
    user["paid_until"] = (current + timedelta(days=days)).isoformat()
    set_user(target_id, user)

    until = datetime.fromisoformat(user["paid_until"]).strftime("%d.%m.%Y")
    await update.message.reply_text(f"✅ Доступ выдан: {target_id} до {until}")

    try:
        await context.bot.send_message(
            chat_id=target_id,
            text=f"✨ Доступ активирован до {until}.\n\nНапиши /start — продолжим."
        )
    except Exception:
        pass


async def free_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/free <user_id>"""
    if update.effective_user.id not in ADMIN_IDS:
        return
    args = context.args
    if not args:
        await update.message.reply_text("Использование: /free <user_id>")
        return
    target_id = int(args[0])
    user = get_user(target_id)
    user["free"] = True
    set_user(target_id, user)
    await update.message.reply_text(f"✅ Бесплатный доступ выдан: {target_id}")
    try:
        await context.bot.send_message(
            chat_id=target_id,
            text="✨ Тебе открыт бесплатный доступ.\n\nНапиши /start — начнём."
        )
    except Exception:
        pass


async def revoke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/revoke <user_id>"""
    if update.effective_user.id not in ADMIN_IDS:
        return
    args = context.args
    if not args:
        await update.message.reply_text("Использование: /revoke <user_id>")
        return
    target_id = int(args[0])
    user = get_user(target_id)
    user["paid_until"] = None
    user["trial_until"] = None
    user["free"] = False
    set_user(target_id, user)
    await update.message.reply_text(f"⛔ Доступ отозван: {target_id}")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/stats"""
    if update.effective_user.id not in ADMIN_IDS:
        return
    db = load_db()
    now = datetime.now()
    total = len(db)
    paid = sum(1 for u in db.values()
               if u.get("paid_until") and datetime.fromisoformat(u["paid_until"]) > now)
    free = sum(1 for u in db.values() if u.get("free"))
    trial = sum(1 for u in db.values()
                if u.get("trial_until") and datetime.fromisoformat(u["trial_until"]) > now
                and not u.get("paid_until"))
    await update.message.reply_text(
        f"📊 *Статистика*\n\n"
        f"Всего: {total}\n"
        f"Активные подписки: {paid}\n"
        f"Бесплатный доступ: {free}\n"
        f"Пробный период: {trial}\n"
        f"Без доступа: {total - paid - free - trial}",
        parse_mode="Markdown"
    )


async def users_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/users"""
    if update.effective_user.id not in ADMIN_IDS:
        return
    db = load_db()
    now = datetime.now()
    lines = []
    for uid, u in list(db.items())[-20:]:
        if u.get("free"):
            status = "🎁 free"
        elif u.get("paid_until") and datetime.fromisoformat(u["paid_until"]) > now:
            until = datetime.fromisoformat(u["paid_until"]).strftime("%d.%m")
            status = f"✅ до {until}"
        elif u.get("trial_until") and datetime.fromisoformat(u["trial_until"]) > now:
            status = "🔍 trial"
        else:
            status = "❌"
        name = f"@{u['username']}" if u.get("username") else uid
        lines.append(f"{name} — {status}")
    await update.message.reply_text(
        "👥 *Последние пользователи:*\n\n" + "\n".join(lines),
        parse_mode="Markdown"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_admin = update.effective_user.id in ADMIN_IDS
    text = (
        "Архитектор — твой персональный коуч.\n\n"
        "Я не даю советов и не оцениваю.\n"
        "Я строю пространство из твоих слов.\n\n"
        "/start — начать сессию\n"
        "/new — новая сессия\n"
        "/subscribe — подписка\n"
    )
    if is_admin:
        text += (
            "\n*Команды админа:*\n"
            "/grant <id> <дней>\n"
            "/free <id>\n"
            "/revoke <id>\n"
            "/stats\n"
            "/users\n"
        )
    await update.message.reply_text(text, parse_mode="Markdown")


# ── Запуск ────────────────────────────────────────────────────────────────────

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("new", new_session))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("grant", grant))
    app.add_handler(CommandHandler("free", free_user))
    app.add_handler(CommandHandler("revoke", revoke))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("users", users_list))
    app.add_handler(CallbackQueryHandler(handle_payment_callback))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.AUDIO, handle_voice))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Архитектор на Groq запущен ✦")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
