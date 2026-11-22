/* E-Sannad buy buttons.
   Paste a Ziina payment link for each package below (Ziina app > Get paid > Payment link).
   Until a link is pasted, the button opens WhatsApp with the order, so it always works. */
window.BUROOQ_PAY = {
  'fleet': '',   // Fleet & Traffic Fines – 1000 AED
  'retail': '',   // Retail Shop POS – 1000 AED
  'grocery': '',   // Grocery & Supermarket POS – 1000 AED
  'salon': '',   // Beauty Salon & Barber POS – 1000 AED
  'tailoring': '',   // Tailoring & Abaya Shop – 1000 AED
  'emenu': '',   // QR E-Menu – 1000 AED
  'restaurant': '',   // Restaurant & Café POS – 1000 AED
  'laundry': '',   // Laundry & Dry Cleaning – 1000 AED
  'carwash': '',   // Car Wash POS – 1000 AED
  'contracting': '',   // Contracting & Projects – 1000 AED
};
(function () {
  document.querySelectorAll('[data-buy]').forEach(function (a) {
    var link = (window.BUROOQ_PAY || {})[a.getAttribute('data-buy')];
    if (link) a.href = link;
  });
  var calc = document.querySelector('.sw-calc');
  if (!calc) return;
  var ar = calc.getAttribute('data-lang') === 'ar', out = calc.querySelector('[data-total]'), btn = calc.querySelector('[data-order]');
  function update() {
    var setup = 0, renew = 0, names = [];
    calc.querySelectorAll('input[type=checkbox]:checked').forEach(function (c) {
      setup += +c.getAttribute('data-setup'); renew += +c.getAttribute('data-renew'); names.push(c.getAttribute('data-name'));
    });
    var usd = Math.round(setup / 3.6725);
    out.textContent = ar ? setup.toLocaleString('en-US') + ' درهم (≈ $' + usd + ')، ثم ' + renew + ' درهم سنوياً'
                         : setup.toLocaleString('en-US') + ' AED (≈ $' + usd + '), then ' + renew + ' AED a year';
    var msg = (ar ? 'مرحباً، أريد شراء: ' : 'Hi, I want to buy: ') + names.join(', ') + (ar ? ' — الإجمالي ' : ' — total ') + setup + ' AED';
    btn.href = 'https://wa.me/971544389066?text=' + encodeURIComponent(msg);
    btn.style.opacity = names.length ? 1 : .5;
  }
  calc.addEventListener('change', update); update();
})();
