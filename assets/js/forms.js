// forms.js — client-side validation and submission feedback

/* ---- Newsletter / email collection ----------------------------------
   Every email signup is sent to:
   1) FormSubmit -> arrives in the Gmail inbox below (works today)
   2) MailerLite -> added to your list automatically, once you paste the
      numeric form ID (MailerLite > Forms > Embedded form > HTML code,
      look for .../jsonp/2426568/forms/XXXXXXXX/subscribe)            */
window.BUROOQ_NEWSLETTER = {
  formsubmit: 'https://formsubmit.co/ajax/mhsooq9@gmail.com',
  mailerliteAccount: '2426568',
  mailerliteFormId: ''   // e.g. '123456789012345678'
};
window.burooqSubscribe = function(email, source){
  var C = window.BUROOQ_NEWSLETTER, jobs = [];
  try { localStorage.setItem('burooq_email', email); } catch(e){}
  if(C.formsubmit){
    jobs.push(fetch(C.formsubmit, {method:'POST', headers:{'Content-Type':'application/json','Accept':'application/json'},
      body: JSON.stringify({email: email, source: source || 'website', page: location.href,
        _subject: 'New email subscriber (' + (source || 'website') + ') - burooq.net', _template: 'table'})}));
  }
  if(C.mailerliteFormId){
    var fd = new FormData(); fd.append('fields[email]', email); fd.append('ml-submit', '1'); fd.append('anticsrf', 'true');
    jobs.push(fetch('https://assets.mailerlite.com/jsonp/' + C.mailerliteAccount + '/forms/' + C.mailerliteFormId + '/subscribe',
      {method:'POST', body: fd, mode:'no-cors'}));
  }
  return Promise.allSettled(jobs).then(function(r){
    return r.some(function(x){ return x.status === 'fulfilled'; });
  });
};
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
        var em = form.querySelector('[type="email"],[name="email"]');
        if(em && em.value.trim()){
          var btn = form.querySelector('button[type="submit"]'); if(btn) btn.disabled = true;
          window.burooqSubscribe(em.value.trim(), 'footer-newsletter').then(function(ok){
            if(btn) btn.disabled = false;
            showMessage(form, ok ? 'success' : 'error', ok ? 'Thank you! You are subscribed to Alburooq offers and guides.' : 'Sorry, something went wrong. Please WhatsApp us on +971 54 438 9066.');
            if(ok) form.reset();
          });
          return;
        }
        showMessage(form, 'success', 'Thank you. Our team will contact you within one business hour.');
        form.reset();
      }
    });
  });
})();
