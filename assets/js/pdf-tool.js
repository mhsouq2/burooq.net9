/* Burooq PDF Converter — runs 100% in the browser (files are never uploaded).
   Free plan: requires an email once; limited files and daily conversions.
   Pro plan: unlimited, no footer stamp. Unlocked with an access code.      */
(function () {
  'use strict';

  /* ===================== SETTINGS (edit these) ===================== */
  var CFG = {
    freeImages: 5,          // max images per PDF on free plan
    freeMerge: 3,           // max PDFs to merge on free plan
    freeDaily: 5,           // conversions per day on free plan
    proPrice: 'AED 19 / month',
    // Paste your Payhip (or other) subscription checkout link here.
    // If empty, the "Go Pro" button opens WhatsApp so you can sell manually.
    proCheckoutUrl: '',
    whatsapp: '971544389066',
    // SHA-256 hashes of valid Pro access codes. Add a new hash each month
    // and remove old ones to expire them (see README note in the zip).
    proCodeHashes: ['192db046e33155c0a7c19597539bf3ebe61ec2b976bab4a108fa8d7c6a8b373b'],
    stamp: 'Created free with burooq.net/tools/pdf-converter'
  };
  /* ================================================================== */

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  var isPro = function () { return store.get('burooq_pdf_pro') === '1'; };
  var hasEmail = function () { return !!store.get('burooq_email'); };
  var today = new Date().toISOString().slice(0, 10);
  var usedToday = function () { return store.get('burooq_pdf_day') === today ? parseInt(store.get('burooq_pdf_count') || '0', 10) : 0; };
  var countUse = function () { store.set('burooq_pdf_day', today); store.set('burooq_pdf_count', String(usedToday() + 1)); };

  function msg(el, text, type) {
    el.textContent = text; el.className = 'pdf-msg ' + (type || ''); el.hidden = !text;
  }
  function track(name) { try { if (window.gtag) gtag('event', name); } catch (e) {} }

  function refreshPlan() {
    var pro = isPro();
    $$('[data-plan-label]').forEach(function (el) {
      el.textContent = pro ? 'Pro plan — unlimited' :
        'Free plan — ' + (CFG.freeDaily - usedToday()) + ' of ' + CFG.freeDaily + ' conversions left today';
    });
    $$('[data-free-only]').forEach(function (el) { el.hidden = pro; });
    $$('[data-pro-price]').forEach(function (el) { el.textContent = CFG.proPrice; });
  }

  /* Gate: returns true if the user may convert now; otherwise shows the right panel. */
  function canConvert(count, limit, out) {
    if (isPro()) return true;
    if (!hasEmail()) { $('#pdf-email-gate').hidden = false; $('#pdf-email').focus(); $('#pdf-email-gate').scrollIntoView({ behavior: 'smooth', block: 'center' }); return false; }
    if (usedToday() >= CFG.freeDaily) { msg(out, 'You have used today\'s free conversions. Go Pro for unlimited use, or come back tomorrow.', 'error'); showPro(); return false; }
    if (count > limit) { msg(out, 'The free plan allows up to ' + limit + ' files at once. Remove some files or go Pro for unlimited.', 'error'); showPro(); return false; }
    return true;
  }
  function showPro() { var p = $('#pdf-pro'); p.hidden = false; p.scrollIntoView({ behavior: 'smooth', block: 'center' }); }

  function download(bytes, name) {
    var blob = new Blob([bytes], { type: 'application/pdf' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = name;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 4000);
  }

  function readAsArrayBuffer(file) {
    return new Promise(function (res, rej) { var r = new FileReader(); r.onload = function () { res(r.result); }; r.onerror = rej; r.readAsArrayBuffer(file); });
  }
  // Convert any browser-readable image to JPEG bytes (handles WebP, HEIC-less browsers fall back gracefully)
  function imageToJpeg(file) {
    return new Promise(function (res, rej) {
      var img = new Image(), url = URL.createObjectURL(file);
      img.onload = function () {
        var c = document.createElement('canvas'); c.width = img.naturalWidth; c.height = img.naturalHeight;
        var ctx = c.getContext('2d'); ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, c.width, c.height); ctx.drawImage(img, 0, 0);
        URL.revokeObjectURL(url);
        c.toBlob(function (b) { b.arrayBuffer().then(function (buf) { res({ bytes: buf, w: c.width, h: c.height }); }); }, 'image/jpeg', 0.92);
      };
      img.onerror = function () { URL.revokeObjectURL(url); rej(new Error('Cannot read image: ' + file.name)); };
      img.src = url;
    });
  }

  var SIZES = { a4: [595.28, 841.89], letter: [612, 792] };

  function addStamp(page, font) {
    if (isPro()) return;
    page.drawText(CFG.stamp, { x: 20, y: 10, size: 7, font: font, color: PDFLib.rgb(0.55, 0.55, 0.55) });
  }

  /* ------------------------- Images → PDF ------------------------- */
  var images = [];
  function renderImageList() {
    var list = $('#img-list'); list.innerHTML = '';
    images.forEach(function (f, i) {
      var li = document.createElement('li');
      li.innerHTML = '<span>' + (i + 1) + '. </span><span class="pdf-name"></span>' +
        '<button type="button" data-mv="-1" aria-label="Move up">↑</button>' +
        '<button type="button" data-mv="1" aria-label="Move down">↓</button>' +
        '<button type="button" data-rm aria-label="Remove">✕</button>';
      li.querySelector('.pdf-name').textContent = f.name;
      li.querySelector('[data-rm]').onclick = function () { images.splice(i, 1); renderImageList(); };
      $$('[data-mv]', li).forEach(function (b) {
        b.onclick = function () { var j = i + parseInt(b.getAttribute('data-mv'), 10); if (j < 0 || j >= images.length) return; var t = images[i]; images[i] = images[j]; images[j] = t; renderImageList(); };
      });
      list.appendChild(li);
    });
    $('#img-convert').disabled = !images.length;
  }
  function addImages(files) {
    Array.prototype.forEach.call(files, function (f) { if (/^image\//.test(f.type)) images.push(f); });
    renderImageList();
  }

  function imagesToPdf() {
    var out = $('#img-msg');
    if (!canConvert(images.length, CFG.freeImages, out)) return;
    msg(out, 'Creating your PDF…');
    var size = $('#img-size').value, margin = parseInt($('#img-margin').value, 10);
    PDFLib.PDFDocument.create().then(function (doc) {
      return doc.embedFont(PDFLib.StandardFonts.Helvetica).then(function (font) {
        var chain = Promise.resolve();
        images.forEach(function (f) {
          chain = chain.then(function () { return imageToJpeg(f); }).then(function (im) {
            return doc.embedJpg(im.bytes).then(function (jpg) {
              var pw, ph;
              if (size === 'fit') { pw = im.w * 0.75 + margin * 2; ph = im.h * 0.75 + margin * 2; }
              else { var s = SIZES[size]; var land = im.w > im.h; pw = land ? s[1] : s[0]; ph = land ? s[0] : s[1]; }
              var page = doc.addPage([pw, ph]);
              var scale = Math.min((pw - margin * 2) / jpg.width, (ph - margin * 2) / jpg.height);
              var w = jpg.width * scale, h = jpg.height * scale;
              page.drawImage(jpg, { x: (pw - w) / 2, y: (ph - h) / 2, width: w, height: h });
              addStamp(page, font);
            });
          });
        });
        return chain.then(function () { return doc.save(); });
      });
    }).then(function (bytes) {
      download(bytes, 'images-burooq.pdf'); countUse(); refreshPlan(); track('pdf_images_converted');
      msg(out, 'Done! Your PDF has downloaded.', 'success');
    }).catch(function (e) { msg(out, 'Error: ' + e.message, 'error'); });
  }

  /* -------------------------- Text → PDF -------------------------- */
  // Rendered via canvas so Arabic and any language display correctly.
  function textToPdf() {
    var out = $('#txt-msg'), text = $('#txt-input').value;
    if (!text.trim()) { msg(out, 'Please type or paste some text first.', 'error'); return; }
    if (!canConvert(1, 1, out)) return;
    msg(out, 'Creating your PDF…');
    var W = 1240, H = 1754, M = 110, FS = 30, LH = 46; // A4 at 150 dpi
    var c = document.createElement('canvas'); c.width = W; c.height = H;
    var ctx = c.getContext('2d');
    var font = FS + 'px Tajawal, Inter, Arial, sans-serif';
    ctx.font = font;
    var lines = [];
    text.split('\n').forEach(function (para) {
      var words = para.split(/\s+/), line = '';
      var rtl = /[\u0600-\u06FF]/.test(para);
      if (!para.trim()) { lines.push({ t: '', rtl: false }); return; }
      words.forEach(function (w) {
        var t = line ? line + ' ' + w : w;
        if (ctx.measureText(t).width > W - M * 2 && line) { lines.push({ t: line, rtl: rtl }); line = w; } else line = t;
      });
      lines.push({ t: line, rtl: rtl });
    });
    var perPage = Math.floor((H - M * 2) / LH), pages = [];
    for (var i = 0; i < lines.length; i += perPage) pages.push(lines.slice(i, i + perPage));
    PDFLib.PDFDocument.create().then(function (doc) {
      return doc.embedFont(PDFLib.StandardFonts.Helvetica).then(function (hf) {
        var chain = Promise.resolve();
        pages.forEach(function (pl) {
          chain = chain.then(function () {
            ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, W, H); ctx.fillStyle = '#111';
            ctx.font = font; ctx.textBaseline = 'top';
            pl.forEach(function (ln, k) { ctx.direction = ln.rtl ? 'rtl' : 'ltr'; ctx.textAlign = ln.rtl ? 'right' : 'left'; ctx.fillText(ln.t, ln.rtl ? W - M : M, M + k * LH); });
            return new Promise(function (res) { c.toBlob(function (b) { b.arrayBuffer().then(res); }, 'image/png'); });
          }).then(function (png) {
            return doc.embedPng(png).then(function (img) {
              var page = doc.addPage(SIZES.a4);
              page.drawImage(img, { x: 0, y: 0, width: SIZES.a4[0], height: SIZES.a4[1] });
              addStamp(page, hf);
            });
          });
        });
        return chain.then(function () { return doc.save(); });
      });
    }).then(function (bytes) {
      download(bytes, 'text-burooq.pdf'); countUse(); refreshPlan(); track('pdf_text_converted');
      msg(out, 'Done! Your PDF has downloaded.', 'success');
    }).catch(function (e) { msg(out, 'Error: ' + e.message, 'error'); });
  }

  /* -------------------------- Merge PDFs -------------------------- */
  var pdfs = [];
  function renderPdfList() {
    var list = $('#merge-list'); list.innerHTML = '';
    pdfs.forEach(function (f, i) {
      var li = document.createElement('li');
      li.innerHTML = '<span>' + (i + 1) + '. </span><span class="pdf-name"></span><button type="button" data-mv="-1" aria-label="Move up">↑</button><button type="button" data-mv="1" aria-label="Move down">↓</button><button type="button" data-rm aria-label="Remove">✕</button>';
      li.querySelector('.pdf-name').textContent = f.name;
      li.querySelector('[data-rm]').onclick = function () { pdfs.splice(i, 1); renderPdfList(); };
      $$('[data-mv]', li).forEach(function (b) {
        b.onclick = function () { var j = i + parseInt(b.getAttribute('data-mv'), 10); if (j < 0 || j >= pdfs.length) return; var t = pdfs[i]; pdfs[i] = pdfs[j]; pdfs[j] = t; renderPdfList(); };
      });
      list.appendChild(li);
    });
    $('#merge-convert').disabled = pdfs.length < 2;
  }
  function mergePdfs() {
    var out = $('#merge-msg');
    if (!canConvert(pdfs.length, CFG.freeMerge, out)) return;
    msg(out, 'Merging…');
    PDFLib.PDFDocument.create().then(function (doc) {
      var chain = Promise.resolve();
      pdfs.forEach(function (f) {
        chain = chain.then(function () { return readAsArrayBuffer(f); })
          .then(function (buf) { return PDFLib.PDFDocument.load(buf, { ignoreEncryption: true }); })
          .then(function (src) { return doc.copyPages(src, src.getPageIndices()); })
          .then(function (pages) { pages.forEach(function (p) { doc.addPage(p); }); });
      });
      return chain.then(function () {
        return doc.embedFont(PDFLib.StandardFonts.Helvetica).then(function (font) {
          if (!isPro()) doc.getPages().forEach(function (p) { addStamp(p, font); });
          return doc.save();
        });
      });
    }).then(function (bytes) {
      download(bytes, 'merged-burooq.pdf'); countUse(); refreshPlan(); track('pdf_merged');
      msg(out, 'Done! Your merged PDF has downloaded.', 'success');
    }).catch(function (e) { msg(out, 'Could not merge: ' + e.message + ' (password-protected PDFs are not supported).', 'error'); });
  }

  /* ---------------------- Email gate & Pro ------------------------ */
  function sha256(s) {
    return crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)).then(function (b) {
      return Array.prototype.map.call(new Uint8Array(b), function (x) { return ('0' + x.toString(16)).slice(-2); }).join('');
    });
  }

  function init() {
    if (!window.PDFLib) { $$('.pdf-msg').forEach(function (m) { msg(m, 'The converter could not load. Please refresh the page.', 'error'); }); return; }
    // tabs
    $$('[data-tab]').forEach(function (t) {
      t.onclick = function () {
        $$('[data-tab]').forEach(function (x) { x.setAttribute('aria-selected', x === t ? 'true' : 'false'); });
        $$('[data-panel]').forEach(function (p) { p.hidden = p.getAttribute('data-panel') !== t.getAttribute('data-tab'); });
      };
    });
    // images
    var drop = $('#img-drop'), inp = $('#img-input');
    inp.onchange = function () { addImages(inp.files); inp.value = ''; };
    ['dragover', 'dragenter'].forEach(function (ev) { drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.add('is-over'); }); });
    ['dragleave', 'drop'].forEach(function (ev) { drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.remove('is-over'); }); });
    drop.addEventListener('drop', function (e) { addImages(e.dataTransfer.files); });
    $('#img-convert').onclick = imagesToPdf;
    // text
    $('#txt-convert').onclick = textToPdf;
    // merge
    var mi = $('#merge-input');
    mi.onchange = function () { Array.prototype.forEach.call(mi.files, function (f) { if (f.type === 'application/pdf' || /\.pdf$/i.test(f.name)) pdfs.push(f); }); mi.value = ''; renderPdfList(); };
    $('#merge-convert').onclick = mergePdfs;

    // email gate
    $('#pdf-email-form').onsubmit = function (e) {
      e.preventDefault();
      var em = $('#pdf-email').value.trim(), out = $('#pdf-email-msg');
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(em)) { msg(out, 'Please enter a valid email address.', 'error'); return; }
      var btn = $('#pdf-email-form button'); btn.disabled = true;
      var done = function () { btn.disabled = false; store.set('burooq_email', em); $('#pdf-email-gate').hidden = true; refreshPlan(); track('pdf_email_signup'); };
      if (window.burooqSubscribe) window.burooqSubscribe(em, 'pdf-converter').then(done, done); else done();
    };

    // Pro
    var wa = 'https://wa.me/' + CFG.whatsapp + '?text=' + encodeURIComponent('Hi Alburooq, I want the PDF Converter Pro subscription (' + CFG.proPrice + ').');
    $$('[data-go-pro]').forEach(function (a) { a.href = CFG.proCheckoutUrl || wa; a.onclick = function () { track('pdf_go_pro_click'); }; });
    $$('[data-show-pro]').forEach(function (b) { b.onclick = showPro; });
    $('#pro-code-form').onsubmit = function (e) {
      e.preventDefault();
      var code = $('#pro-code').value.trim().toUpperCase(), out = $('#pro-code-msg');
      sha256(code).then(function (h) {
        if (CFG.proCodeHashes.indexOf(h) > -1) { store.set('burooq_pdf_pro', '1'); refreshPlan(); msg(out, 'Pro activated on this browser. Enjoy unlimited conversions!', 'success'); track('pdf_pro_activated'); }
        else msg(out, 'That code is not valid. Check it, or WhatsApp us on +971 54 438 9066.', 'error');
      });
    };
    refreshPlan();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
