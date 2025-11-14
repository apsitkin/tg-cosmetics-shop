import os
import logging
from flask import Flask, request, jsonify

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
PORT = int(os.getenv('PORT', 10000))

# Простой эндпоинт для проверки работы
@app.route('/')
def home():
    return jsonify({
        'status': 'ok', 
        'message': 'Cosmetics Bot API is running',
        'endpoints': ['/health', '/test', '/api/order']
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'cosmetics-bot'})

@app.route('/test')
def test():
    return jsonify({'status': 'ok', 'message': 'Test endpoint works!'})

# Эндпоинт для обработки заказов из фронтенда
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

# Эндпоинт для получения товаров (можно добавить позже)
@app.route('/api/products', methods=['GET'])
def get_products():
    products = [
        {
            "id": 1,
            "name": "PRO Увлажняющий крем",
            "price": 2500,
            "category": "skincare"
        },
        {
            "id": 2, 
            "name": "PRO Тональная основа",
            "price": 3200,
            "category": "makeup"
        }
    ]
    return jsonify({'products': products})

if __name__ == '__main__':
    logger.info(f"Запуск Flask приложения на порту {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False)