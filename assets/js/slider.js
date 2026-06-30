// slider.js — minimal accessible carousel
(function(){
  document.querySelectorAll('[data-slider]').forEach(function(slider){
    var track = slider.querySelector('[data-slider-track]');
    var prev = slider.querySelector('[data-slider-prev]');
    var next = slider.querySelector('[data-slider-next]');
    if(!track) return;
    var scrollAmount = function(){ return track.clientWidth * 0.9; };
    if(next) next.addEventListener('click', function(){ track.scrollBy({left: scrollAmount(), behavior:'smooth'}); });
    if(prev) prev.addEventListener('click', function(){ track.scrollBy({left: -scrollAmount(), behavior:'smooth'}); });
  });
})();
