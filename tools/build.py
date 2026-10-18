# -*- coding: utf-8 -*-
import sys,os,json,re,html
sys.path.insert(0,os.path.dirname(__file__))
from cities import CITIES
from guides import GUIDES
R=sys.argv[1]; DOMAIN="https://meshakemhabayit.com"
src=open(f"{R}/index.html",encoding="utf-8").read()
css=src[src.index("<style>")+7:src.index("</style>")]
os.makedirs(f"{R}/assets",exist_ok=True)
open(f"{R}/assets/site.css","w",encoding="utf-8").write(css)
header=src[src.index("<header>"):src.index('<div class="tape" aria-hidden="true"></div>')+len('<div class="tape" aria-hidden="true"></div>')]
header=header.replace('href="#top"','href="/"').replace('href="#','href="/#')
footer=src[src.index("<footer>"):src.index("</footer>")+9]
footer=footer.replace('href="privacy.html"','href="/privacy.html"').replace('href="accessibility.html"','href="/accessibility.html"')
mbar=src[src.index('<div class="mbar">'):src.index('</div>',src.index('<div class="mbar">'))+6]
mbar=mbar.replace('href="#','href="/#')
WA=src[src.index('<a class="btn btn-whats btn-xl"'):src.index('</a>',src.index('<a class="btn btn-whats btn-xl"'))+4]
STEPS=[("שולחים תמונות","תמונות של הליקויים ומכתב העירייה בוואטסאפ, ומקבלים הערכה ראשונית בחינם תוך שעה."),
 ("בדיקה בבניין בחינם","מגיעים לבניין, ממפים את כל הליקויים ונותנים הצעת מחיר מפורטת לפי סעיפים."),
 ("תיאום עם העירייה","מפרט מהנדס, ביטוח והגשת המסמכים למחלקת המבנים המסוכנים בעירייה."),
 ("ביצוע העבודה","פיגום, סנפלינג או במת הרמה, עם עדכון לוועד הבית בכל שלב."),
 ("הסרת הצו","המהנדס חותם על חוות דעת, ואנחנו מלווים מול העירייה עד שהצו מוסר.")]
def page(c):
    n=c["name"]; esc=html.escape
    title=f"שיקום מבנים מסוכנים ב{n} | הסרת צו מבנה מסוכן | משקם הבית"
    desc=f"שיקום וחיזוק מבנים ב{n}: הסרת צו מבנה מסוכן, שיקום עמודים ומרפסות. 16 שנות ניסיון, הערכה ובדיקה בבניין בחינם. שלחו תמונה ונחזור תוך שעה."
    url=f"{DOMAIN}/shikum-mivnim/{c['slug']}/"
    faqs=c["faq"]+[(f"כמה עולה שיקום מבנה ב{n}?","המחיר תלוי במספר הליקויים, בגובה הבניין ובדרך הגישה. אחרי שתשלחו תמונות ניתן טווח מחיר ראשוני בחינם, והצעה מדויקת אחרי בדיקה בבניין, שגם היא בחינם.")]
    ld=[{"@context":"https://schema.org","@type":"GeneralContractor","name":"משקם הבית","url":DOMAIN+"/","telephone":"+972-50-555-0182","areaServed":{"@type":"City","name":n},
         "description":f"שיקום וחיזוק מבנים והסרת צו מבנה מסוכן ב{n}"},
        {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
          {"@type":"ListItem","position":1,"name":"דף הבית","item":DOMAIN+"/"},
          {"@type":"ListItem","position":2,"name":f"שיקום מבנים ב{n}","item":url}]}]
    defects="".join(f'<div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t,d in c["defects"])
    hoods="".join(f"<li><span>{esc(h)}</span></li>" for h in c["hoods"])
    steps="".join(f"<li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>" for t,d in STEPS)
    faqh="".join(f"<details{' open' if i==0 else ''}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for i,(q,a) in enumerate(faqs))
    gl="".join(f'<li><a href="/madrich/{g["slug"]}/">{esc(g["title"])}</a></li>' for g in GUIDES)
    others="".join(f'<li><a href="/shikum-mivnim/{o["slug"]}/">שיקום מבנים ב{esc(o["name"])}</a></li>' for o in CITIES if o is not c)
    return f'''<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{DOMAIN}/img/hero.jpg">
<meta property="og:locale" content="he_IL">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Secular+One&family=Assistant:wght@400;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/site.css">
<style>
.crumbs{{font-size:14px;color:rgba(255,255,255,.8);margin-bottom:12px}}
.crumbs a{{color:inherit}}
.city-intro{{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,.8fr);gap:32px;align-items:start}}
@media (max-width:820px){{.city-intro{{grid-template-columns:1fr}}}}
.city-intro p+p{{margin-top:14px}}
.city-intro p{{font-size:17.5px;max-width:62ch}}
.city-intro figure{{margin:0}}
.city-intro img{{display:block;width:100%;height:auto;border-radius:10px;border:1px solid var(--line)}}
.city-intro figcaption{{font-size:13px;color:var(--muted);margin-top:6px}}
.hoods{{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0;margin:0}}
.hoods span{{display:inline-block;padding:6px 14px;border:1px solid var(--line);border-radius:99px;background:var(--surface);font-weight:600;font-size:15px}}
</style>
{"".join('<script type="application/ld+json">'+json.dumps(x,ensure_ascii=False)+'</script>' for x in ld)}
</head>
<body>
<div lang="he" dir="rtl">
{header}
<main>
<section class="hx">
  <img class="hx-bg" src="/img/hero.jpg" width="1920" height="1085" alt="צוות שיקום ומהנדס בודקים עיבוי עמוד בטון בבניין מגורים ב{esc(n)}" fetchpriority="high">
  <div class="hx-shade" aria-hidden="true"></div>
  <div class="wrap hx-grid">
    <div class="hx-copy">
      <nav class="crumbs" aria-label="מיקום בעמוד"><a href="/">דף הבית</a> › שיקום מבנים ב{esc(n)}</nav>
      <span class="hx-alert">קיבלתם צו מבנה מסוכן ב{esc(n)}? יש לכם מועד אחרון לתיקון</span>
      <h1>שיקום מבנים מסוכנים <span class="hl">ב{esc(n)}</span></h1>
      <p class="hx-lead">16 שנה אנחנו משקמים עמודים, מרפסות וחזיתות בבניינים ב{esc(n)}, ומלווים את הדיירים מול העירייה עד שהצו מוסר.</p>
      <div class="hx-cta">
        {WA}
        <a class="btn btn-light btn-xl" href="/#contact"><span>תאמו בדיקה בבניין<small>בחינם וללא התחייבות</small></span></a>
      </div>
      <ul class="hx-trust"><li><b>16</b> שנות ניסיון</li><li><b>✓</b> מהנדס מלווה בביצוע</li><li><b>✓</b> מענה תוך שעה</li></ul>
    </div>
  </div>
</section>

<section>
  <div class="wrap city-intro">
    <div>
      <h2 style="font-size:clamp(26px,3.4vw,36px);margin-bottom:14px">שיקום מבנים ב{esc(n)}: מה מיוחד בבניינים בעיר</h2>
      <p>{esc(c["intro"])}</p>
      <p>{esc(c["local"])}</p>
    </div>
    <figure><img src="/img/column.jpg" width="900" height="605" alt="עמוד בטון עם ברזל זיון חלוד וחשוף, ליקוי נפוץ בבניינים ותיקים ב{esc(n)}" loading="lazy"><figcaption>עמוד עם ברזל חשוף: הליקוי הנפוץ ביותר בצווי מבנה מסוכן.</figcaption></figure>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="sec-head"><h2>הליקויים הנפוצים בבניינים ב{esc(n)}</h2><p>אלה הליקויים שאנחנו פוגשים הכי הרבה בבדיקות בעיר. כל אחד מהם יכול להוביל לצו מבנה מסוכן.</p></div>
    <div class="why">{defects}</div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="sec-head"><h2>שכונות שאנחנו עובדים בהן ב{esc(n)}</h2><p>אנחנו מגיעים לכל השכונות בעיר. אלה חלק מהאזורים שבהם יש הכי הרבה בניינים ותיקים.</p></div>
    <ul class="hoods">{hoods}</ul>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="sec-head"><h2>איך מסירים צו מבנה מסוכן ב{esc(n)}</h2><p>אנחנו מלווים את הדיירים בכל שלב, כדי שלא תצטרכו להתעסק עם הבירוקרטיה בעצמכם.</p></div>
    <ol class="steps">{steps}</ol>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="sec-head"><h2>שאלות נפוצות על שיקום מבנים ב{esc(n)}</h2></div>
    <div class="faq">{faqh}</div>
  </div>
</section>

<section class="band" id="contact-city">
  <div class="wrap" style="display:grid;gap:16px;max-width:760px">
    <h2 style="font-size:clamp(26px,3.4vw,38px)">גרים ב{esc(n)} וקיבלתם צו? שלחו תמונה וקבלו הערכה בחינם</h2>
    <p style="color:color-mix(in srgb,var(--band-ink) 80%,transparent)">שלחו 3 תמונות של הליקויים ואת מכתב העירייה, ונחזור אליכם תוך שעה עם הערכה ראשונית. ההערכה והבדיקה בבניין בחינם וללא התחייבות.</p>
    <div style="display:flex;flex-wrap:wrap;gap:12px">{WA}<a class="btn btn-light btn-xl" href="tel:+972505550182"><span>חייגו 050-555-0182<small>מענה מיידי</small></span></a></div>
  </div>
</section>

<section style="padding-bottom:0">
  <div class="wrap">
    <div class="sec-head"><h2>מדריכים שימושיים</h2></div>
    <ul class="cities">{gl}</ul>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head"><h2>שיקום מבנים בערים נוספות במרכז</h2></div>
    <ul class="cities">{others}</ul>
  </div>
</section>
</main>
{footer}
{mbar}
</div>
<script src="/assets/leads.js"></script>
</body>
</html>
'''
for c in CITIES:
    d=f"{R}/shikum-mivnim/{c['slug']}"; os.makedirs(d,exist_ok=True)
    open(f"{d}/index.html","w",encoding="utf-8").write(page(c))
# sitemap + robots
urls=[DOMAIN+"/"]+[f"{DOMAIN}/shikum-mivnim/{c['slug']}/" for c in CITIES]+[DOMAIN+"/privacy.html",DOMAIN+"/accessibility.html"]
open(f"{R}/sitemap.xml","w",encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"  <url><loc>{u}</loc><lastmod>2026-10-18</lastmod></url>\n" for u in urls)+"</urlset>\n")
open(f"{R}/robots.txt","w").write(f"User-agent: *\nAllow: /\nDisallow: /toda/\n\nSitemap: {DOMAIN}/sitemap.xml\n")
print("built",len(CITIES))
