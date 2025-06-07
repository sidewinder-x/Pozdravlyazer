from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src import config


def get_check_subscription_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="↗️ Перейти в канал", url=config.CHANNEL_URL)
    builder.button(text="✅ Я подписался", callback_data="check_subscription")
    builder.adjust(1)
    return builder.as_markup()


def get_start_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🎉 Создать поздравление", callback_data="create_greeting")
    builder.button(text="ℹ️ Как это работает?", callback_data="how_it_works")
    builder.adjust(1)
    return builder.as_markup()


def get_greeting_options_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Маму", callback_data="recipient_mom")
    builder.button(text="Папу", callback_data="recipient_dad")
    builder.button(text="Друга / Подругу", callback_data="recipient_friend")
    builder.button(text="Коллегу", callback_data="recipient_colleague")
    builder.button(text="Любимого человека", callback_data="recipient_lover")
    builder.button(text="Другое (ввести вручную)", callback_data="recipient_custom")
    builder.button(text="⬅️ Назад", callback_data="back_to_start")
    builder.adjust(2, 2, 2, 1)
    return builder.as_markup()


def get_gender_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для выбора пола."""
    builder = InlineKeyboardBuilder()
    builder.button(text="Мужчине 👨", callback_data="gender_male")
    builder.button(text="Женщине 👩", callback_data="gender_female")
    builder.button(text="⬅️ Назад", callback_data="back_to_recipient")
    builder.adjust(2, 1)
    return builder.as_markup()


def get_custom_recipient_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура с кнопкой 'Назад' для шага ручного ввода."""
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад", callback_data="back_to_recipient")
    return builder.as_markup()


def get_occasion_options_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="День рождения", callback_data="occasion_birthday")
    builder.button(text="Новый год", callback_data="occasion_new_year")
    builder.button(text="Свадьба", callback_data="occasion_wedding")
    builder.button(text="Просто так", callback_data="occasion_just_because")
    builder.button(text="Другой повод", callback_data="occasion_custom")
    builder.button(text="⬅️ Назад", callback_data="back_to_gender_or_recipient")
    builder.adjust(2, 2, 1, 1)
    return builder.as_markup()


def get_style_options_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="😎 Дружеский", callback_data="style_friendly")
    builder.button(text="👔 Официальный", callback_data="style_formal")
    builder.button(text="😂 Шутливый", callback_data="style_humorous")
    builder.button(text="🥰 Трогательный", callback_data="style_emotional")
    builder.button(text="⬅️ Назад", callback_data="back_to_occasion")
    builder.adjust(2, 2, 1)
    return builder.as_markup()


def get_ty_vy_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="На 'ты'", callback_data="ty_vy_ty")
    builder.button(text="На 'Вы'", callback_data="ty_vy_vy")
    builder.button(text="⬅️ Назад", callback_data="back_to_style")
    builder.adjust(2, 1)
    return builder.as_markup()


def get_mood_options_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🥳 Радостное", callback_data="mood_joyful")
    builder.button(text="❤️ Душевное", callback_data="mood_calm")
    builder.button(text="🧐 Серьезное", callback_data="mood_solemn")
    builder.button(text="😜 С юмором", callback_data="mood_ironic")
    builder.button(text="⬅️ Назад", callback_data="back_to_ty_vy")
    builder.adjust(2, 2, 1)
    return builder.as_markup()


def get_length_options_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Короткое (2-3 предложения)", callback_data="length_short")
    builder.button(text="Среднее (небольшой абзац)", callback_data="length_medium")
    builder.button(text="Длинное (полноценное письмо)", callback_data="length_long")
    builder.button(text="⬅️ Назад", callback_data="back_to_mood")
    builder.adjust(1)
    return builder.as_markup()


def get_keywords_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="➡️ Пропустить", callback_data="keywords_skip")
    builder.button(text="⬅️ Назад", callback_data="back_to_length")
    builder.adjust(2)
    return builder.as_markup()


def get_greeting_variant_keyboard(variant_index: int, has_emojis: bool) -> InlineKeyboardMarkup:
    """Клавиатура с действиями для каждого варианта."""
    builder = InlineKeyboardBuilder()
    builder.button(text="📋 Копировать", callback_data=f"copy_{variant_index}")
    if has_emojis:
        builder.button(text="🚫 Убрать эмодзи", callback_data=f"remove_emojis_{variant_index}")
    else:
        builder.button(text="✨ Добавить эмодзи", callback_data=f"add_emojis_{variant_index}")
    builder.adjust(2)
    return builder.as_markup()


def get_after_greeting_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура с действиями после генерации."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🔄 Другие варианты", callback_data="more_options")
    builder.button(text="✍️ Дописать детали", callback_data="add_on")
    builder.button(text="✏️ Изменить параметры", callback_data="edit_params")
    builder.button(text="🎉 Создать новое", callback_data="create_greeting")
    builder.adjust(2, 2)
    return builder.as_markup()
