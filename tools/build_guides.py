# -*- coding: utf-8 -*-
import sys,os,json,html
sys.path.insert(0,os.path.dirname(__file__))
from guides import GUIDES
from cities import CITIES
R=sys.argv[1]; DOMAIN="https://meshakemhabayit.com"; esc=html.escape
src=open(f"{R}/index.html",encoding="utf-8").read()
header=src[src.index("<header>"):src.index('<div class="tape" aria-hidden="true"></div>')+len('<div class="tape" aria-hidden="true"></div>')]
header=header.replace('href="#top"','href="/"').replace('href="#','href="/#')
footer=src[src.index("<footer>"):src.index("</footer>")+9].replace('href="privacy.html"','href="/privacy.html"').replace('href="accessibility.html"','href="/accessibility.html"')
mbar=src[src.index('<div class="mbar">'):src.index('</div>',src.index('<div class="mbar">'))+6].replace('href="#','href="/#')
WA=src[src.index('<a class="btn btn-whats btn-xl"'):src.index('</a>',src.index('<a class="btn btn-whats btn-xl"'))+4]
HEAD='''<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{img}">
<meta property="og:locale" content="he_IL">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Secular+One&family=Assistant:wght@400;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/site.css">
<style>
.g-hero{{background:var(--band);color:var(--band-ink);padding-block:40px 32px}}
.g-hero .crumbs{{font-size:14px;opacity:.8;margin-bottom:10px}}
.g-hero .crumbs a{{color:inherit}}
.g-hero h1{{font-size:clamp(30px,4.4vw,48px);max-width:22ch}}
.g-meta{{margin-top:10px;font-size:14.5px;opacity:.8}}
.g-wrap{{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:40px;align-items:start;padding-block:36px 24px}}
@media (max-width:900px){{.g-wrap{{grid-template-columns:1fr}}.g-side{{order:-1}}}}
.g-art{{max-width:68ch}}
.g-art .lead{{font-size:19px;line-height:1.7}}
.g-art figure{{margin:22px 0}}
.g-art img{{display:block;width:100%;height:auto;border-radius:10px;border:1px solid var(--line)}}
.g-art figcaption{{font-size:13px;color:var(--muted);margin-top:6px}}
.g-art h2{{font-size:clamp(24px,3vw,30px);margin:34px 0 10px;scroll-margin-top:90px}}
.g-art p{{margin:0 0 12px;font-size:17.5px;line-height:1.75}}
.g-art ul,.g-art ol{{margin:0 0 14px;padding-inline-start:22px;display:grid;gap:8px;font-size:17px;line-height:1.7}}
.g-cta{{margin:28px 0;padding:20px;border-radius:10px;background:var(--rebar-soft);display:grid;gap:12px}}
.g-cta b{{font-family:var(--f-display);font-weight:400;font-size:22px;color:var(--rebar)}}
.g-cta div{{display:flex;flex-wrap:wrap;gap:10px}}
.g-side{{position:sticky;top:96px;display:grid;gap:16px}}
@media (max-width:900px){{.g-side{{position:static}}}}
.toc{{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:16px 18px}}
.toc b{{font-family:var(--f-display);font-weight:400;font-size:18px}}
.toc ol{{margin:8px 0 0;padding-inline-start:20px;display:grid;gap:6px;font-size:15px}}
.toc a{{text-decoration:none}}
.toc a:hover{{color:var(--rebar)}}
.side-cta{{background:var(--band);color:var(--band-ink);border-radius:10px;padding:18px;display:grid;gap:10px}}
.side-cta b{{font-family:var(--f-display);font-weight:400;font-size:20px}}
.side-cta p{{font-size:14.5px;opacity:.85}}
.disc{{font-size:13.5px;color:var(--muted);border-top:1px solid var(--line);padding-top:14px;margin-top:28px}}
.g-list{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;list-style:none;padding:0;margin:0}}
@media (max-width:820px){{.g-list{{grid-template-columns:1fr}}}}
.g-list a{{display:grid;gap:8px;height:100%;padding:18px;border:1px solid var(--line);border-radius:10px;background:var(--surface);text-decoration:none}}
.g-list a:hover{{border-color:var(--rebar)}}
.g-list b{{font-family:var(--f-display);font-weight:400;font-size:20px;line-height:1.3}}
.g-list span{{color:var(--muted);font-size:15px}}
</style>
{ld}
</head>
<body>
<div lang="he" dir="rtl">
'''
def cards(exclude=None):
    return "".join(f'<li><a href="/madrich/{g["slug"]}/"><b>{esc(g["title"])}</b><span>{esc(g["short"])}</span></a></li>' for g in GUIDES if g is not exclude)
def tail(): return f'''
<section>
  <div class="wrap">
    <div class="sec-head"><h2>שיקום מבנים לפי עיר</h2></div>
    <ul class="cities">{"".join(f'<li><a href="/shikum-mivnim/{c["slug"]}/">שיקום מבנים ב{esc(c["name"])}</a></li>' for c in CITIES)}</ul>
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
def guide(g):
    url=f"{DOMAIN}/madrich/{g['slug']}/"
    faq=g["faq"]
    ld=[{"@context":"https://schema.org","@type":"Article","headline":g["title"],"description":g["desc"],"image":f"{DOMAIN}/img/{g['img'][0]}",
         "datePublished":"2026-10-18","dateModified":"2026-10-18","inLanguage":"he","mainEntityOfPage":url,
         "author":{"@type":"Organization","name":"משקם הבית","url":DOMAIN+"/"},"publisher":{"@type":"Organization","name":"משקם הבית","logo":{"@type":"ImageObject","url":DOMAIN+"/apple-touch-icon.png"}}},
        {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
          {"@type":"ListItem","position":1,"name":"דף הבית","item":DOMAIN+"/"},
          {"@type":"ListItem","position":2,"name":"מדריכים","item":DOMAIN+"/madrich/"},
          {"@type":"ListItem","position":3,"name":g["title"],"item":url}]}]
    ldh="".join('<script type="application/ld+json">'+json.dumps(x,ensure_ascii=False)+'</script>' for x in ld)
    toc="".join(f'<li><a href="#s{i}">{esc(h)}</a></li>' for i,(h,_) in enumerate(g["body"],1))
    parts=[]
    for i,(h,b) in enumerate(g["body"],1):
        parts.append(f'<h2 id="s{i}">{esc(h)}</h2>\n{b}')
        if i==2:
            parts.append(f'<aside class="g-cta"><b>רוצים שנסתכל על הבניין שלכם?</b><p>שלחו לנו תמונה של הליקוי או של המכתב מהעירייה, ונחזור אליכם תוך שעה עם הערכה ראשונית בחינם.</p><div>{WA}</div></aside>')
    faqh="".join(f"<details{' open' if i==0 else ''}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for i,(q,a) in enumerate(faq))
    body=f'''{header}
<main>
<section class="g-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="מיקום בעמוד"><a href="/">דף הבית</a> › <a href="/madrich/">מדריכים</a> › {esc(g["title"])}</nav>
    <h1>{esc(g["title"])}</h1>
    <p class="g-meta">צוות משקם הבית · זמן קריאה: {g["minutes"]} דקות · עודכן: 18 באוקטובר 2026</p>
  </div>
</section>
<div class="wrap g-wrap">
  <article class="g-art">
    <p class="lead">{esc(g["lead"])}</p>
    <figure><img src="/img/{g["img"][0]}" width="900" height="605" alt="{esc(g["img"][1])}" fetchpriority="high"><figcaption>{esc(g["img"][1])}.</figcaption></figure>
    {"".join(parts)}
    <h2 id="faq">שאלות נפוצות</h2>
    <div class="faq">{faqh}</div>
    <p class="disc">המידע במדריך הוא מידע כללי, ואינו מחליף ייעוץ של מהנדס או של עורך דין במקרה הספציפי שלכם.</p>
  </article>
  <aside class="g-side">
    <nav class="toc" aria-label="תוכן העניינים"><b>במדריך הזה</b><ol>{toc}<li><a href="#faq">שאלות נפוצות</a></li></ol></nav>
    <div class="side-cta"><b>הערכה ובדיקה בבניין בחינם</b><p>16 שנות ניסיון בשיקום מבנים במרכז. מענה תוך שעה.</p>{WA}<a class="btn btn-light" href="tel:+972505550182">חייגו 050-555-0182</a></div>
  </aside>
</div>
<section style="padding-top:8px">
  <div class="wrap">
    <div class="sec-head"><h2>מדריכים נוספים</h2></div>
    <ul class="g-list">{cards(g)}</ul>
  </div>
</section>'''
    return HEAD.format(title=esc(g["seo"]),desc=esc(g["desc"]),url=url,img=f"{DOMAIN}/img/{g['img'][0]}",ld=ldh)+body+tail()
for g in GUIDES:
    d=f"{R}/madrich/{g['slug']}"; os.makedirs(d,exist_ok=True)
    open(f"{d}/index.html","w",encoding="utf-8").write(guide(g))
# guides index
url=f"{DOMAIN}/madrich/"
idx=HEAD.format(title="מדריכים לשיקום מבנים ולוועדי בתים | משקם הבית",desc="מדריכים מעשיים לוועדי בתים ולבעלי דירות: צו מבנה מסוכן, סדקים בקירות, שיקום לפני התחדשות עירונית ועוד.",url=url,img=f"{DOMAIN}/img/hero.jpg",ld="")+f'''{header}
<main>
<section class="g-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="מיקום בעמוד"><a href="/">דף הבית</a> › מדריכים</nav>
    <h1>מדריכים לשיקום מבנים</h1>
    <p class="g-meta">מידע מעשי לוועדי בתים ולבעלי דירות, מצוות משקם הבית.</p>
  </div>
</section>
<section>
  <div class="wrap"><ul class="g-list">{cards()}</ul></div>
</section>'''+tail()
open(f"{R}/madrich/index.html","w",encoding="utf-8").write(idx)
# sitemap
urls=[DOMAIN+"/",DOMAIN+"/madrich/"]+[f"{DOMAIN}/madrich/{g['slug']}/" for g in GUIDES]+[f"{DOMAIN}/shikum-mivnim/{c['slug']}/" for c in CITIES]+[DOMAIN+"/privacy.html",DOMAIN+"/accessibility.html"]
open(f"{R}/sitemap.xml","w",encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"  <url><loc>{u}</loc><lastmod>2026-10-18</lastmod></url>\n" for u in urls)+"</urlset>\n")
print("guides",len(GUIDES))
