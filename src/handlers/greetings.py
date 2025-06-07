from typing import Union

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold

from src.keyboards import inline as kb
from src import config
from src.ai_module import get_greeting_from_ai, add_emojis_to_text

router = Router()


class GreetingStates(StatesGroup):
    waiting_for_recipient = State()
    waiting_for_custom_recipient = State()
    waiting_for_gender = State()
    waiting_for_occasion = State()
    waiting_for_style = State()
    waiting_for_ty_vy = State()
    waiting_for_mood = State()
    waiting_for_length = State()
    waiting_for_keywords = State()
    waiting_for_addon = State()


RECIPIENT_MAP = {
    "recipient_mom": "маме", "recipient_dad": "папе", "recipient_friend": "другу / подруге",
    "recipient_colleague": "коллеге", "recipient_lover": "любимому человеку"
}
RECIPIENT_NEEDS_GENDER = ['recipient_friend', 'recipient_colleague', 'recipient_lover', 'recipient_custom']


async def check_subscription(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=config.CHANNEL_ID, user_id=user_id)
        return member.status not in ["left", "kicked"]
    except Exception:
        return False


# --- Навигационные функции ---
async def go_to_start(callback_or_message: Union[CallbackQuery, Message], state: FSMContext):
    await state.clear()
    text = "Чем могу помочь? ✨"
    markup = kb.get_start_keyboard()
    if isinstance(callback_or_message, CallbackQuery):
        await callback_or_message.message.edit_text(text, reply_markup=markup)
        await callback_or_message.answer()
    else:
        await callback_or_message.answer(text, reply_markup=markup)


async def go_to_recipient_step(callback_or_message: Union[CallbackQuery, Message], state: FSMContext, bot: Bot):
    if not await check_subscription(bot, callback_or_message.from_user.id):
        text = "Для доступа к генерации, пожалуйста, подпишитесь на наш канал ❤️\n\nПосле подписки нажмите кнопку ниже."
        markup = kb.get_check_subscription_keyboard()
        if isinstance(callback_or_message, CallbackQuery):
            await callback_or_message.message.edit_text(text, reply_markup=markup)
            await callback_or_message.answer(show_alert=True, text="Сначала нужно подписаться на канал!")
        else:
            await callback_or_message.answer(text, reply_markup=markup)
        return

    text = f"{hbold('Шаг 1:')} Кого будем поздравлять? 🎯"
    markup = kb.get_greeting_options_keyboard()
    if isinstance(callback_or_message, CallbackQuery):
        await callback_or_message.message.edit_text(text, reply_markup=markup)
    else:
        await callback_or_message.answer(text, reply_markup=markup)
    await state.set_state(GreetingStates.waiting_for_recipient)
    if isinstance(callback_or_message, CallbackQuery): await callback_or_message.answer()


async def go_to_gender_step(callback_or_message: Union[CallbackQuery, Message], state: FSMContext):
    text = f"{hbold('Шаг 2:')} Уточните пол получателя 👨/👩"
    markup = kb.get_gender_keyboard()
    if isinstance(callback_or_message, CallbackQuery):
        await callback_or_message.message.edit_text(text, reply_markup=markup)
    else:
        await callback_or_message.answer(text, reply_markup=markup)
    await state.set_state(GreetingStates.waiting_for_gender)


async def go_to_occasion_step(callback_or_message: Union[CallbackQuery, Message], state: FSMContext):
    user_data = await state.get_data()
    step_num = 3 if user_data.get("gender_step_passed") else 2
    text = f"{hbold(f'Шаг {step_num}:')} Какой повод для поздравления? 🥳"
    markup = kb.get_occasion_options_keyboard()
    if isinstance(callback_or_message, CallbackQuery):
        await callback_or_message.message.edit_text(text, reply_markup=markup)
    else:
        await callback_or_message.answer(text, reply_markup=markup)
    await state.set_state(GreetingStates.waiting_for_occasion)


async def go_to_style_step(callback_or_message: Union[CallbackQuery, Message], state: FSMContext):
    user_data = await state.get_data()
    step_num = 4 if user_data.get("gender_step_passed") else 3
    text = f"{hbold(f'Шаг {step_num}:')} В каком стиле должно быть поздравление? 🎨"
    markup = kb.get_style_options_keyboard()
    if isinstance(callback_or_message, CallbackQuery):
        await callback_or_message.message.edit_text(text, reply_markup=markup)
    else:
        await callback_or_message.answer(text, reply_markup=markup)
    await state.set_state(GreetingStates.waiting_for_style)


async def go_to_ty_vy_step(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    step_num = 5 if user_data.get("gender_step_passed") else 4
    await callback.message.edit_text(f"{hbold(f'Шаг {step_num}:')} Поздравление будет на 'ты' или на 'Вы'? 👇",
                                     reply_markup=kb.get_ty_vy_keyboard())
    await state.set_state(GreetingStates.waiting_for_ty_vy)


async def go_to_mood_step(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    step_num = 6 if user_data.get("gender_step_passed") else 5
    await callback.message.edit_text(f"{hbold(f'Шаг {step_num}:')} Какое настроение должно быть у поздравления? 🤔",
                                     reply_markup=kb.get_mood_options_keyboard())
    await state.set_state(GreetingStates.waiting_for_mood)


async def go_to_length_step(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    step_num = 7 if user_data.get("gender_step_passed") else 6
    await callback.message.edit_text(f"{hbold(f'Шаг {step_num}:')} Какой длины должно быть поздравление? 📏",
                                     reply_markup=kb.get_length_options_keyboard())
    await state.set_state(GreetingStates.waiting_for_length)


async def go_to_keywords_step(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "И последний штрих! ✨\n\n"
        "Здесь можно указать **имя получателя** или другие важные детали (например: 'Иван, любит рыбалку').\n\n"
        "Или просто пропустите этот шаг.",
        reply_markup=kb.get_keywords_keyboard()
    )
    await state.set_state(GreetingStates.waiting_for_keywords)


# --- Логика генерации ---
async def generate_and_show_greeting(message: Message, state: FSMContext):
    await message.answer("⏳ Минутку, подключаю нейросеть...")
    user_data = await state.get_data()

    recipient = user_data.get('recipient', 'человеку')
    if (gender := user_data.get('gender')):
        recipient = f"{recipient} ({'мужчине' if gender == 'male' else 'женщине'})"

    prompt_details = [
        f"Напиши поздравление для {recipient} по случаю '{user_data.get('occasion', 'праздника')}'.",
        f"Стиль: {user_data.get('style', 'дружеский')}. Обращение: {'на ты' if user_data.get('ty_vy') == 'ty' else 'на Вы'}.",
        f"Настроение: {user_data.get('mood', 'радостное')}. Длина: {user_data.get('length', 'средняя')}."
    ]
    if keywords := user_data.get('keywords'):
        prompt_details.append(f"Обязательно используй или учти эти детали: {keywords}.")

    prompt = " ".join(prompt_details)
    generated_texts = await get_greeting_from_ai(prompt)

    variants_data = [{'original': text, 'emojified': None, 'has_emojis': False} for text in generated_texts]
    await state.update_data(generated_variants=variants_data)

    await message.answer(f"{hbold('✨ Готово!')} Вот несколько вариантов от нейросети:")
    for i, data in enumerate(variants_data):
        await message.answer(data['original'], reply_markup=kb.get_greeting_variant_keyboard(i, data['has_emojis']))

    await message.answer("Что делаем дальше?", reply_markup=kb.get_after_greeting_keyboard())


# --- ОБРАБОТЧИКИ (HANDLERS) ---
@router.callback_query(F.data.in_({"create_greeting", "check_subscription"}))
async def cb_create_greeting_start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await go_to_recipient_step(callback, state, bot)


# --- Кнопки "Назад" ---
@router.callback_query(F.data == "back_to_start")
async def cb_back_to_start(callback: CallbackQuery, state: FSMContext):
    await go_to_start(callback, state)


@router.callback_query(F.data == "back_to_recipient")
async def cb_back_to_recipient(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await go_to_recipient_step(callback, state, bot)


@router.callback_query(F.data == "back_to_gender_or_recipient")
async def cb_back_to_gender_or_recipient(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    if user_data.get("gender_step_passed"):
        await go_to_gender_step(callback, state)
    else:
        await go_to_recipient_step(callback, state, bot)
    await callback.answer()


@router.callback_query(F.data == "back_to_occasion")
async def cb_back_to_occasion(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    if user_data.get("gender_step_passed"):
        await go_to_gender_step(callback, state)
    else:
        await go_to_recipient_step(callback, state, bot)
    await callback.answer()


@router.callback_query(F.data == "back_to_style")
async def cb_back_to_style(callback: CallbackQuery, state: FSMContext):
    await go_to_occasion_step(callback, state)
    await callback.answer()


@router.callback_query(F.data == "back_to_ty_vy")
async def cb_back_to_ty_vy(callback: CallbackQuery, state: FSMContext):
    await go_to_style_step(callback, state)
    await callback.answer()


@router.callback_query(F.data == "back_to_mood")
async def cb_back_to_mood(callback: CallbackQuery, state: FSMContext):
    await go_to_ty_vy_step(callback, state)
    await callback.answer()


@router.callback_query(F.data == "back_to_length")
async def cb_back_to_length(callback: CallbackQuery, state: FSMContext):
    await go_to_mood_step(callback, state)
    await callback.answer()


# --- Шаги анкеты (FSM) ---

# Step 1: Recipient
@router.callback_query(GreetingStates.waiting_for_recipient, F.data.startswith("recipient_"))
async def process_recipient_from_kb(callback: CallbackQuery, state: FSMContext):
    recipient_key = callback.data
    if recipient_key == "recipient_custom":
        await callback.message.edit_text(
            "Хорошо, напишите, кому адресовано поздравление (например, 'лучшей подруге Ане').",
            reply_markup=kb.get_custom_recipient_keyboard()
        )
        await state.set_state(GreetingStates.waiting_for_custom_recipient)
    else:
        recipient_text = RECIPIENT_MAP.get(recipient_key, "человеку")
        await state.update_data(recipient=recipient_text, recipient_type_raw=recipient_key)
        if recipient_key in RECIPIENT_NEEDS_GENDER:
            await state.update_data(gender_step_passed=True)
            await go_to_gender_step(callback, state)
        else:
            await state.update_data(gender_step_passed=False)
            gender = "female" if recipient_key == "recipient_mom" else "male"
            await state.update_data(gender=gender)
            await go_to_occasion_step(callback, state)
    await callback.answer()


@router.message(GreetingStates.waiting_for_custom_recipient)
async def process_custom_recipient_text(message: Message, state: FSMContext):
    await state.update_data(recipient=message.text, recipient_type_raw="recipient_custom", gender_step_passed=True)
    await go_to_gender_step(message, state)


# Step 2: Gender
@router.callback_query(GreetingStates.waiting_for_gender, F.data.startswith("gender_"))
async def process_gender(callback: CallbackQuery, state: FSMContext):
    gender = callback.data.replace('gender_', '')
    await state.update_data(gender=gender)
    await go_to_occasion_step(callback, state)
    await callback.answer()


# Step 3: Occasion
@router.callback_query(GreetingStates.waiting_for_occasion, F.data.startswith("occasion_"))
async def process_occasion_from_kb(callback: CallbackQuery, state: FSMContext):
    if callback.data == "occasion_custom":
        await callback.message.edit_text("Понял. Напишите, какой именно повод.",
                                         reply_markup=kb.get_custom_recipient_keyboard())
        await state.set_state(GreetingStates.waiting_for_occasion)
    else:
        button_text = next((b.text for row in callback.message.reply_markup.inline_keyboard for b in row if
                            b.callback_data == callback.data), "праздник")
        await state.update_data(occasion=button_text)
        await go_to_style_step(callback, state)
    await callback.answer()


@router.message(GreetingStates.waiting_for_occasion)
async def process_occasion_from_text(message: Message, state: FSMContext):
    await state.update_data(occasion=message.text)
    await go_to_style_step(message, state)


# Step 4: Style
@router.callback_query(GreetingStates.waiting_for_style, F.data.startswith("style_"))
async def process_style(callback: CallbackQuery, state: FSMContext):
    button_text = next((b.text for row in callback.message.reply_markup.inline_keyboard for b in row if
                        b.callback_data == callback.data), "дружеский").strip("😎👔😂�")
    await state.update_data(style=button_text)
    await go_to_ty_vy_step(callback, state)
    await callback.answer()


# Step 5: 'ty'/'vy'
@router.callback_query(GreetingStates.waiting_for_ty_vy, F.data.startswith("ty_vy_"))
async def process_ty_vy(callback: CallbackQuery, state: FSMContext):
    await state.update_data(ty_vy=callback.data.replace('ty_vy_', ''))
    await go_to_mood_step(callback, state)
    await callback.answer()


# Step 6: Mood
@router.callback_query(GreetingStates.waiting_for_mood, F.data.startswith("mood_"))
async def process_mood(callback: CallbackQuery, state: FSMContext):
    button_text = next((b.text for row in callback.message.reply_markup.inline_keyboard for b in row if
                        b.callback_data == callback.data), "радостное").strip("🥳❤️🧐😜")
    await state.update_data(mood=button_text)
    await go_to_length_step(callback, state)
    await callback.answer()


# Step 7: Length
@router.callback_query(GreetingStates.waiting_for_length, F.data.startswith("length_"))
async def process_length(callback: CallbackQuery, state: FSMContext):
    button_text = next((b.text for row in callback.message.reply_markup.inline_keyboard for b in row if
                        b.callback_data == callback.data), "средняя")
    await state.update_data(length=button_text)
    await go_to_keywords_step(callback, state)
    await callback.answer()


# Step 8: Keywords & Generation
@router.message(GreetingStates.waiting_for_keywords)
async def process_keywords_and_generate(message: Message, state: FSMContext):
    await state.update_data(keywords=message.text.strip())
    await message.delete()
    await generate_and_show_greeting(message, state)


@router.callback_query(GreetingStates.waiting_for_keywords, F.data == "keywords_skip")
async def process_skip_keywords_and_generate(callback: CallbackQuery, state: FSMContext):
    await state.update_data(keywords="")
    await callback.message.delete()
    await generate_and_show_greeting(callback.message, state)
    await callback.answer()


# --- Обработчики после генерации ---
@router.callback_query(F.data.startswith("copy_"))
async def cb_copy_text(callback: CallbackQuery):
    await callback.answer(text="Нажмите на текст и удерживайте, затем выберите 'Копировать'", show_alert=True)


@router.callback_query(F.data.startswith(("add_emojis_", "remove_emojis_")))
async def cb_toggle_emojis(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split('_')
    action = parts[0]
    variant_index = int(parts[-1])

    user_data = await state.get_data()
    variants = user_data.get("generated_variants", [])

    if not (variant_index < len(variants)):
        await callback.answer("Не удалось найти этот вариант.", show_alert=True)
        return

    variant_data = variants[variant_index]

    if action == "add":
        if variant_data.get('emojified') is None:
            await callback.answer("✨ Оживляю текст...")
            emojified_text = await add_emojis_to_text(variant_data['original'])
            variant_data['emojified'] = emojified_text
        else:
            emojified_text = variant_data['emojified']
            await callback.answer()
        variant_data['has_emojis'] = True
        text_to_show = emojified_text
    else:  # remove
        variant_data['has_emojis'] = False
        text_to_show = variant_data['original']
        await callback.answer("Эмодзи убраны")

    await state.update_data(generated_variants=variants)
    await callback.message.edit_text(
        text_to_show,
        reply_markup=kb.get_greeting_variant_keyboard(variant_index, variant_data['has_emojis'])
    )


@router.callback_query(F.data == "more_options")
async def cb_more_options(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    if not user_data.get("recipient"):
        await callback.answer("Ой, я уже забыл параметры. Начните заново.", show_alert=True)
        await go_to_start(callback, state)
        return

    await callback.message.delete()
    await generate_and_show_greeting(callback.message, state)
    await callback.answer()


@router.callback_query(F.data == "add_on")
async def cb_add_on(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Отлично! Напишите, что бы вы хотели добавить или уточнить в поздравлении.")
    await state.set_state(GreetingStates.waiting_for_addon)
    await callback.answer()


@router.message(GreetingStates.waiting_for_addon)
async def process_addon_and_regenerate(message: Message, state: FSMContext):
    user_data = await state.get_data()
    existing_keywords = user_data.get("keywords", "")
    new_addon = message.text
    updated_keywords = f"{existing_keywords}. Дополнительные пожелания: {new_addon}"
    await state.update_data(keywords=updated_keywords)

    # Удаляем сообщение с кнопками "Другие варианты" и т.д.
    try:
        if message.reply_to_message:
            pass
    except Exception as e:
        print(f"Не удалось удалить сообщение с кнопками: {e}")

    await generate_and_show_greeting(message, state)


@router.callback_query(F.data == "edit_params")
async def cb_edit_params(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer("Давайте начнем заново!")
    await callback.message.delete()
    await go_to_recipient_step(callback, state, bot)
