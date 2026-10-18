# -*- coding: utf-8 -*-
"""Insert the Google tag right after <head> in every HTML page of the site."""
import sys,os,glob
GTAG='''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-DEE8HKJVYE"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-DEE8HKJVYE');
</script>
'''
def run(root):
    n=0
    for f in glob.glob(os.path.join(root,"**","*.html"),recursive=True):
        if "/tools/" in f: continue
        h=open(f,encoding="utf-8").read()
        if "G-DEE8HKJVYE" in h or "<head>" not in h: continue
        h=h.replace("<head>\n","<head>\n"+GTAG,1) if "<head>\n" in h else h.replace("<head>","<head>\n"+GTAG,1)
        open(f,"w",encoding="utf-8").write(h); n+=1
    print("gtag added to",n,"pages")
if __name__=="__main__": run(sys.argv[1])
