import logging
import time
from datetime import datetime, timedelta
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import config
from main import *

logging.basicConfig(format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
cooldowns = {}
COOLDOWN_PERIOD = timedelta(seconds=5)

async def check_cooldown(user_id: int) -> bool:
    now = datetime.now()
    last_used = cooldowns.get(user_id)
    if last_used and now - last_used < COOLDOWN_PERIOD:
        return False  
    cooldowns[user_id] = now
    return True 

async def start(update:Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("The '/start' command was used")
    await update.message.reply_text(
        "Благодаря боту вы можете в разы быстрее смотреть расписание учебной группы Уральского Регионального Колледжа.\n\n*Доступные команды*:\n`/help` — Информация о доступных командах.\n`/schedule` _значение_ — Получить сегодняшнее расписание занятий.\n`/tomorrow` _значение_ — Получить завтрашнее расписание занятий. *Для выполения команды может занять какое-то время*.",
        parse_mode=ParseMode.MARKDOWN
        )

async def help(update:Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("The '/help' command was used")
    await update.message.reply_text(
        "*Доступные команды*:\n`/start` — Информация о боте.\n`/help` — Информация о доступных командах.\n`/schedule` _значение_ — Получить сегодняшнее расписание занятий. *Для выполения команды может занять какое-то время*.\n`/tomorrow` _значение_ — Получить завтрашнее расписание занятий. *Для выполения команды может занять какое-то время*.",
        parse_mode=ParseMode.MARKDOWN
        )

async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not await check_cooldown(user_id):
        await update.message.reply_text("Подождите немного перед повторным использованием этой команды.")
        return
    
    if context.args:
        number_value = context.args[0]
        logger.info(f"The '/schedule {number_value}' command was used")
        if number_value in config['groups']:
            try:
                logger.info("Fetching schedule...")
                start_time = time.time()
                schedule_result = await get_schedule(number_value)
                end_time = time.time()
                logger.info(f"Schedule fetched in {end_time - start_time} seconds")

                await update.message.reply_text(schedule_result, parse_mode=ParseMode.MARKDOWN)
            except Exception as e:
                logger.error(f"Error fetching schedule: {e}")
        else:
            await update.message.reply_text("Указать можно только доступные учебные группы: " + ", ".join(config['groups']))
    else:
        await update.message.reply_text("Пожалуйста, укажите учебную группу после команды. Пример: `/schedule 112`", parse_mode=ParseMode.MARKDOWN)

async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not await check_cooldown(user_id):
        await update.message.reply_text("Подождите немного перед повторным использованием этой команды.")
        return
    
    if context.args:
        number_value = context.args[0]
        logger.info(f"The '/tomorrow {number_value}' command was used")
        if number_value in config['groups']:
            try:
                logger.info("Fetching schedule...")
                start_time = time.time()
                schedule_result = await get_schedule_tomorrow(number_value)
                end_time = time.time()
                logger.info(f"Schedule fetched in {end_time - start_time} seconds")

                await update.message.reply_text(schedule_result, parse_mode=ParseMode.MARKDOWN)
            except Exception as e:
                logger.error(f"Error fetching schedule: {e}")
        else:
            await update.message.reply_text("Указать можно только доступные учебные группы: " + ", ".join(config['groups']))
    else:
        await update.message.reply_text("Пожалуйста, укажите учебную группу после команды. Пример: `/tomorrow 112`", parse_mode=ParseMode.MARKDOWN)

if __name__ == "__main__":
    app = ApplicationBuilder().token(config["token"]).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("schedule", schedule))
    app.add_handler(CommandHandler("tomorrow", tomorrow))
    app.run_polling()
