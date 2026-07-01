// shop.js — client-side cart & wishlist engine (no backend; localStorage persistence)
(function(){
  var CART_KEY = 'alburooq_cart';
  var WISH_KEY = 'alburooq_wishlist';
  var WHATSAPP_NUMBER = '971544389066';

  function getCart(){
    try{ return JSON.parse(localStorage.getItem(CART_KEY)) || []; }catch(e){ return []; }
  }
  function setCart(cart){
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
    updateBadges();
  }
  function getWishlist(){
    try{ return JSON.parse(localStorage.getItem(WISH_KEY)) || []; }catch(e){ return []; }
  }
  function setWishlist(list){
    localStorage.setItem(WISH_KEY, JSON.stringify(list));
    updateBadges();
  }

  function addToCart(id, name, price, qty){
    qty = qty || 1;
    var cart = getCart();
    var existing = cart.find(function(i){ return i.id === id; });
    if(existing){ existing.qty += qty; }
    else { cart.push({id:id, name:name, price:price, qty:qty}); }
    setCart(cart);
  }
  function removeFromCart(id){
    setCart(getCart().filter(function(i){ return i.id !== id; }));
  }
  function updateQty(id, qty){
    var cart = getCart();
    var item = cart.find(function(i){ return i.id === id; });
    if(item){
      item.qty = Math.max(1, qty);
      setCart(cart);
    }
  }
  function toggleWishlist(id, name, price){
    var list = getWishlist();
    var idx = list.findIndex(function(i){ return i.id === id; });
    if(idx > -1){ list.splice(idx, 1); }
    else { list.push({id:id, name:name, price:price}); }
    setWishlist(list);
    return idx === -1; // true if now wishlisted
  }
  function isWishlisted(id){
    return getWishlist().some(function(i){ return i.id === id; });
  }

  function updateBadges(){
    var cart = getCart();
    var cartCount = cart.reduce(function(sum, i){ return sum + i.qty; }, 0);
    document.querySelectorAll('[data-cart-count]').forEach(function(el){
      el.textContent = cartCount;
      el.style.display = cartCount > 0 ? 'inline-flex' : 'none';
    });
    var wishCount = getWishlist().length;
    document.querySelectorAll('[data-wishlist-count]').forEach(function(el){
      el.textContent = wishCount;
      el.style.display = wishCount > 0 ? 'inline-flex' : 'none';
    });
    // sync wishlist heart buttons on current page
    document.querySelectorAll('[data-wishlist-btn]').forEach(function(btn){
      var id = btn.getAttribute('data-wishlist-btn');
      btn.classList.toggle('is-active', isWishlisted(id));
    });
  }

  function fmt(n){ return 'AED ' + Number(n).toLocaleString('en-AE', {minimumFractionDigits:0}); }

  function renderCartPage(){
    var container = document.getElementById('cart-items');
    if(!container) return;
    var cart = getCart();
    if(cart.length === 0){
      container.innerHTML = '<p class="form-hint">Your cart is empty. <a href="../">Browse the shop</a> to add equipment.</p>';
      document.getElementById('cart-summary').style.display = 'none';
      return;
    }
    var rows = cart.map(function(item){
      return '<div class="card" style="display:flex;justify-content:space-between;align-items:center;gap:1rem;margin-bottom:.75rem;flex-wrap:wrap;">' +
        '<div><strong>' + item.name + '</strong><div class="form-hint">' + fmt(item.price) + ' each</div></div>' +
        '<div style="display:flex;align-items:center;gap:.5rem;">' +
        '<input type="number" min="1" value="' + item.qty + '" data-qty="' + item.id + '" style="width:64px;padding:.4rem;border:1px solid var(--color-gray-300);border-radius:6px;">' +
        '<strong>' + fmt(item.price * item.qty) + '</strong>' +
        '<button class="btn btn-outline btn-sm" data-remove="' + item.id + '">Remove</button>' +
        '</div></div>';
    }).join('');
    container.innerHTML = rows;
    var total = cart.reduce(function(sum, i){ return sum + i.price * i.qty; }, 0);
    document.getElementById('cart-total').textContent = fmt(total);
    document.getElementById('cart-summary').style.display = 'block';

    container.querySelectorAll('[data-remove]').forEach(function(btn){
      btn.addEventListener('click', function(){
        removeFromCart(btn.getAttribute('data-remove'));
        renderCartPage();
      });
    });
    container.querySelectorAll('[data-qty]').forEach(function(input){
      input.addEventListener('change', function(){
        updateQty(input.getAttribute('data-qty'), parseInt(input.value, 10) || 1);
        renderCartPage();
      });
    });

    var waBtn = document.getElementById('cart-whatsapp');
    if(waBtn){
      waBtn.addEventListener('click', function(e){
        e.preventDefault();
        var lines = cart.map(function(i){ return '- ' + i.name + ' x' + i.qty + ' (' + fmt(i.price*i.qty) + ')'; });
        var msg = 'Hi, I would like to order the following equipment:%0A' + encodeURIComponent(lines.join('\n')) + '%0A%0ATotal: ' + encodeURIComponent(fmt(total));
        window.open('https://wa.me/' + WHATSAPP_NUMBER + '?text=' + msg, '_blank');
      });
    }
  }

  function renderWishlistPage(){
    var container = document.getElementById('wishlist-items');
    if(!container) return;
    var list = getWishlist();
    if(list.length === 0){
      container.innerHTML = '<p class="form-hint">Your wishlist is empty. <a href="../">Browse the shop</a> to save items for later.</p>';
      return;
    }
    container.innerHTML = list.map(function(item){
      return '<div class="card" style="display:flex;justify-content:space-between;align-items:center;gap:1rem;margin-bottom:.75rem;flex-wrap:wrap;">' +
        '<div><strong>' + item.name + '</strong><div class="form-hint">' + fmt(item.price) + '</div></div>' +
        '<div style="display:flex;gap:.5rem;">' +
        '<button class="btn btn-primary btn-sm" data-move="' + item.id + '" data-name="' + item.name + '" data-price="' + item.price + '">Add to Cart</button>' +
        '<button class="btn btn-outline btn-sm" data-remove-wish="' + item.id + '">Remove</button>' +
        '</div></div>';
    }).join('');
    container.querySelectorAll('[data-move]').forEach(function(btn){
      btn.addEventListener('click', function(){
        addToCart(btn.getAttribute('data-move'), btn.getAttribute('data-name'), parseFloat(btn.getAttribute('data-price')), 1);
        var note = document.createElement('span');
        note.className = 'form-hint';
        note.textContent = ' Added to cart';
        btn.after(note);
        setTimeout(function(){ note.remove(); }, 2000);
      });
    });
    container.querySelectorAll('[data-remove-wish]').forEach(function(btn){
      btn.addEventListener('click', function(){
        toggleWishlist(btn.getAttribute('data-remove-wish'));
        renderWishlistPage();
      });
    });
  }

  // Wire up product page / catalog buttons present on the page
  document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('[data-add-cart]').forEach(function(btn){
      btn.addEventListener('click', function(){
        var id = btn.getAttribute('data-add-cart');
        var name = btn.getAttribute('data-name');
        var price = parseFloat(btn.getAttribute('data-price'));
        var qtyInput = document.querySelector('[data-qty-input="' + id + '"]');
        var qty = qtyInput ? (parseInt(qtyInput.value, 10) || 1) : 1;
        addToCart(id, name, price, qty);
        var original = btn.textContent;
        btn.textContent = 'Added ✓';
        setTimeout(function(){ btn.textContent = original; }, 1500);
      });
    });
    document.querySelectorAll('[data-wishlist-btn]').forEach(function(btn){
      btn.addEventListener('click', function(){
        var id = btn.getAttribute('data-wishlist-btn');
        var name = btn.getAttribute('data-name');
        var price = parseFloat(btn.getAttribute('data-price'));
        toggleWishlist(id, name, price);
      });
    });
    updateBadges();
    renderCartPage();
    renderWishlistPage();
  });
})();
