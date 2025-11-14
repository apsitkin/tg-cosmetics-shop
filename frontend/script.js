// В методе checkout() замените URL:
fetch('https://pro-cosmetics-backend.onrender.com/api/order', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(orderData)
})