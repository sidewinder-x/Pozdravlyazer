from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold, hitalic

from src.keyboards import inline as kb

router = Router()

# Обновленное приветственное сообщение с HTML-форматированием
WELCOME_MESSAGE = (
    f"{hbold('Добро пожаловать в Поздравляйзер!')} 🤖✨\n\n"
    "Я твой личный ИИ-помощник для создания "
    f"{hitalic('идеальных')} поздравлений на любой случай.\n\n"
    "Надоели банальные фразы? Я помогу придумать теплые, душевные или шутливые слова, "
    "которые точно запомнятся!\n\n"
    f"👇 Нажми {hbold('🎉 Создать поздравление')}, чтобы начать магию!"
)

# Обновленное описание с HTML-форматированием
HOW_IT_WORKS_MESSAGE = (
    f"{hbold('Как это работает? Всё просто!')}\n\n"
    f"1️⃣ {hbold('Ответь на пару вопросов:')} Кого поздравляем? Какой повод? Какое настроение?\n\n"
    f"2️⃣ {hbold('Получи варианты:')} Я предложу несколько уникальных текстов, сгенерированных нейросетью.\n\n"
    f"3️⃣ {hbold('Выбери лучший:')} Просто скопируй понравившееся поздравление одним касанием.\n\n"
    f"{hitalic('Идеальное поздравление готово!')}\n\n"
    "———\n"
    "Если что-то пошло не так или есть идеи, как сделать меня лучше, "
    f"напиши моему создателю: {hbold('@sidewinder_x')}" # TODO: Замените на реальный контакт
)


@router.message(CommandStart())
async def cmd_start(message: Message):
    # Убедитесь, что в bot.py у вас указан parse_mode="HTML"
    await message.answer(WELCOME_MESSAGE, reply_markup=kb.get_start_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(HOW_IT_WORKS_MESSAGE, disable_web_page_preview=True)


@router.callback_query(F.data == "how_it_works")
async def cb_how_it_works(callback: CallbackQuery):
    await callback.message.edit_text(
        HOW_IT_WORKS_MESSAGE,
        reply_markup=kb.get_start_keyboard(),
        disable_web_page_preview=True
    )
    await callback.answer()

# Рекомендация: обработчик команды /new лучше перенести в greetings.py,
# чтобы вся логика создания поздравлений была в одном месте.
# Я пока убрал его отсюда, чтобы избежать ошибок.
