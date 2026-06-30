// forms.js — client-side validation and submission feedback
(function(){
  function showMessage(form, type, text){
    var existing = form.querySelector('.form-success, .form-error');
    if(existing) existing.remove();
    var box = document.createElement('div');
    box.className = type === 'success' ? 'form-success' : 'form-error';
    box.setAttribute('role', 'status');
    box.textContent = text;
    form.appendChild(box);
  }

  document.querySelectorAll('form[data-form]').forEach(function(form){
    form.addEventListener('submit', function(e){
      var name = form.querySelector('[name="name"]');
      var phone = form.querySelector('[name="phone"]');
      if(name && !name.value.trim()){
        e.preventDefault();
        showMessage(form, 'error', 'Please enter your name.');
        name.focus();
        return;
      }
      if(phone && !/^[0-9+\s-]{7,}$/.test(phone.value.trim())){
        e.preventDefault();
        showMessage(form, 'error', 'Please enter a valid phone number.');
        phone.focus();
        return;
      }
      // MailerLite / Formspree-style endpoints submit natively (action attr).
      // We show optimistic confirmation for forms without a configured backend.
      if(form.getAttribute('data-demo') === 'true'){
        e.preventDefault();
        showMessage(form, 'success', 'Thank you. Our team will contact you within one business hour.');
        form.reset();
      }
    });
  });
})();
