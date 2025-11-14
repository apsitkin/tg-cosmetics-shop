import os
import logging
from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Конфигурация
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://your-frontend.onrender.com')
PORT = int(os.getenv('PORT', 5000))

class CosmeticsBot:
    def __init__(self):
        self.application = Application.builder().token(BOT_TOKEN).build()
        self.setup_handlers()

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("shop", self.shop))
        self.application.add_handler(CallbackQueryHandler(self.button_handler))

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
        logger.info("Бот запущен...")
        self.application.run_polling()

# Flask endpoints для обработки заказов
@app.route('/api/order', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        logger.info(f"Получен заказ: {data}")
        
        # Здесь будет логика сохранения заказа
        # Пока просто возвращаем успех
        return jsonify({
            'status': 'success',
            'message': 'Заказ принят в обработку',
            'order_id': '12345'
        })
    except Exception as e:
        logger.error(f"Ошибка при создании заказа: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'service': 'cosmetics-bot'})

@app.route('/')
def home():
    return jsonify({'status': 'ok', 'message': 'Cosmetics Bot is running'})

# Создаем экземпляр бота
bot = CosmeticsBot()

if __name__ == '__main__':
    # В Render используем Flask для веб-сервера
    app.run(host='0.0.0.0', port=PORT, debug=False)