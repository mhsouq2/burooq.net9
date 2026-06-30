// analytics.js — lightweight event tracking hooks
// Replace GA_MEASUREMENT_ID with the real GA4 ID before launch.
(function(){
  window.trackEvent = function(action, params){
    if(typeof gtag === 'function'){
      gtag('event', action, params || {});
    }
  };
  document.querySelectorAll('[data-track]').forEach(function(el){
    el.addEventListener('click', function(){
      window.trackEvent(el.getAttribute('data-track'), {label: el.textContent.trim()});
    });
  });
})();
