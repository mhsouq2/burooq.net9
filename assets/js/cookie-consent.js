/* Alburooq Smart Solutions — Cookie Consent Banner
   Self-contained: injects its own markup + styles, no CSS file changes needed.
   Stores choice in localStorage so it only shows once per visitor. */
(function () {
  var STORAGE_KEY = "burooq_cookie_consent";
  try {
    if (localStorage.getItem(STORAGE_KEY)) return;
  } catch (e) {
    return; // localStorage unavailable (private mode etc.) — skip banner rather than error
  }

  var isArabic = document.documentElement.lang === "ar";

  var text = isArabic
    ? "نستخدم ملفات تعريف الارتباط لتحسين تجربتك وعرض إعلانات ذات صلة. بمتابعة استخدام الموقع، فإنك توافق على"
    : "We use cookies to improve your experience and show relevant ads. By continuing to use this site, you agree to our";
  var linkLabel = isArabic ? "سياسة ملفات تعريف الارتباط" : "Cookie Policy";
  var linkHref = "/cookie-policy/";
  var acceptLabel = isArabic ? "موافق" : "Accept";
  var declineLabel = isArabic ? "رفض غير الضروري" : "Decline non-essential";

  var style = document.createElement("style");
  style.textContent =
    "#burooq-cookie-banner{position:fixed;left:0;right:0;bottom:0;z-index:9999;" +
    "background:#0A2A45;color:#fff;padding:1rem 1.25rem;display:flex;gap:1rem;" +
    "align-items:center;flex-wrap:wrap;justify-content:center;font-family:Inter,Tajawal,sans-serif;" +
    "font-size:.875rem;box-shadow:0 -2px 12px rgba(0,0,0,.15);}" +
    "#burooq-cookie-banner a{color:#9CC3EE;text-decoration:underline;}" +
    "#burooq-cookie-banner .bcc-actions{display:flex;gap:.6rem;flex-wrap:wrap;}" +
    "#burooq-cookie-banner button{border:none;border-radius:6px;padding:.5rem 1rem;font-size:.85rem;cursor:pointer;font-weight:600;}" +
    "#burooq-cookie-banner .bcc-accept{background:#E8A33D;color:#0A2A45;}" +
    "#burooq-cookie-banner .bcc-decline{background:transparent;color:#fff;border:1px solid rgba(255,255,255,.4)!important;}" +
    "@media (max-width:600px){#burooq-cookie-banner{flex-direction:column;text-align:center;}}";
  document.head.appendChild(style);

  var banner = document.createElement("div");
  banner.id = "burooq-cookie-banner";
  banner.setAttribute("role", "region");
  banner.setAttribute("aria-label", isArabic ? "إشعار ملفات تعريف الارتباط" : "Cookie notice");
  banner.innerHTML =
    "<span>" + text + ' <a href="' + linkHref + '">' + linkLabel + "</a>.</span>" +
    '<span class="bcc-actions">' +
    '<button class="bcc-decline" type="button" data-choice="declined">' + declineLabel + "</button>" +
    '<button class="bcc-accept" type="button" data-choice="accepted">' + acceptLabel + "</button>" +
    "</span>";

  document.addEventListener("DOMContentLoaded", function () {
    document.body.appendChild(banner);
    banner.querySelectorAll("button").forEach(function (btn) {
      btn.addEventListener("click", function () {
        try {
          localStorage.setItem(STORAGE_KEY, btn.getAttribute("data-choice"));
        } catch (e) {}
        banner.remove();
      });
    });
  });
})();
