/**
 * משקם הבית – קבלת לידים מהאתר
 * מוסיף כל פנייה מהטפסים לגיליון "לידים", כל לחיצה על וואטסאפ או חיוג לגיליון "לחיצות",
 * ושולח מייל על כל ליד חדש.
 *
 * הגדרה (פעם אחת):
 * 1. בגיליון "לידים - משקם הבית": תוספים > Apps Script.
 * 2. מוחקים את מה שיש בעורך ומדביקים את כל הקובץ הזה. שומרים.
 * 3. פריסה > פריסה חדשה > סוג: אפליקציית אינטרנט.
 *    הרצה בתור: אני. למי יש גישה: כל אחד.
 * 4. מאשרים את ההרשאות, ומעתיקים את הכתובת שמסתיימת ב־/exec.
 */

const SHEET_ID = '1GnPA6afCdKfvwg2faQ8mYEotuGaWW-YjfBbxfBhXmGY';
const NOTIFY_EMAIL = 'dandinn22@gmail.com';
const TZ = 'Asia/Jerusalem';

function clean_(v, max) {
  v = String(v == null ? '' : v).replace(/[\u0000-\u001f]/g, ' ').trim();
  if (/^[=+\-@]/.test(v)) v = "'" + v;           // מונע הזרקת נוסחאות לגיליון
  return v.slice(0, max || 200);
}

function today_() {
  const p = Utilities.formatDate(new Date(), TZ, 'yyyy,M,d');
  return '=DATE(' + p + ')';
}

function doGet() {
  return ContentService.createTextOutput('ok');
}

function doPost(e) {
  const p = (e && e.parameter) || {};
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const ss = SpreadsheetApp.openById(SHEET_ID);
    const time = Utilities.formatDate(new Date(), TZ, 'HH:mm');

    if (p.type === 'click') {
      ss.getSheetByName('לחיצות').appendRow([
        today_(), time,
        p.kind === 'phone' ? 'שיחת טלפון' : 'וואטסאפ',
        clean_(p.page, 150)
      ]);
      return json_({ ok: true });
    }

    if (p.website) return json_({ ok: true });       // מלכודת לרובוטים
    const name = clean_(p.name, 80);
    const phone = clean_(p.phone, 20).replace(/[^\d+\-\s]/g, '');
    if (!name || phone.replace(/\D/g, '').length < 9) return json_({ ok: false });

    const fromAds = p.gclid || p.gbraid || p.wbraid ||
      (String(p.utm_source).toLowerCase() === 'google' && /cpc|ppc|paid/i.test(p.utm_medium || ''));
    const source = fromAds ? 'גוגל אדס' : 'טופס באתר';

    const notes = [
      p.msg ? 'הודעה: ' + clean_(p.msg, 500) : '',
      'טופס: ' + clean_(p.form, 40),
      'עמוד: ' + clean_(p.page, 150),
      p.s ? 'שירות מהמודעה: ' + clean_(p.s, 40) : '',
      p.utm_campaign ? 'קמפיין: ' + clean_(p.utm_campaign, 80) : '',
      p.utm_term ? 'מילת חיפוש: ' + clean_(p.utm_term, 80) : ''
    ].filter(String).join(' | ');

    const sh = ss.getSheetByName('לידים');
    const id = sh.getLastRow();                      // שורה 1 היא הכותרות
    sh.appendRow([
      id, today_(), time, name, phone,
      clean_(p.city, 40), clean_(p.situation, 60), clean_(p.visit, 10),
      source, 'חדש', '', '', '', '', '',
      'לחזור ללקוח', today_(), notes
    ]);

    const rows = [
      ['שם', name], ['טלפון', phone], ['עיר', clean_(p.city, 40)],
      ['מה המצב', clean_(p.situation, 60)], ['בדיקה בבניין', clean_(p.visit, 10)],
      ['הודעה', clean_(p.msg, 500)], ['מקור', source], ['עמוד', clean_(p.page, 150)]
    ].filter(function (r) { return r[1]; });
    const html = '<div dir="rtl" style="font-family:Arial,sans-serif;font-size:15px">' +
      '<h2 style="color:#b4561f;margin:0 0 12px">ליד חדש מהאתר – משקם הבית</h2>' +
      '<table cellpadding="6" style="border-collapse:collapse">' +
      rows.map(function (r) {
        return '<tr><td style="font-weight:bold;border-bottom:1px solid #ddd">' + r[0] +
          '</td><td style="border-bottom:1px solid #ddd">' + escape_(r[1]) + '</td></tr>';
      }).join('') +
      '</table><p>באתר הבטחנו לחזור תוך שעה.</p>' +
      '<p><a href="https://docs.google.com/spreadsheets/d/' + SHEET_ID + '/edit">לגיליון הלידים</a></p></div>';
    MailApp.sendEmail({
      to: NOTIFY_EMAIL,
      subject: 'ליד חדש – משקם הבית – ' + name + ' ' + phone,
      htmlBody: html
    });
    return json_({ ok: true });
  } finally {
    lock.releaseLock();
  }
}

function escape_(s) {
  return String(s).replace(/[&<>"]/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
  });
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
