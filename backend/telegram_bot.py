import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBAPP_URL = os.getenv('WEBAPP_URL')

class TelegramBot:
    def __init__(self):
        self.application = None
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [InlineKeyboardButton("🛍️ Открыть магазин", web_app=WebAppInfo(url=WEBAPP_URL))],
            [InlineKeyboardButton("📞 Контакты", callback_data="contacts")],
            [InlineKeyboardButton("ℹ️ О нас", callback_data="about")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Добро пожаловать в PRO Cosmetics! 🎀\n\n"
            "Профессиональная косметика для мастеров и салонов красоты.",
            reply_markup=reply_markup
        )

    async def shop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [[InlineKeyboardButton("🛒 Открыть магазин", web_app=WebAppInfo(url=WEBAPP_URL))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Нажмите кнопку ниже, чтобы открыть каталог товаров:",
            reply_markup=reply_markup
        )

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        if query.data == "contacts":
            await query.edit_message_text(
                "📞 Наши контакты:\n\n"
                "Телефон: +7 (999) 123-45-67\n"
                "Email: info@procosmetics.ru\n"
                "Адрес: г. Москва, ул. Косметическая, 1\n\n"
                "⏰ Время работы: 9:00 - 21:00"
            )
        elif query.data == "about":
            await query.edit_message_text(
                "PRO Cosmetics - поставщик профессиональной косметики премиум-класса.\n\n"
                "✅ Только оригинальная продукция\n"
                "✅ Доставка по всей России\n"
                "✅ Консультации профессионалов\n"
                "✅ Специальные условия для салонов"
            )

    def run(self):
        """Запускает бота"""
        try:
            self.application = Application.builder().token(BOT_TOKEN).build()
            
            # Регистрируем обработчики
            self.application.add_handler(CommandHandler("start", self.start))
            self.application.add_handler(CommandHandler("shop", self.shop))
            self.application.add_handler(CallbackQueryHandler(self.button_handler))
            
            logger.info("Бот запускается...")
            self.application.run_polling()
        except Exception as e:
            logger.error(f"Ошибка при запуске бота: {e}")

# Для запуска бота отдельно
if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()