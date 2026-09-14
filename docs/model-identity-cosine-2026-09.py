#!/usr/bin/env python3
"""AMBER nine-axis completion vectors + cosine similarity — crof vs the world."""
import math, json

# Case -> (face, max_pins or 'd2')
CASES = {
 'A-791e90ac':('text',6),'A-1fd3683a':('text',2),'A-13854d9d':('text',5),
 'A-77d62143':('build',8),'A-569dbe0d':('build',10),'A-87c472cb':('build',8),
 'A-641195e2':('build',8),'A-442d4aab':('build',7),'A-61f7ad01':('build',7),
 'A-d511f9e8':('verify',12),'A-a317e74b':('verify',15),'A-be92627f':('verify',9),
 'A-cdc3d11a':('review','d2'),'A-47eea242':('review','d2'),
 'A-ea80d793':('vision','d2'),
 'A-a5608487':('ops',5),'A-984e80ee':('ops',5),'A-24bcf707':('ops',5),'A-8d4bc770':('ops',5),
 'A-6fbeb363':('ops',6),'A-8c909d0a':('ops',7),
 'A-0676097b':('req',4),'A-d9b79b46':('ui',12),
}
OPS_ALL=['A-a5608487','A-984e80ee','A-24bcf707','A-8d4bc770','A-6fbeb363','A-8c909d0a']
BUILD=['A-77d62143','A-569dbe0d','A-87c472cb','A-641195e2','A-442d4aab','A-61f7ad01']
SUBSET21=[c for c in CASES if c not in ('A-6fbeb363','A-8c909d0a')]

def d2norm(d2): return (d2+4)/9.0

def cell_completion(case, cell):
    """cell -> completion 0..1, or None if excluded (infra/not-run)."""
    face,pins = CASES[case]
    if cell is None: return None
    if isinstance(cell,str):
        s=cell.strip()
        if s in ('—','∅'): return None
        if s=='SKIP': return None
        if s=='D2BLANK': return d2norm(-2.0)   # no-delivery on d2 case
        if s=='FAIL': return 0.0
        if s=='PASS': return 1.0
    if isinstance(cell,(int,float)):
        v=float(cell)
        if pins=='d2': return d2norm(v)
        return v/pins
    raise ValueError((case,cell))

# lane -> {case: cell}
L = {}

# ---- crof W36 (d4f,d4fv,g53f,q38,q35) ----
crof_w36 = {
'A-791e90ac':[6,6,6,6,6],'A-1fd3683a':[2,2,'FAIL',2,1],'A-13854d9d':[5,5,5,5,4],
'A-77d62143':[8,8,8,8,8],'A-569dbe0d':[10,10,10,10,10],'A-87c472cb':[6,6,6,6,6],
'A-641195e2':[8,8,8,8,3],'A-442d4aab':[7,7,1,7,7],'A-61f7ad01':[5,7,7,7,7],
'A-d511f9e8':[4,4,4,4,4],'A-a317e74b':[9,7,8,15,7],'A-be92627f':[4,0,4,3,1],
'A-cdc3d11a':[-12,0,-2,-2,-3],'A-47eea242':[3,3,3,4,3],
'A-ea80d793':['D2BLANK',-3,-2,-2,-3],
'A-a5608487':['PASS','PASS','PASS','FAIL','FAIL'],'A-984e80ee':['PASS','FAIL','PASS','PASS','∅'],
'A-24bcf707':['PASS','PASS','PASS','PASS','PASS'],'A-8d4bc770':['PASS','PASS','PASS','PASS','PASS'],
'A-0676097b':[4,2,4,4,1],'A-d9b79b46':['FAIL','FAIL','PASS','FAIL','FAIL'],
}
crof_makeup = {  # W37: q38, d4f, g53f
 'qwen3.8-27b @ crof':{'A-6fbeb363':6,'A-8c909d0a':7},
 'deepseek-v4-flash-0731 @ crof':{'A-6fbeb363':6,'A-8c909d0a':7},
 'glm-5.3-flash @ crof':{'A-6fbeb363':6,'A-8c909d0a':6},
}
for i,name in enumerate(['deepseek-v4-flash-0731 @ crof','deepseek-v4-flash-vision-exp @ crof','glm-5.3-flash @ crof','qwen3.8-27b @ crof','qwen3.5-9b @ crof']):
    L[name] = {c:v[i] for c,v in crof_w36.items()}
for name,extra in crof_makeup.items(): L[name].update(extra)

# ---- ollama W36 (d4f, g53f) + W37 makeup ----
oll_w36 = {
'A-791e90ac':[6,6],'A-1fd3683a':[2,2],'A-13854d9d':[5,5],
'A-77d62143':[8,8],'A-569dbe0d':[10,10],'A-87c472cb':[6,6],
'A-641195e2':[8,8],'A-442d4aab':[7,7],'A-61f7ad01':[7,7],
'A-d511f9e8':[4,4],'A-a317e74b':[14,14],'A-be92627f':[7,4],
'A-cdc3d11a':[-2,0],'A-47eea242':[2,4],'A-ea80d793':[-2,3.0],
'A-a5608487':[4,'PASS'],'A-984e80ee':['PASS','PASS'],'A-24bcf707':['PASS','PASS'],
'A-8d4bc770':['PASS','PASS'],'A-0676097b':[4,4],
'A-d9b79b46':['FAIL',11],  # g53f re-judged 11/12 (fail)
}
for i,name in enumerate(['deepseek-v4-flash:0731 @ ollama','glm-5.3-flash @ ollama (17/23 run)']):
    L[name]={c:v[i] for c,v in oll_w36.items()}
    L[name].update({'A-6fbeb363':6,'A-8c909d0a':7})

# ---- ollama W37 addendum 09-11 (g53f rerun, d41f) ----
oll_add = {
'A-0676097b':['PASS','PASS'],'A-13854d9d':[5,5],'A-1fd3683a':[2,2],'A-24bcf707':['PASS','PASS'],
'A-442d4aab':[7,7],'A-47eea242':[4,4],'A-569dbe0d':[10,10],'A-61f7ad01':[7,7],
'A-641195e2':[8,8],'A-6fbeb363':['PASS','PASS'],'A-77d62143':[8,8],'A-791e90ac':[6,6],
'A-87c472cb':[6,6],'A-8c909d0a':['PASS','PASS'],'A-8d4bc770':['PASS','PASS'],'A-984e80ee':['PASS','PASS'],
'A-a317e74b':[0,7],'A-a5608487':['PASS','PASS'],'A-be92627f':[4,4],'A-cdc3d11a':[-2,0],
'A-d511f9e8':[4,4],'A-d9b79b46':['FAIL','PASS'],'A-ea80d793':[2.0,-2],
}
for i,name in enumerate(['glm-5.3-flash @ ollama (09-11 rerun)','deepseek-v4.1-flash @ ollama']):
    L[name]={c:v[i] for c,v in oll_add.items()}

# ---- gpt W36 astra 5 bands (low,medium,high,xhigh,max) ----
astra = {
'A-791e90ac':[6,6,6,6,6],'A-1fd3683a':[2,2,2,'FAIL','FAIL'],'A-13854d9d':[0,0,5,0,0],
'A-77d62143':[8,8,8,8,8],'A-569dbe0d':[10,10,10,10,10],'A-87c472cb':[6,6,6,6,6],
'A-641195e2':[8,8,8,8,8],'A-442d4aab':[7,7,7,7,7],'A-61f7ad01':[7,7,7,7,7],
'A-d511f9e8':[4,4,4,4,4],'A-a317e74b':[14,14,14,14,14],'A-be92627f':[4,4,5,4,4],
'A-cdc3d11a':[-2,-12,-1,-2,-2],'A-47eea242':[4,4,4,-2,-2],
'A-ea80d793':[0.0,3.0,2.0,-2,-2],   # high: median of clean-wire reruns (2.0/-2/3.0)
'A-a5608487':[4,'PASS','PASS','PASS','PASS'],'A-984e80ee':['PASS']*5,
'A-24bcf707':['FAIL']*5,'A-8d4bc770':['PASS']*5,'A-0676097b':[4,4,4,4,4],
'A-d9b79b46':['PASS','PASS','PASS','FAIL','FAIL'],
}
for i,name in enumerate(['astra-900k low','astra-900k medium','astra-900k high','astra-900k xhigh','astra-900k max']):
    L[name]={c:v[i] for c,v in astra.items()}
# astra board entry = W36 high + bare-base makeup on 2 ops cases
L['gpt-6-astra (board: -900k W36high + bare makeup)']=dict(L['astra-900k high'])
L['gpt-6-astra (board: -900k W36high + bare makeup)'].update({'A-6fbeb363':6,'A-8c909d0a':7})

# ---- gpt W37 (luna m,h,xh ; sol m,h) ----
gptw37 = {
'A-0676097b':[4,4,4,4,4],'A-13854d9d':[5,5,5,5,5],'A-1fd3683a':[2,2,2,2,2],
'A-24bcf707':['PASS','PASS','PASS','FAIL','FAIL'],'A-442d4aab':[7,7,7,7,7],
'A-47eea242':[-1,-2,-2,-1,-2],'A-569dbe0d':[10,10,10,10,10],'A-61f7ad01':[7,7,7,7,7],
'A-641195e2':[8,8,8,8,8],'A-6fbeb363':['PASS']*5,'A-77d62143':[8,8,8,8,8],
'A-791e90ac':[6,6,6,6,6],'A-87c472cb':[6,6,6,6,6],'A-8c909d0a':['PASS']*5,
'A-8d4bc770':['PASS']*5,'A-984e80ee':['PASS']*5,
'A-a317e74b':[14,12,7,7,'∅'],'A-a5608487':['PASS']*5,
'A-be92627f':[4,2,3,4,4],'A-cdc3d11a':[-1,-2,-2,-3,-2],
'A-d511f9e8':[3,4,4,3,'∅'],'A-d9b79b46':['FAIL']*5,'A-ea80d793':[-3,-2,-3,-3,-3],
}
for i,name in enumerate(['luna-900k medium','luna-900k high','luna-900k xhigh','sol-900k medium','sol-900k high']):
    L[name]={c:v[i] for c,v in gptw37.items()}

# ---- devin W37 (swe-1-7-medium, glm-5-2, swe-2-high, swe-2-medium, swe-2-max, swe-2-low) ----
devin = {
'A-0676097b':[3,0,4,4,4,4],'A-13854d9d':[5]*6,'A-1fd3683a':[2]*6,
'A-24bcf707':['FAIL','FAIL','PASS','PASS','PASS','FAIL'],
'A-442d4aab':[7,1,7,1,7,7],'A-47eea242':[1,3,3,4,3,4],
'A-569dbe0d':[10,3,10,10,10,10],'A-61f7ad01':[7]*6,'A-641195e2':[8,1,8,8,8,8],
'A-6fbeb363':['PASS',0,'PASS','PASS','PASS','PASS'],   # glm ∅ = delivery-contract fail -> 0
'A-77d62143':[8,3,8,8,8,8],'A-791e90ac':[6]*6,'A-87c472cb':[6,2,6,6,6,6],
'A-8c909d0a':['PASS',0,'PASS','PASS','PASS','PASS'],
'A-8d4bc770':['FAIL','FAIL','FAIL','FAIL','PASS','FAIL'],
'A-984e80ee':['PASS','FAIL','PASS','PASS','PASS','PASS'],
'A-a317e74b':[13,7,7,0,'∅',7],
'A-a5608487':['PASS','FAIL','FAIL','FAIL','PASS','FAIL'],
'A-be92627f':[3,6,4,4,4,4],'A-cdc3d11a':[1.0,-4,-3.0,-2,-1.0,1.0],
'A-d511f9e8':[4]*6,'A-d9b79b46':['FAIL','PASS',12,12,12,12],
'A-ea80d793':[3.0,-2,3.0,4.0,3.0,3.0],
}
for i,name in enumerate(['swe-1-7-medium @ devin','glm-5-2 @ devin','swe-2-high @ devin','swe-2-medium @ devin','swe-2-max @ devin','swe-2-low @ devin']):
    L[name]={c:v[i] for c,v in devin.items()}

# ---- commandcode W37 (cc, ocgo-ref, preview-ref) — use cc col only (ocgo/preview have own lanes) ----
cc = {
'A-0676097b':4,'A-13854d9d':5,'A-1fd3683a':2,'A-24bcf707':5,'A-442d4aab':7,'A-47eea242':4,
'A-569dbe0d':10,'A-61f7ad01':7,'A-641195e2':8,'A-6fbeb363':6,'A-77d62143':8,'A-791e90ac':6,
'A-87c472cb':6,'A-8c909d0a':7,'A-8d4bc770':5,'A-984e80ee':5,'A-a317e74b':13,'A-a5608487':5,
'A-be92627f':8,'A-cdc3d11a':-2,'A-d511f9e8':4,'A-d9b79b46':12,'A-ea80d793':-1.0,
}
L['deepseek-v4.1-flash @ commandcode']=cc

# ---- opencode W37 col1 (ocgo) ----
ocgo = {
'A-0676097b':4,'A-13854d9d':5,'A-1fd3683a':2,'A-24bcf707':5,'A-442d4aab':7,'A-47eea242':3,
'A-569dbe0d':10,'A-61f7ad01':7,'A-641195e2':8,'A-6fbeb363':6,'A-77d62143':8,'A-791e90ac':6,
'A-87c472cb':6,'A-8c909d0a':7,'A-8d4bc770':5,'A-984e80ee':5,'A-a317e74b':7,'A-a5608487':5,
'A-be92627f':7,'A-cdc3d11a':-2,'A-d511f9e8':4,'A-d9b79b46':0,'A-ea80d793':-2,
}
L['deepseek-flash @ opencode-go']=ocgo

# ---- deepseek W37 (GA official, preview official) ----
L['deepseek-flash @ official GA']={
'A-0676097b':4,'A-13854d9d':5,'A-1fd3683a':2,'A-24bcf707':5,'A-442d4aab':7,'A-47eea242':3,
'A-569dbe0d':10,'A-61f7ad01':7,'A-641195e2':8,'A-6fbeb363':6,'A-77d62143':8,'A-791e90ac':6,
'A-87c472cb':6,'A-8c909d0a':7,'A-8d4bc770':5,'A-984e80ee':5,'A-a317e74b':7,'A-a5608487':5,
'A-be92627f':4,'A-cdc3d11a':-4,'A-d511f9e8':4,'A-d9b79b46':0,'A-ea80d793':-2}
L['deepseek-v4.1-flash-exp preview @ official']={
'A-0676097b':4,'A-13854d9d':5,'A-1fd3683a':2,'A-24bcf707':5,'A-442d4aab':7,'A-47eea242':1,
'A-569dbe0d':10,'A-61f7ad01':7,'A-641195e2':8,'A-6fbeb363':6,'A-77d62143':8,'A-791e90ac':'FAIL',
'A-87c472cb':6,'A-8c909d0a':7,'A-8d4bc770':5,'A-984e80ee':5,'A-a317e74b':7,'A-a5608487':5,
'A-be92627f':4,'A-cdc3d11a':-2,'A-d511f9e8':4,'A-d9b79b46':0,'A-ea80d793':-1.0}

# ---- workbuddy W37 (d41f wb, hy4 wb) ----
L['deepseek-v4.1-flash @ workbuddy']={
'A-0676097b':4,'A-13854d9d':5,'A-1fd3683a':2,'A-24bcf707':5,'A-442d4aab':7,'A-47eea242':4,
'A-569dbe0d':8,'A-61f7ad01':5,'A-641195e2':8,'A-6fbeb363':6,'A-77d62143':8,'A-791e90ac':6,
'A-87c472cb':6,'A-8c909d0a':7,'A-8d4bc770':5,'A-984e80ee':5,'A-a317e74b':9,'A-a5608487':5,
'A-be92627f':9,'A-cdc3d11a':-2.0,'A-d511f9e8':4,'A-d9b79b46':0,'A-ea80d793':-2}
L['hy4-preview-f @ workbuddy']={
'A-0676097b':4,'A-13854d9d':5,'A-1fd3683a':2,'A-24bcf707':5,'A-442d4aab':7,'A-47eea242':3,
'A-569dbe0d':10,'A-61f7ad01':7,'A-641195e2':8,'A-6fbeb363':6,'A-77d62143':8,'A-791e90ac':6,
'A-87c472cb':6,'A-8c909d0a':7,'A-8d4bc770':5,'A-984e80ee':5,'A-a317e74b':14,'A-a5608487':5,
'A-be92627f':3,'A-cdc3d11a':-1.0,'A-d511f9e8':4,'A-d9b79b46':12,'A-ea80d793':-1.0}

# ---------- compute ----------
def casevec(lane, cases):
    d={}
    for c in cases:
        v = cell_completion(c, lane.get(c))
        if v is not None: d[c]=v
    return d

def facetvec(lane):
    cv = casevec(lane, list(CASES))
    def m(cases):
        vals=[cv[c] for c in cases if c in cv]
        return sum(vals)/len(vals) if vals else None
    rev=[cv.get('A-cdc3d11a'),cv.get('A-47eea242')]
    return {
     'coding':m(BUILD),'delivery':cv.get('A-791e90ac'),
     'defense':m(['A-d511f9e8','A-be92627f']),'attribution':cv.get('A-a317e74b'),
     'review':(sum(rev)/2 if all(x is not None for x in rev) else None),
     'ops':m(OPS_ALL),'req-drift':cv.get('A-0676097b'),'ui':cv.get('A-d9b79b46'),
     'vision':cv.get('A-ea80d793')}

AXES=['coding','delivery','defense','attribution','review','ops','req-drift','ui','vision']
FV={name:facetvec(d) for name,d in L.items()}
CV21={name:casevec(d,SUBSET21) for name,d in L.items()}

# verify against published values
pub={'deepseek-v4.1-flash @ commandcode':{'coding':.958,'delivery':1,'defense':.611,'attribution':.867,'review':.556,'ops':1,'req-drift':1,'ui':1,'vision':.333},
     'glm-5.3-flash @ ollama (17/23 run)':{'coding':.958,'delivery':1,'defense':.389,'attribution':.933,'review':.667,'ops':1,'req-drift':1,'ui':.917,'vision':.778},
     'deepseek-v4.1-flash @ ollama':{'coding':.958,'delivery':1,'defense':.389,'attribution':.467,'review':.667,'ops':1,'req-drift':1,'ui':1,'vision':.222},
     'hy4-preview-f @ workbuddy':{'coding':.958,'delivery':1,'defense':.333,'attribution':.933,'review':.556,'ops':1,'req-drift':1,'ui':1,'vision':.333}}
print('=== normalization check vs published ===')
for lane,exp in pub.items():
    got=FV[lane]
    bad=[a for a in AXES if got[a] is None or abs(got[a]-exp[a])>0.005]
    print(f'{lane}: {"OK" if not bad else "MISMATCH "+str({a:(got[a],exp[a]) for a in bad})}')

def cosine(v1,v2,keys):
    pairs=[(v1[k],v2[k]) for k in keys if v1.get(k) is not None and v2.get(k) is not None]
    if not pairs: return None
    dot=sum(a*b for a,b in pairs); n1=math.sqrt(sum(a*a for a,b in pairs)); n2=math.sqrt(sum(b*b for a,b in pairs))
    return dot/(n1*n2) if n1 and n2 else None

crof=[n for n in L if '@ crof' in n]
refs=[n for n in L if '@ crof' not in n]
print('\n=== 9-axis cosine: crof lanes vs all published lanes ===')
for c in crof:
    scored=sorted([(cosine(FV[c],FV[r],AXES),r) for r in refs],key=lambda x:-(x[0] or -1))
    print(f'\n{c}')
    for s,r in scored[:6]: print(f'   {s:.3f}  {r}')
print('\n=== 21-case completion-vector cosine ===')
for c in crof:
    scored=sorted([(cosine(CV21[c],CV21[r],SUBSET21),r) for r in refs],key=lambda x:-(x[0] or -1))
    print(f'\n{c}')
    for s,r in scored[:6]: print(f'   {s:.3f}  {r}')

print('\n=== crof lane 9-axis vectors ===')
for c in crof:
    print(c, {a:(round(FV[c][a],3) if FV[c][a] is not None else None) for a in AXES})

# ---------- extended metrics (z-scored cosine + identity checks) ----------
def euclid(v1,v2,keys):
    p=[(v1[k],v2[k]) for k in keys if v1.get(k) is not None and v2.get(k) is not None]
    if not p: return None
    return math.sqrt(sum((a-b)**2 for a,b in p))

allnames=list(L)
axmean={a: sum(FV[n][a] for n in allnames if FV[n][a] is not None)/sum(1 for n in allnames if FV[n][a] is not None) for a in AXES}
axstd={a: (sum((FV[n][a]-axmean[a])**2 for n in allnames if FV[n][a] is not None)/max(1,sum(1 for n in allnames if FV[n][a] is not None)-1))**.5 for a in AXES}
def zvec(name):
    return {a:((FV[name][a]-axmean[a])/axstd[a] if axstd[a]>0 else 0) for a in AXES if FV[name][a] is not None}
ZV={n:zvec(n) for n in allnames}

print('\n=== axis stats across lanes (mean, std) ===')
print({a:(round(axmean[a],3),round(axstd[a],3)) for a in AXES})

print('\n=== z-scored 9-axis cosine (shape of strengths) ===')
for c in crof:
    s=sorted([(cosine(ZV[c],ZV[r],AXES),euclid(FV[c],FV[r],AXES),r) for r in refs],key=lambda x:-(x[0] or -9))
    print(f'\n{c}')
    for z,e,r in s[:6]: print(f'   z-cos {z:+.3f}  L2 {e:.3f}  {r}')

print('\n=== same-name identity checks (raw cos / z-cos / 21-case cos) ===')
pairs=[('deepseek-v4-flash-0731 @ crof','deepseek-v4-flash:0731 @ ollama'),
       ('deepseek-v4-flash-0731 @ crof','deepseek-flash @ official GA'),
       ('glm-5.3-flash @ crof','glm-5.3-flash @ ollama (17/23 run)'),
       ('glm-5.3-flash @ crof','glm-5.3-flash @ ollama (09-11 rerun)'),
       ('glm-5.3-flash @ crof','deepseek-v4.1-flash @ ollama'),
       ('qwen3.8-27b @ crof','deepseek-v4-flash:0731 @ ollama'),
       ('qwen3.5-9b @ crof','deepseek-v4-flash:0731 @ ollama'),
       ('deepseek-v4-flash-vision-exp @ crof','deepseek-v4-flash:0731 @ ollama')]
for a,b in pairs:
    r=cosine(FV[a],FV[b],AXES); z=cosine(ZV[a],ZV[b],AXES); c21=cosine(CV21[a],CV21[b],SUBSET21)
    print(f'{a}  vs  {b}:  cos {r:.3f} | z-cos {z:+.3f} | 21c {c21:.3f}')

print('\n=== per-case gaps |delta|>0.15 for the interesting pairs ===')
def difftab(a,b):
    ks=[k for k in SUBSET21 if k in CV21[a] and k in CV21[b]]
    d=sorted(ks,key=lambda k:-abs(CV21[a][k]-CV21[b][k]))
    return [(k,round(CV21[a][k],3),round(CV21[b][k],3)) for k in d if abs(CV21[a][k]-CV21[b][k])>0.15]
for a,b in [('glm-5.3-flash @ crof','glm-5.3-flash @ ollama (17/23 run)'),
            ('glm-5.3-flash @ crof','deepseek-v4.1-flash @ ollama'),
            ('deepseek-v4-flash-0731 @ crof','deepseek-v4-flash:0731 @ ollama'),
            ('deepseek-v4-flash-0731 @ crof','deepseek-flash @ official GA'),
            ('qwen3.8-27b @ crof','deepseek-v4-flash:0731 @ ollama')]:
    print(f'\n{a}\n  vs {b}\n  gaps>0.15: {difftab(a,b)}')
