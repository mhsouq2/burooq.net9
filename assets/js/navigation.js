// navigation.js — mobile nav toggle + dropdown handling
(function(){
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.main-nav');
  if(toggle && nav){
    toggle.addEventListener('click', function(){
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open);
    });
  }
  document.querySelectorAll('.has-dropdown > a').forEach(function(link){
    link.addEventListener('click', function(e){
      if(window.innerWidth <= 900){
        e.preventDefault();
        link.parentElement.classList.toggle('open');
      }
    });
  });
  // Close mobile nav on outside click
  document.addEventListener('click', function(e){
    if(nav && nav.classList.contains('open') && !nav.contains(e.target) && e.target !== toggle){
      nav.classList.remove('open');
    }
  });
})();
