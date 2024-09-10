import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import config
from main import *

# Logging
logging.basicConfig(format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Commands for telegram bot
async def start(update:Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("The '/start' command was used")
    await update.message.reply_text(
        "Благодаря боту вы можете в разы быстрее смотреть расписание учебной группы Уральского Регионального Колледжа.\n\n*Доступные команды*:\n/help — Информация о доступных командах.\n/schedule _значение_ — Получить сегодняшнее расписание занятий.",
        parse_mode=ParseMode.MARKDOWN
        )

async def help(update:Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("The '/help' command was used")
    await update.message.reply_text(
        "*Доступные команды*:\n/start — Информация о боте.\n/help — Информация о доступных командах.\n/schedule _значение_ — Получить сегодняшнее расписание занятий. *Для выполения команды может занять какое-то время*.",
        parse_mode=ParseMode.MARKDOWN
        )

async def schedule(update:Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("The '/schedule' command was used")
    if context.args:
        number_value = context.args[0]
        if number_value in config['groups']:
            await update.message.reply_text(get_schedule(number_value), parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text("Указать можно только доступные учебные группы: " + ", ".join(config['groups']))
    else:
        await update.message.reply_text("Пожалуйста, укажите учебную группу после команды. Пример: /schedule 112")
# ---

if __name__ == "__main__":
    app = ApplicationBuilder().token(config["token"]).build()
    logger.info("Bot is ready to work")
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("schedule", schedule))
    app.run_polling()
