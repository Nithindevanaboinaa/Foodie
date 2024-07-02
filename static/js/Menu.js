document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.categories button');
    const items = document.querySelectorAll('.menu-item');

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const filter = button.getAttribute('data-filter');

            items.forEach(item => {
                if (filter === 'all') {
                    item.style.display = 'block';
                } else {
                    if (item.getAttribute('data-category') === filter) {
                        item.style.display = 'block';
                    } else {
                        item.style.display = 'none';
                    }
                }
            });
        });
    });
});

function showDetails(element) {
    const item = element.closest('.menu-item');
    const name = item.getAttribute('data-name');
    const price = item.getAttribute('data-price');
    const description = item.getAttribute('data-description');
    const image = item.getAttribute('data-image');

    document.getElementById('modal-image').src = image;
    document.getElementById('modal-title').textContent = name;
    document.getElementById('modal-description').textContent = description;
    document.getElementById('modal-price').textContent = `price ₹${price}`;
    document.getElementById('quantity').value = 1;

    document.getElementById('item-modal').style.display = 'block';
}

function closeModal() {
    document.getElementById('item-modal').style.display = 'none';
}

let cart = [];

function addToCart() {
    const name = document.getElementById('modal-title').textContent;
    const quantity = parseInt(document.getElementById('quantity').value);
    const price = parseInt(document.getElementById('modal-price').textContent.replace('price ₹', ''));
    
    const item = { name, quantity, price };
    cart.push(item);
    
    updateCartCount();
    console.log(cart)
    closeModal();
}

function updateCartCount() {
    document.getElementById('cart-count').textContent = cart.length;
}

document.getElementById('cart-icon').addEventListener('click', () => {
    if (cart.length === 0) {
        alert('Your cart is empty');
    } else {
        const cartItemsList = document.getElementById('cart-items');
        const totalAmount = document.getElementById('total-amount');
    
        cartItemsList.innerHTML = '';
        let total = 0;
        cart.forEach(item => {
            const listItem = document.createElement('li');
            listItem.textContent = `${item.quantity} x ${item.name} - ₹${item.price * item.quantity}`;
            cartItemsList.appendChild(listItem);
            total += item.price * item.quantity;
        });
    
        totalAmount.textContent = `Total: ₹${total}`;
        window.location.href = "cart.html";
    }
});

function displayCartDetails() {
    const cartItemsList = document.getElementById('cart-items');
    const totalAmount = document.getElementById('total-amount');

    cartItemsList.innerHTML = '';
    let total = 0;
    cart.forEach(item => {
        const listItem = document.createElement('li');
        listItem.textContent = `${item.quantity} x ${item.name} - ₹${item.price * item.quantity}`;
        cartItemsList.appendChild(listItem);
        total += item.price * item.quantity;
    });

    totalAmount.textContent = `Total: ₹${total}`;
    
}

updateCartCount();
