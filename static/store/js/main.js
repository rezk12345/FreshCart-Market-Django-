function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function updateCartBadge(count) {
    const badge = document.getElementById('cartBadge');
    if (badge) badge.textContent = count;
}

function showToast(message) {
    let toast = document.getElementById('stockToast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'stockToast';
        toast.className = 'stock-toast';
        document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(toast._hideTimer);
    toast._hideTimer = setTimeout(function () {
        toast.classList.remove('show');
    }, 2500);
}

function postForm(url, data) {
    const body = new URLSearchParams(data);
    return fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: body,
    }).then((res) => res.json());
}

document.addEventListener('DOMContentLoaded', function () {

    const navToggle = document.getElementById('navToggle');
    const mainNav = document.getElementById('mainNav');
    if (navToggle && mainNav) {
        navToggle.addEventListener('click', function () {
            mainNav.classList.toggle('open');
        });
    }

    document.querySelectorAll('.btn-add-cart').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const productId = btn.dataset.productId;
            postForm('/cart/add/' + productId + '/', { quantity: 1 }).then((data) => {
                if (data.success) {
                    updateCartBadge(data.cart_count);
                    if (data.capped) {
                        showToast('Only ' + data.stock + ' in stock — cart updated to the max available.');
                    } else {
                        btn.textContent = 'Added ✓';
                        btn.classList.add('added');
                        setTimeout(function () {
                            btn.textContent = 'Add +';
                            btn.classList.remove('added');
                        }, 1200);
                    }
                }
            });
        });
    });

    const addToCartBtn = document.getElementById('addToCartBtn');
    const qtyInput = document.getElementById('qtyInput');
    const qtyMinus = document.getElementById('qtyMinus');
    const qtyPlus = document.getElementById('qtyPlus');
    const addConfirm = document.getElementById('addConfirm');

    if (qtyMinus && qtyInput) {
        qtyMinus.addEventListener('click', function () {
            const val = parseInt(qtyInput.value) || 1;
            qtyInput.value = Math.max(1, val - 1);
        });
        qtyPlus.addEventListener('click', function () {
            const val = parseInt(qtyInput.value) || 1;
            const max = parseInt(qtyInput.max) || 999;
            qtyInput.value = Math.min(max, val + 1);
        });
        qtyInput.addEventListener('change', function () {
            const max = parseInt(qtyInput.max) || 999;
            let val = parseInt(qtyInput.value) || 1;
            if (val > max) {
                val = max;
                showToast('Only ' + max + ' in stock.');
            }
            if (val < 1) val = 1;
            qtyInput.value = val;
        });
    }

    if (addToCartBtn) {
        addToCartBtn.addEventListener('click', function () {
            const productId = addToCartBtn.dataset.productId;
            const quantity = qtyInput ? qtyInput.value : 1;
            postForm('/cart/add/' + productId + '/', { quantity: quantity }).then((data) => {
                if (data.success) {
                    updateCartBadge(data.cart_count);
                    if (data.capped) {
                        showToast('Only ' + data.stock + ' in stock — cart updated to the max available.');
                    } else {
                        addConfirm.classList.add('show');
                        setTimeout(() => addConfirm.classList.remove('show'), 2000);
                    }
                }
            });
        });
    }

    const liveSearch = document.getElementById('liveSearch');
    const productGrid = document.getElementById('productGrid');
    const resultsCount = document.getElementById('resultsCount');

    function filterProducts() {
        if (!productGrid) return;
        const term = liveSearch ? liveSearch.value.toLowerCase() : '';
        const cards = productGrid.querySelectorAll('.product-card');
        let visibleCount = 0;

        cards.forEach(function (card) {
            const name = card.dataset.name || '';
            const matchesTerm = name.includes(term);
            if (matchesTerm) {
                card.style.display = '';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        if (resultsCount) {
            resultsCount.textContent = visibleCount + ' product' + (visibleCount === 1 ? '' : 's') + ' found';
        }
    }

    if (liveSearch) {
        liveSearch.addEventListener('input', filterProducts);
    }

    function recalcCartTotals() {
        let total = 0;
        let count = 0;
        document.querySelectorAll('.cart-item').forEach(function (item) {
            const subtotalEl = item.querySelector('.cart-item-subtotal');
            const subtotal = parseFloat(subtotalEl.textContent.replace('$', '')) || 0;
            total += subtotal;
            count += parseInt(item.querySelector('.cart-qty-input').value) || 0;
        });
        const summaryTotal = document.getElementById('summaryTotal');
        const summaryCount = document.getElementById('summaryCount');
        if (summaryTotal) summaryTotal.textContent = '$' + total.toFixed(2);
        if (summaryCount) summaryCount.textContent = count;
        updateCartBadge(count);
    }

    document.querySelectorAll('.cart-item').forEach(function (item) {
        const productId = item.dataset.productId;
        const qtyInputEl = item.querySelector('.cart-qty-input');
        const minusBtn = item.querySelector('.cart-qty-minus');
        const plusBtn = item.querySelector('.cart-qty-plus');
        const removeBtn = item.querySelector('.cart-item-remove');
        const unitPrice = parseFloat(item.querySelector('.cart-item-info p').textContent.replace('$', ''));
        const subtotalEl = item.querySelector('.cart-item-subtotal');
        const maxStock = parseInt(qtyInputEl.max) || 999;

        function applyQuantity(newQty) {
            if (newQty < 1) newQty = 1;
            qtyInputEl.value = newQty;
            subtotalEl.textContent = '$' + (unitPrice * newQty).toFixed(2);
            recalcCartTotals();
        }

        function updateQuantity(newQty) {
            if (newQty > maxStock) {
                showToast('Only ' + maxStock + ' in stock.');
                newQty = maxStock;
            }
            applyQuantity(newQty);
            postForm('/cart/update/' + productId + '/', { quantity: newQty }).then((data) => {
                if (data.success && data.capped && data.quantity_in_cart !== newQty) {
                    applyQuantity(data.quantity_in_cart);
                }
            });
        }

        if (minusBtn) {
            minusBtn.addEventListener('click', function () {
                updateQuantity((parseInt(qtyInputEl.value) || 1) - 1);
            });
        }
        if (plusBtn) {
            plusBtn.addEventListener('click', function () {
                updateQuantity((parseInt(qtyInputEl.value) || 1) + 1);
            });
        }
        if (qtyInputEl) {
            qtyInputEl.addEventListener('change', function () {
                updateQuantity(parseInt(qtyInputEl.value) || 1);
            });
        }
        if (removeBtn) {
            removeBtn.addEventListener('click', function () {
                postForm('/cart/remove/' + productId + '/', {}).then((data) => {
                    if (data.success) {
                        item.remove();
                        recalcCartTotals();
                        if (document.querySelectorAll('.cart-item').length === 0) {
                            location.reload();
                        }
                    }
                });
            });
        }
    });

});
