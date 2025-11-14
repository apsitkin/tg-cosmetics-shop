import os
import logging
import asyncio
from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Конфигурация
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://pro-cosmetics-frontend.onrender.com')
PORT = int(os.getenv('PORT', 5000))

# Глобальная переменная для приложения
application = None

def create_bot():
    """Создает и настраивает бота"""
    global application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("shop", shop))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    return application

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
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

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /shop"""
    keyboard = [[InlineKeyboardButton("🛒 Открыть магазин", web_app=WebAppInfo(url=WEBAPP_URL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Нажмите кнопку ниже, чтобы открыть каталог товаров:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на кнопки"""
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

def run_bot():
    """Запускает бота в отдельном потоке"""
    global application
    if application:
        logger.info("Запуск бота...")
        application.run_polling()

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

# Инициализация при запуске
if __name__ == '__main__':
    # Создаем бота
    create_bot()
    
    # Запускаем Flask приложение
    logger.info(f"Запуск Flask приложения на порту {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False)