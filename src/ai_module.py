import httpx
from src import config

API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

async def _send_request_to_yandex_gpt(payload: dict) -> dict:
    """Вспомогательная функция для отправки запроса к YandexGPT."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {config.YANDEX_API_KEY}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, headers=headers, json=payload, timeout=30.0)
        response.raise_for_status()
        return response.json()

async def get_greeting_from_ai(prompt: str) -> list[str]:
    """Отправляет промпт в YandexGPT для генерации поздравлений."""
    payload = {
        "modelUri": f"gpt://{config.YANDEX_FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {"stream": False, "temperature": 0.7, "maxTokens": 2000},
        "messages": [
            {
                "role": "system",
                "text": "Ты — дружелюбный и креативный ассистент, который пишет красивые поздравления на русском. "
                        "Твоя задача — сгенерировать 2-3 полностью готовых к отправке варианта. "
                        "КРАЙНЕ ВАЖНО: не используй плейсхолдеры вроде [имя] или [имя коллеги]. Пиши готовый текст. "
                        "Если имя не указано, обращайся безлично (например, 'Уважаемый коллега!'). "
                        "Каждый вариант отделяй от следующего уникальным разделителем: '---'."
            },
            {"role": "user", "text": prompt}
        ]
    }
    try:
        data = await _send_request_to_yandex_gpt(payload)
        generated_text = data['result']['alternatives'][0]['message']['text']
        # Разделяем ответ нейросети по кастомному разделителю, чтобы избежать случайных разрывов
        variants = [variant.strip() for variant in generated_text.split('---') if variant.strip()]
        return variants if variants else ["К сожалению, нейросеть не дала ответа. Попробуйте снова."]
    except Exception as e:
        print(f"Ошибка при генерации поздравления: {e}")
        return ["Извините, при генерации произошла ошибка. Попробуйте изменить запрос."]

async def add_emojis_to_text(text: str) -> str:
    """Отправляет текст в YandexGPT, чтобы добавить эмодзи."""
    payload = {
        "modelUri": f"gpt://{config.YANDEX_FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {"stream": False, "temperature": 0.4, "maxTokens": 2000},
        "messages": [
            {
                "role": "system",
                "text": "Твоя задача — аккуратно добавить подходящие по смыслу эмодзи в существующий текст, чтобы он стал более живым. "
                        "Не меняй сам текст, только расставь эмодзи."
            },
            {"role": "user", "text": text}
        ]
    }
    try:
        data = await _send_request_to_yandex_gpt(payload)
        return data['result']['alternatives'][0]['message']['text']
    except Exception as e:
        print(f"Ошибка при добавлении эмодзи: {e}")
        return text # В случае ошибки возвращаем исходный текст
