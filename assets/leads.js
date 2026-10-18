/* משקם הבית – שליחת לידים ולחיצות לגיליון הלידים */
(function () {
  // הכתובת של סקריפט גוגל (מסתיימת ב־/exec). כל עוד היא ריקה, הטפסים לא שולחים.
  var LEAD_URL = '';

  var KEYS = ['gclid', 'gbraid', 'wbraid', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 's', 'c'];
  var q = new URLSearchParams(location.search);
  try {
    KEYS.forEach(function (k) { if (q.get(k)) sessionStorage.setItem('mh_' + k, q.get(k)); });
  } catch (e) {}

  function attribution() {
    var o = {};
    KEYS.forEach(function (k) {
      var v = q.get(k);
      if (!v) { try { v = sessionStorage.getItem('mh_' + k); } catch (e) {} }
      if (v) o[k] = v;
    });
    return o;
  }

  function post(data) {
    data.page = location.pathname;
    var a = attribution();
    for (var k in a) if (!(k in data)) data[k] = a[k];
    var body = new URLSearchParams(data);
    if (!LEAD_URL) return Promise.reject(new Error('not configured'));
    if (data.type === 'click' && navigator.sendBeacon) {
      navigator.sendBeacon(LEAD_URL, body);
      return Promise.resolve();
    }
    return fetch(LEAD_URL, { method: 'POST', mode: 'no-cors', body: body, keepalive: true });
  }

  function ga(name, params) {
    try { if (typeof window.gtag === 'function') window.gtag('event', name, params || {}); } catch (e) {}
  }

  window.sendLead = function (data) {
    data.type = 'lead';
    return post(data).then(function () {
      return new Promise(function (done) {
        var finished = false;
        function go() { if (!finished) { finished = true; done(); location.href = '/toda/'; } }
        ga('generate_lead', { form_name: data.form || '', event_callback: go });
        setTimeout(go, 800);
      });
    });
  };

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="tel:"], a[href*="wa.me/"]');
    if (!a) return;
    var isPhone = a.getAttribute('href').indexOf('tel:') === 0;
    ga(isPhone ? 'click_call' : 'click_whatsapp', { page_path: location.pathname });
    post({ type: 'click', kind: a.getAttribute('href').indexOf('tel:') === 0 ? 'phone' : 'whatsapp' }).catch(function () {});
  }, true);
})();
