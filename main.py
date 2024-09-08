import asyncio

from aiogram import Bot, Dispatcher

import bots
from handlers.check_profile_handler import check_profile_main
from handlers.booking_handler import booking_menu, stanytsia, vynnyky, botton
from handlers.start_menu import start


async def main():
    bot = Bot(bots.main_bot)
    dp = Dispatcher()
    dp.include_routers(
        booking_menu.router,
        start.router,
        stanytsia.router,
        vynnyky.router,
        botton.router,
        check_profile_main.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())