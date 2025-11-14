// В методе checkout() замените URL:
fetch('https://pro-cosmetics-backend.onrender.com/api/order', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(orderData)
})class CosmeticsStore {
    constructor() {
        this.products = [];
        this.cart = [];
        this.tg = window.Telegram.WebApp;
        this.init();
    }

    init() {
        if (this.tg && this.tg.initDataUnsafe) {
            this.tg.expand();
            this.tg.enableClosingConfirmation();
        }
        
        this.loadProducts();
        this.setupEventListeners();
        this.updateUserInfo();
    }

    async loadProducts() {
        try {
            // Пример товаров - в реальном приложении будет запрос к API
            this.products = [
                {
                    id: 1,
                    name: "PRO Увлажняющий крем",
                    price: 2500,
                    category: "skincare",
                    image: "https://via.placeholder.com/300x300?text=PRO+Крем"
                },
                {
                    id: 2,
                    name: "PRO Тональная основа",
                    price: 3200,
                    category: "makeup",
                    image: "https://via.placeholder.com/300x300?text=Тональная+Основа"
                },
                {
                    id: 3,
                    name: "PRO Шампунь для волос",
                    price: 1800,
                    category: "hair",
                    image: "https://via.placeholder.com/300x300?text=PRO+Шампунь"
                },
                {
                    id: 4,
                    name: "PRO Омолаживающая сыворотка",
                    price: 4500,
                    category: "skincare",
                    image: "https://via.placeholder.com/300x300?text=PRO+Сыворотка"
                },
                {
                    id: 5,
                    name: "PRO Помада премиум",
                    price: 2200,
                    category: "makeup",
                    image: "https://via.placeholder.com/300x300?text=PRO+Помада"
                },
                {
                    id: 6,
                    name: "PRO Кондиционер",
                    price: 1900,
                    category: "hair",
                    image: "https://via.placeholder.com/300x300?text=PRO+Кондиционер"
                }
            ];
            
            this.renderProducts(this.products);
        } catch (error) {
            console.error('Ошибка загрузки товаров:', error);
        }
    }

    renderProducts(products) {
        const grid = document.getElementById('products-grid');
        if (!grid) return;
        
        grid.innerHTML = products.map(product => `
            <div class="product-card" data-category="${product.category}">
                <div class="product-image">${product.name}</div>
                <div class="product-title">${product.name}</div>
                <div class="product-price">${product.price} руб.</div>
                <button class="add-to-cart" onclick="store.addToCart(${product.id})">
                    Добавить в корзину
                </button>
            </div>
        `).join('');
    }

    addToCart(productId) {
        const product = this.products.find(p => p.id === productId);
        const existingItem = this.cart.find(item => item.id === productId);
        
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            this.cart.push({ ...product, quantity: 1 });
        }
        
        this.updateCart();
        if (this.tg && this.tg.HapticFeedback) {
            this.tg.HapticFeedback.impactOccurred('light');
        }
    }

    removeFromCart(productId) {
        this.cart = this.cart.filter(item => item.id !== productId);
        this.updateCart();
    }

    updateCart() {
        const count = this.cart.reduce((sum, item) => sum + item.quantity, 0);
        const cartCount = document.getElementById('cart-count');
        if (cartCount) {
            cartCount.textContent = count;
        }
        
        // Сохраняем корзину в localStorage
        localStorage.setItem('cosmetics_cart', JSON.stringify(this.cart));
    }

    renderCart() {
        const cartItems = document.getElementById('cart-items');
        if (!cartItems) return;
        
        const total = this.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        
        cartItems.innerHTML = this.cart.map(item => `
            <div class="cart-item">
                <div>
                    <strong>${item.name}</strong><br>
                    ${item.price} руб. × ${item.quantity}
                </div>
                <div>
                    <button onclick="store.removeFromCart(${item.id})">❌</button>
                </div>
            </div>
        `).join('');
        
        const totalPrice = document.getElementById('total-price');
        if (totalPrice) {
            totalPrice.textContent = total;
        }
    }

    setupEventListeners() {
        // Фильтрация по категориям
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                
                const category = e.target.dataset.category;
                const filtered = category === 'all' 
                    ? this.products 
                    : this.products.filter(p => p.category === category);
                
                this.renderProducts(filtered);
            });
        });

        // Модальное окно корзины
        const cartBtn = document.getElementById('cart-btn');
        const modal = document.getElementById('cart-modal');
        const closeBtn = document.querySelector('.close');

        if (cartBtn && modal && closeBtn) {
            cartBtn.addEventListener('click', () => {
                this.renderCart();
                modal.style.display = 'block';
            });

            closeBtn.addEventListener('click', () => {
                modal.style.display = 'none';
            });

            window.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.style.display = 'none';
                }
            });
        }

        // Оформление заказа
        const checkoutBtn = document.getElementById('checkout-btn');
        if (checkoutBtn) {
            checkoutBtn.addEventListener('click', () => {
                this.checkout();
            });
        }
    }

    updateUserInfo() {
        const user = this.tg?.initDataUnsafe?.user;
        const userName = document.getElementById('user-name');
        
        if (userName && user) {
            userName.textContent = 
                `${user.first_name || ''} ${user.last_name || ''}`.trim() || 'Пользователь';
        }
    }

    checkout() {
        if (this.cart.length === 0) {
            alert('Корзина пуста!');
            return;
        }

        const orderData = {
            products: this.cart,
            total: this.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0),
            user: this.tg?.initDataUnsafe?.user,
            contact: this.tg?.initDataUnsafe?.user?.id
        };

        // В реальном приложении здесь будет отправка данных на сервер
        console.log('Заказ оформлен:', orderData);
        
        if (this.tg && this.tg.showPopup) {
            this.tg.showPopup({
                title: 'Заказ оформлен!',
                message: `Ваш заказ на сумму ${orderData.total} руб. принят. Мы свяжемся с вами в ближайшее время.`,
                buttons: [{ type: 'ok' }]
            });
        } else {
            alert(`Заказ оформлен! Сумма: ${orderData.total} руб.`);
        }

        this.cart = [];
        this.updateCart();
        const modal = document.getElementById('cart-modal');
        if (modal) {
            modal.style.display = 'none';
        }
    }
}

// Инициализация приложения
const store = new CosmeticsStore();