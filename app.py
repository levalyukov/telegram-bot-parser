import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import config
from main import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def shedule(update:Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("The '/shedule' command was used")
    if context.args:
        number_value = context.args[0]
        if number_value in config['groups']:
            await update.message.reply_text(get_shedule(number_value))
        else:
            await update.message.reply_text("Пожалуйста, укажите доступные учебные группы: " + ", ".join(config['groups']))
    else:
        await update.message.reply_text("Пожалуйста, укажите учебную группу после команды. Пример: /shedule 100")

if __name__ == "__main__":
    app = ApplicationBuilder().token(config["token"]).build()
    logger.info("Telegram bot is ready to work")
    app.add_handler(CommandHandler("shedule", shedule))
    app.run_polling()
