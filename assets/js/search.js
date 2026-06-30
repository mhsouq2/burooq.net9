// search.js — basic client-side filter for service/area listing pages
(function(){
  document.querySelectorAll('[data-search-input]').forEach(function(input){
    var targetSelector = input.getAttribute('data-search-input');
    var items = document.querySelectorAll(targetSelector);
    input.addEventListener('input', function(){
      var q = input.value.trim().toLowerCase();
      items.forEach(function(item){
        var text = item.textContent.toLowerCase();
        item.style.display = text.indexOf(q) > -1 ? '' : 'none';
      });
    });
  });
})();
