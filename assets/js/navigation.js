// navigation.js — mobile nav + dropdown handling (fixed for all screen sizes)
(function(){
  var toggle = document.querySelector('.nav-toggle');
  var nav    = document.querySelector('.main-nav');

  // ── Mobile hamburger toggle ──────────────────────────────────────────
  if(toggle && nav){
    toggle.addEventListener('click', function(e){
      e.stopPropagation();
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    });
  }

  // ── Dropdown: desktop hover handled by CSS.
  //    Mobile: tap the parent link to open/close the sub-list. ─────────
  document.querySelectorAll('.has-dropdown').forEach(function(item){
    var link    = item.querySelector(':scope > a');
    var submenu = item.querySelector(':scope > ul.dropdown');
    if(!link || !submenu) return;

    // Mobile tap
    link.addEventListener('click', function(e){
      if(window.innerWidth > 900) return;       // let desktop CSS handle it
      e.preventDefault();
      e.stopPropagation();
      var isOpen = item.classList.contains('open');
      // Close all other open dropdowns first
      document.querySelectorAll('.has-dropdown.open').forEach(function(other){
        if(other !== item) other.classList.remove('open');
      });
      item.classList.toggle('open', !isOpen);
    });
  });

  // ── Close mobile nav + dropdowns when clicking outside ───────────────
  document.addEventListener('click', function(e){
    if(!nav) return;
    if(!nav.contains(e.target) && e.target !== toggle){
      nav.classList.remove('open');
      document.querySelectorAll('.has-dropdown.open').forEach(function(d){
        d.classList.remove('open');
      });
    }
  });

  // ── Close on Escape key ───────────────────────────────────────────────
  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape'){
      nav && nav.classList.remove('open');
      document.querySelectorAll('.has-dropdown.open').forEach(function(d){
        d.classList.remove('open');
      });
    }
  });
})();
