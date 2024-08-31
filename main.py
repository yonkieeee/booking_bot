import asyncio
from aiogram import Bot, Dispatcher
from handlers.booking_handler import booking_menu, stanytsia, vynnyky, botton
from handlers.start_menu import start
import bots


async def main():
    bot = Bot(bots.main_bot)
    dp = Dispatcher()
    dp.include_routers(
        booking_menu.router,
        start.router,
        stanytsia.router,
        vynnyky.router,
        botton.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())