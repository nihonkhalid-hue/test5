import sys;sys.path.insert(0,'.')
from netlib import fetch,BASE
import os,re,json
def payload(fp):
    b=open(fp,encoding='utf-8',errors='ignore').read()
    chunks=re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)',b,re.S)
    out=[]
    for c in chunks:
        try: out.append(json.loads('"'+c+'"'))
        except Exception: pass
    return ''.join(out)
for i,u in enumerate(sys.argv[1:]):
    fp=os.path.join(BASE,'pages',f'prof_probe_{i}.html')
    st,_=fetch('profitable.app',u,fp,7,10)
    s=payload(fp)
    m=re.search(r'"activeCategory":(\{[^}]*\}|"\$undefined"|null)',s); n=re.search(r'"activeInsightId":("[^"]*")',s)
    t=re.search(r'"total":(\d+)',s)
    print(u,st,os.path.getsize(fp),'cat=',m.group(1)[:120] if m else None,'ins=',n.group(1) if n else None,'total=',t.group(1) if t else None, 'asins',s.count('"asin"'),flush=True)
