import asyncio
import logging
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import config
from handlers import common, greetings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    logger.info("Starting bot...")

    if not config.BOT_TOKEN:
        logger.error("BOT_TOKEN not found in environment variables! Please check your .env file.")
        return

    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML")) # Можно использовать HTML

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(common.router)
    dp.include_router(greetings.router)

    await bot.delete_webhook(drop_pending_updates=True)

    try:
        logger.info("Bot started polling.")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
    finally:
        await bot.session.close()
        logger.info("Bot stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot execution stopped by user.")
    except Exception as e:
        logger.error(f"An unexpected error occurred during main execution: {e}", exc_info=True)