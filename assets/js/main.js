// main.js — global behaviors: scroll reveal, dynamic year, lazy images
(function(){
  // Footer year
  var yearEl = document.querySelector('[data-year]');
  if(yearEl) yearEl.textContent = new Date().getFullYear();

  // Scroll reveal
  var targets = document.querySelectorAll('.reveal');
  if('IntersectionObserver' in window && targets.length){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if(entry.isIntersecting){
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, {threshold:0.15});
    targets.forEach(function(t){ io.observe(t); });
  } else {
    targets.forEach(function(t){ t.classList.add('is-visible'); });
  }

  // Lazy image fade-in
  document.querySelectorAll('img[loading="lazy"]').forEach(function(img){
    img.classList.add('lazy');
    if(img.complete){ img.classList.add('loaded'); }
    img.addEventListener('load', function(){ img.classList.add('loaded'); });
  });
})();
