"""Synthetic training database. Python standard library only. Seed 20251014.
Run: python generate.py. Overwrites generated raw/ and reference/ files.
"""
import csv, random, json, copy
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter

R = random.Random(20251014)
ROOT = Path(__file__).resolve().parent
START = datetime(2025,1,1)
END = datetime(2025,12,31,23,59,59)
def stamp(d): return d.strftime('%Y-%m-%d %H:%M:%S') if d else ''
def dt(s): return datetime.fromisoformat(s)
def pick(xs, ws=None): return R.choices(xs, weights=ws, k=1)[0]
def write(path, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

customers=[]
first='Camille Léa Emma Louise Alice Chloé Inès Sarah Julie Manon Clara Anna Hugo Louis Gabriel Lucas'.split()
last='Martin Bernard Dubois Thomas Robert Richard Petit Durand Leroy Moreau Simon Laurent Lefebvre Michel Garcia'.split()
places=[('France','Paris'),('France','Lyon'),('France','Bordeaux'),('France','Lille'),('France','Nantes'),('Belgium','Brussels'),('Switzerland','Geneva'),('Luxembourg','Luxembourg')]
for i in range(5000):
    country,city=pick(places,[40,18,9,7,7,9,7,3]); source=pick(['Website Registration','Guest Checkout','Boutique'],[45,35,20])
    customers.append(dict(customer_id=f'C{i+1:05}',first_name=pick(first),last_name=pick(last),email=f'customer{i+1:05}@example.com' if R.random()>(.25 if source=='Boutique' else .01) else '',phone=f'TEST-PHONE-{i+1:05}' if R.random()<.65 else '',customer_created_at=stamp(START-timedelta(days=R.randint(1,600),hours=R.randint(0,23))),customer_creation_source=source,country=country,city=city,acquisition_channel=pick(['Organic Search','Paid Social','Referral','Email','Direct'],[30,25,15,10,20]),email_marketing_consent='Unknown'))
    customers[-1]['email_marketing_consent']=pick(['Yes','No','Unknown'],[55,40,5]) if customers[-1]['email'] else 'Unknown'
products=[]
cats=['Bras','Briefs','Bodysuits','Nightwear','Loungewear']
for i in range(200):
    cat=cats[i//40]; price=R.randrange(*[(65,151),(25,76),(90,191),(95,251),(85,221)][i//40],5)
    products.append(dict(product_id=f'P{i+1:04}',product_name=f'{pick(["Épure","Velours","Aurore","Soie","Lumière"])} {cat} {i+1:03}',category=cat,collection=pick(['Essentials','Printemps','Éclat','Nuit']),list_price=price))
problem={'P0003','P0012','P0084','P0091','P0130'}
orders=[]; items=[]; ordermeta={}; itemmap={}
# 4,200 buyers (800 non-buyers); repeat purchases weighted by customer affinity.
buyer_ids=list(range(4200))+R.choices(range(4200),weights=[1+(i%17==0)*5 for i in range(4200)],k=5800)
R.shuffle(buyer_ids)
dates=sorted(START+timedelta(days=pick(list(range(365)),[1.8 if (START+timedelta(days=d)).month in [11,12] else 1 for d in range(365)]),seconds=R.randint(0,86399)) for _ in range(10000))
extra=set(R.sample(range(10000),5000))
for i,(ci,date) in enumerate(zip(buyer_ids,dates)):
    oid=f'O{i+1:05}'; c=customers[ci]; channel='Boutique' if c['customer_creation_source']=='Boutique' else 'Website'
    cancelled=R.random()<.035
    promised=date+timedelta(days=R.randint(2,5)) if channel=='Website' and not cancelled else None
    late=channel=='Website' and R.random()<(.36 if date.month in [11,12] else .10)
    actual=promised+timedelta(days=R.randint(2,9) if late else -R.randint(0,1)) if promised else None
    status='Cancelled' if cancelled else ('Delivered' if channel=='Boutique' or actual<=END else ('Processing' if (END-date).total_seconds()<86400 else 'Shipped'))
    actual=actual if status=='Delivered' else None
    orders.append(dict(order_id=oid,customer_id=c['customer_id'],order_date=stamp(date),order_status=status,sales_channel=channel,promised_delivery_date=stamp(promised),actual_delivery_date=stamp(actual)))
    if c['customer_creation_source'] in ['Guest Checkout','Boutique']:
        if ci not in ordermeta: c['customer_created_at']=stamp(date); ordermeta[ci]=True
    elif ci not in ordermeta and dt(c['customer_created_at'])<START and R.random()<.08:
        c['customer_created_at']=stamp(min(date,START+timedelta(days=R.randint(0,20))))
    ordermeta[ci]=True
    rows=[]
    for j in range(2 if i in extra else 1):
        p=pick(products); q=pick([1,2,3],[92,7,1]); unit=p['list_price']; discount=round(q*unit*pick([0,.1,.2],[72,20,8]),2)
        eligible=status=='Delivered' and (END-(actual or date)).days>=10
        ret=q if eligible and R.random()<(.30 if p['product_id'] in problem else .055) else 0
        row=dict(order_item_id=f'I{len(items)+1:05}',order_id=oid,product_id=p['product_id'],size=pick(['85B','90B','90C','95C','95D']) if p['category']=='Bras' else pick(['XS','S','M','L','XL'],[8,25,34,25,8]),quantity=q,unit_price=unit,discount_amount=discount,returned_quantity=ret,refund_amount=round((q*unit-discount)*ret/q,2))
        items.append(row); rows.append(row)
    itemmap[oid]=rows
# Non-buyers are registered prospects; guest checkout/boutique sources imply purchase.
for c in customers[4200:]:
    c['customer_creation_source']='Website Registration'; c['customer_created_at']=stamp(START+timedelta(days=R.randint(0,364),hours=R.randint(0,23)))

tickets=[]
weights=[]
for o in orders:
    delayed=o['actual_delivery_date'] and o['promised_delivery_date'] and o['actual_delivery_date']>o['promised_delivery_date']
    weights.append(1+5*bool(delayed)+4*any(x['returned_quantity'] for x in itemmap[o['order_id']])+3*any(x['product_id'] in problem for x in itemmap[o['order_id']]))
for i in range(2000):
    o=pick(orders,weights); rows=itemmap[o['order_id']]; row=pick(rows)
    delay=o['actual_delivery_date'] and o['promised_delivery_date'] and o['actual_delivery_date']>o['promised_delivery_date']
    reason=pick(['Delivery','Size & Fit','Return & Refund','Product Quality','Other'],[8 if delay else 2,7 if row['product_id'] in problem else 2,9 if row['returned_quantity'] else 1,1,2])
    if o['order_status']!='Delivered' and reason in ['Size & Fit','Return & Refund','Product Quality']: reason='Other'
    if o['sales_channel']=='Boutique' and reason=='Delivery': reason='Other'
    base=dt(o['order_date'])
    if reason in ['Size & Fit','Return & Refund','Product Quality']: base=dt(o['actual_delivery_date']) if o['actual_delivery_date'] else base
    if reason=='Delivery' and o['promised_delivery_date']: base=min(dt(o['promised_delivery_date']),END)
    created=min(base+timedelta(hours=R.randint(1,120)),END-timedelta(seconds=R.randint(0,60)))
    load=created.month in [11,12]
    response=created+timedelta(hours=round(R.lognormvariate(1.4 if not load else 2.5,.75),2))
    resolved=response+timedelta(hours=round(R.lognormvariate(3.5 if reason=='Return & Refund' else 2.4,.7),2))
    # Some genuinely unresolved historical cases as well as year-end censoring.
    unresolved=R.random()<.025
    first_at=response if response<=END else None
    solved=resolved if resolved<=END and not unresolved else None
    tickets.append(dict(ticket_id=f'T{i+1:05}',customer_id=o['customer_id'],order_id=o['order_id'],product_id=row['product_id'] if reason in ['Size & Fit','Product Quality','Return & Refund'] else '',created_at=stamp(created),first_response_at=stamp(first_at),resolved_at=stamp(solved),ticket_status='Resolved' if solved else ('In Progress' if first_at else 'Open'),contact_channel=pick(['Email','Chat','Phone'],[60,30,10]),contact_reason=reason))
surveys=[]
eligible=[t for t in tickets if t['resolved_at'] and dt(t['resolved_at'])<END-timedelta(days=3)]
for i,t in enumerate(R.sample(eligible,800)):
    hours=(dt(t['resolved_at'])-dt(t['created_at'])).total_seconds()/3600
    score=pick([1,2,3,4,5],[12,16,25,28,19] if hours>48 else [2,3,10,35,50])
    surveys.append(dict(survey_id=f'S{i+1:04}',ticket_id=t['ticket_id'],submitted_at=stamp(dt(t['resolved_at'])+timedelta(hours=R.randint(1,72))),csat_score=score))
tables=dict(customers=customers,products=products,orders=orders,order_items=items,support_tickets=tickets,satisfaction_surveys=surveys)

# Canonical data validation before deliberate corruption.
assert [len(v) for v in tables.values()]==[5000,200,10000,15000,2000,800]
keys={name:set(r[next(iter(r))] for r in rows) for name,rows in tables.items()}
assert all(len(keys[n])==len(rows) for n,rows in tables.items())
cmap={c['customer_id']:c for c in customers}; omap={o['order_id']:o for o in orders}; tmap={t['ticket_id']:t for t in tickets}
for o in orders:
    assert o['customer_id'] in keys['customers']
    assert dt(cmap[o['customer_id']]['customer_created_at'])<=dt(o['order_date'])<=END
for x in items:
    assert x['order_id'] in keys['orders'] and x['product_id'] in keys['products']
    assert 0<=x['returned_quantity']<=x['quantity'] and 0<=x['refund_amount']<=x['quantity']*x['unit_price']-x['discount_amount']
    assert not x['returned_quantity'] or omap[x['order_id']]['order_status']=='Delivered'
for t in tickets:
    o=omap[t['order_id']]; assert t['customer_id']==o['customer_id']
    assert dt(t['created_at'])>=dt(o['order_date'])
    assert not t['product_id'] or t['product_id'] in [x['product_id'] for x in itemmap[t['order_id']]]
    assert not t['first_response_at'] or dt(t['created_at'])<=dt(t['first_response_at'])<=END
    assert not t['resolved_at'] or dt(t['first_response_at'])<=dt(t['resolved_at'])<=END
for s in surveys:
    assert dt(tmap[s['ticket_id']]['resolved_at'])<=dt(s['submitted_at'])<=END
assert len(set(s['ticket_id'] for s in surveys))==800

raw=copy.deepcopy(tables); audit=[]
def change(table,idx,col,value,kind):
    row=raw[table][idx]; audit.append(dict(table=table,record_id=row[next(iter(row))],column=col,original_value=row[col],raw_value=value,issue=kind)); row[col]=value
for idx in R.sample(range(5000),30): change('customers',idx,'country',' france ' if customers[idx]['country']=='France' else customers[idx]['country'].lower(),'category_format')
for idx in R.sample(range(5000),15): change('customers',idx,'customer_created_at','','missing_required')
for idx in R.sample(range(10000),35): change('orders',idx,'sales_channel',orders[idx]['sales_channel'].lower()+' ','category_format')
for idx in R.sample(range(2000),15): change('support_tickets',idx,'contact_reason',' '+tickets[idx]['contact_reason'].lower(),'category_format')
for idx in R.sample([i for i,t in enumerate(tickets) if t['first_response_at']],10): change('support_tickets',idx,'first_response_at',stamp(dt(tickets[idx]['created_at'])-timedelta(hours=2)),'invalid_date_order')
for idx in R.sample(range(800),5): change('satisfaction_surveys',idx,'csat_score',6,'out_of_range')
for name,n in [('customers',20),('products',2),('orders',30),('order_items',45),('support_tickets',10),('satisfaction_surveys',4)]:
    for idx in R.sample(range(len(raw[name])),n):
        raw[name].append(copy.deepcopy(raw[name][idx])); audit.append(dict(table=name,record_id=raw[name][idx][next(iter(raw[name][idx]))],column='ALL',original_value='',raw_value='',issue='exact_duplicate'))
for name,rows in raw.items(): write(ROOT/'raw'/f'{name}.csv',rows)
for name,rows in tables.items(): write(ROOT/'reference'/f'{name}.csv',rows)
write(ROOT/'reference'/'injected_issues.csv',audit)
summary={'synthetic':True,'seed':20251014,'period':'2025-01-01/2025-12-31','as_of':stamp(END),'timezone':'Europe/Paris local naive; SLA uses elapsed wall-clock hours; DST not modeled','clean_counts':{n:len(r) for n,r in tables.items()},'raw_counts':{n:len(r) for n,r in raw.items()},'injected_issue_events':len(audit),'validation':'PASS: primary keys, foreign keys, customer/order/product ownership, chronological order, refunds, survey uniqueness, cutoff','currency':'EUR','prices':'Tax-inclusive retail prices; no VAT accounting; shipping excluded','known_limitation':'No refund timestamps: revenue assigned to original order date. Not a cash-flow or accounting ledger.'}
(ROOT/'reference'/'validation.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
