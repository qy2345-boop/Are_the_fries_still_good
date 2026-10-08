import json,re,math,collections,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
x=json.loads((root/'data/osm-source.json').read_text()); els=x['elements']
def coords(g): return [[p['lon'],p['lat']] for p in g]
def rings(e):
 if e['type']=='way': return [coords(e['geometry'])]
 parts=[coords(m['geometry']) for m in e['members'] if m.get('role')=='outer' and 'geometry' in m]; out=[]
 while parts:
  r=parts.pop(0)
  while r[-1]!=r[0]:
   for i,p in enumerate(parts):
    if p[0]==r[-1]: r+=p[1:];parts.pop(i);break
    if p[-1]==r[-1]: r+=p[-2::-1];parts.pop(i);break
   else: raise ValueError('Incomplete campus ring')
  out.append(r)
 return out
camp=[e for e in els if e['id'] in [1330709889,7469216]]
cr=[r for e in camp for r in rings(e)]
def inside(p,r):
 a=False; j=len(r)-1
 for i in range(len(r)):
  xi,yi=r[i];xj,yj=r[j]
  if (yi>p[1])!=(yj>p[1]) and p[0]<(xj-xi)*(p[1]-yi)/(yj-yi)+xi: a=not a
  j=i
 return a
features=[]
def add(e,layer,g,extra={}):
 features.append({'type':'Feature','properties':{'osm':str(e['type'])+'/'+str(e['id']),'layer':layer,**extra},'geometry':g})
for e in camp:
 add(e,'campus',{'type':'MultiPolygon','coordinates':[[r] for r in rings(e)]},{'name':e['tags']['name:en'].upper()})
for e in els:
 if e['type']!='way' or not e.get('geometry'): continue
 t=e.get('tags',{}); c=coords(e['geometry']); h=t.get('highway','')
 if h and h not in ['construction','proposed','platform','corridor','elevator','steps','ladder','raceway','services']:
  k='arterial' if h.split('_')[0] in ['motorway','trunk'] else 'major' if h.startswith('primary') else 'secondary' if h.split('_')[0] in ['secondary','tertiary'] else 'local'
  if k=='local' and any(inside(c[len(c)//2],r) for r in cr): k='campus-road'
  if h in ['footway','path','cycleway','track','pedestrian'] and k!='campus-road': continue
  add(e,'road',{'type':'LineString','coordinates':c},{'class':k,'highway':h})
 elif c[0]==c[-1] and len(c)>=4:
  l='green' if t.get('landuse') in ['grass','forest','recreation_ground'] or t.get('leisure') in ['park','garden','recreation_ground'] or t.get('natural') in ['wood','grassland'] else 'water' if t.get('natural')=='water' else 'building' if t.get('building') else 'urban' if t.get('landuse') in ['residential','commercial'] else None
  if l: add(e,l,{'type':'Polygon','coordinates':[c]})
geo={'type':'FeatureCollection','features':features}
(root/'data/basemap.geojson').write_text(json.dumps(geo,separators=(',',':')))
counts=collections.Counter(f['properties']['layer'] for f in features); print(counts)
# GCJ-02 to WGS84 inversion for the independently sourced Amap reference.
def delta(lat,lon):
 a=6378245.; ee=.00669342162296594323; q=math.pi; X=lon-105; Y=lat-35
 dy=-100+2*X+3*Y+.2*Y*Y+.1*X*Y+.2*math.sqrt(abs(X))
 dy+=(20*math.sin(6*X*q)+20*math.sin(2*X*q))*2/3
 dy+=(20*math.sin(Y*q)+40*math.sin(Y/3*q))*2/3
 dy+=(160*math.sin(Y/12*q)+320*math.sin(Y*q/30))*2/3
 dx=300+X+2*Y+.1*X*X+.1*X*Y+.1*math.sqrt(abs(X))
 dx+=(20*math.sin(6*X*q)+20*math.sin(2*X*q))*2/3
 dx+=(20*math.sin(X*q)+40*math.sin(X/3*q))*2/3
 dx+=(150*math.sin(X/12*q)+300*math.sin(X/30*q))*2/3
 rad=lat/180*q; magic=1-ee*math.sin(rad)**2
 return dy*180/((a*(1-ee))/(magic*math.sqrt(magic))*q),dx*180/(a/math.sqrt(magic)*math.cos(rad)*q)
lat,lon=39.992347,116.333755
for _ in range(8):
 dy,dx=delta(lat,lon);lat-=lat+dy-39.992347;lon-=lon+dx-116.333755
point=[lat,lon]
(root/'data/delivery-point.json').write_text(json.dumps({'label':'Huaqing Jiayuan community reference','source':'https://www.amap.com/place/B000A835NS','sourceCoordinateSystem':'GCJ-02','sourceCoordinates':[39.992347,116.333755],'mapCoordinateSystem':'WGS84','mapCoordinates':point,'osmCommunity':'https://www.openstreetmap.org/way/473654608','limitation':'Community reference retained from V15; exact dataset collection doorstep is not documented.'},indent=2))
s=(root/'the_real_arrival_v15.html').read_text()
s=s.replace('<link rel="preconnect" href="https://unpkg.com">','').replace('<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />','<style>'+ (root/'vendor/leaflet.css').read_text()+'</style>')
s=s.replace('<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>','<script>'+ (root/'vendor/leaflet.js').read_text()+'</script>')
a=s.index('const validPoints ='); b=s.index('const deliveryIcon =',a)
basemap='''const validPoints = DATA.filter(d => Number.isFinite(d.lat) && Number.isFinite(d.lng));
const studyBounds = L.latLngBounds([39.91771926,116.26543731],[40.06870374,116.43684169]);
const deliveryPoint = POINT;
const map = L.map("map",{zoomControl:false,attributionControl:false,preferCanvas:true,minZoom:12.25,maxZoom:15.75,zoomSnap:.25,maxBounds:studyBounds,maxBoundsViscosity:1});
L.control.zoom({position:"bottomright"}).addTo(map);
const BASEMAP = GEO;
for(const [name,z] of [["urban",210],["campus",220],["green",230],["building",240],["road",250],["outline",260],["delivery",650]]){map.createPane(name);map.getPane(name).style.zIndex=z;if(name!=="delivery")map.getPane(name).style.pointerEvents="none";}
const palette={urban:{fillColor:"#e9e9e3",fillOpacity:.55,stroke:false},campus:{fillColor:"#e4ece0",fillOpacity:.4,stroke:false},green:{fillColor:"#cfe0c6",fillOpacity:.78,stroke:false},water:{fillColor:"#dce5e2",fillOpacity:.85,stroke:false},building:{fillColor:"#d9dcd6",fillOpacity:.45,stroke:false}};
const roadStyles={arterial:{color:"#b9beb7",weight:2.3,opacity:.8},major:{color:"#c5c9c1",weight:1.6,opacity:.85},secondary:{color:"#d0d3ca",weight:1.1,opacity:.85},local:{color:"#d9dcd4",weight:.65,opacity:.8},"campus-road":{color:"#bfcdb9",weight:.6,opacity:.8}};
for(const layer of ["urban","campus","green","water","building","road"]){L.geoJSON(BASEMAP,{filter:f=>f.properties.layer===layer,pane:layer==='water'?'green':layer,interactive:false,style:f=>layer==='road'?roadStyles[f.properties.class]:palette[layer]}).addTo(map);}
const campusLayer=L.geoJSON(BASEMAP,{filter:f=>f.properties.layer==='campus',pane:'outline',interactive:false,style:{color:'#60805e',weight:1.4,opacity:.9,fill:false}}).addTo(map);
for(const l of campusLayer.getLayers())l.bindTooltip(l.feature.properties.name,{permanent:true,direction:'center',className:'campus-label',opacity:.95});
function fitCore(){map.fitBounds([[39.979,116.290],[40.015,116.349]],{padding:[24,24]});}
function updateMinZoom(){map.setMinZoom(Math.max(12.25,map.getBoundsZoom(studyBounds,true)));}
updateMinZoom();fitCore();map.on('resize',updateMinZoom);
const frameControl=L.control({position:'topright'});frameControl.onAdd=()=>{const d=L.DomUtil.create('div','frame-controls');d.innerHTML='<button aria-label="Fit Wudaokou core" id="coreFrame">CORE</button><button aria-label="Fit full study extent" id="fullFrame">STUDY</button>';L.DomEvent.disableClickPropagation(d);d.querySelector('#coreFrame').onclick=fitCore;d.querySelector('#fullFrame').onclick=()=>map.fitBounds(studyBounds);return d;};frameControl.addTo(map);
'''.replace('POINT',json.dumps(point)).replace('GEO',json.dumps(geo,separators=(',',':')))
s=s[:a]+basemap+s[b:]
s=s.replace('icon:deliveryIcon,zIndexOffset:1200','icon:deliveryIcon,pane:"delivery",zIndexOffset:1200').replace('DELIVERY POINT · HUAQING JIAYUAN','WUDAOKOU DELIVERY POINT')
s=re.sub(r'\s*<div class="legend">.*?</div>\s*</div>\s*\n\s*</div>\s*\n\s*<div class="results">','\n</div>\n<div class="results">',s, count=1,flags=re.S)
s=s.replace('Restaurants within current quality threshold','Restaurants in selected stages')
s=s.replace('The slider selects a maximum delivery-time window. Its first stop is the first category breakpoint, not 0 minutes; the filled track shows the accepted interval from 0 to that threshold.','The two clips select a continuous range of quality stages. ETA fixes each restaurant’s glyph; changing the brush only filters visibility.')
s=s.replace('Unmodeled layers have restaurant/location data but no quality–time model in V1. Restaurants at 60+ minutes are shown as X when the slider reaches the final stop.','Single-stage Sushi / Fresh has no modeled transition. Other stages are illustrative quality proxies, including the final X state. They do not establish food safety. OSM provides factual roads, campus boundaries and mapped vegetation; coverage is incomplete. Restaurant source coordinates are retained; their CRS is undocumented. The delivery point is a verified Huaqing Jiayuan community reference, not a confirmed collection doorstep.')
s=s.replace('arr.slice(0,80).map','arr.map')
s=s.replace('}).join("");\n  strip.querySelectorAll','}).join("") || `<div class="empty-results">No restaurants in the selected stages. Enable a layer or widen its range.</div>`;\n  strip.querySelectorAll')
s=s.replace('<button class="toggle ${active.has(cid)?"on":""}" aria-label=', '<button class="toggle ${active.has(cid)?"on":""}" aria-pressed="${active.has(cid)}" aria-label=')
s=s.replace('<button class="cat-expand">','<button class="cat-expand" aria-label="Expand ${cfg.label}" aria-expanded="${openCategory.has(cid)}">')
s=s.replace('class="result" data-id','class="result" role="button" tabindex="0" data-id')
s=s.replace('function renderAll(){','document.getElementById("resultStrip").addEventListener("keydown",e=>{if((e.key==="Enter"||e.key===" ")&&e.target.classList.contains("result")){e.preventDefault();e.target.click();}});\nfunction renderAll(){')
# Keep recognizable Latin brand labels; recover incomplete historical names with conservative transliteration.
latin=json.loads((root/'data/latin-names.json').read_text())
old=json.loads(re.search(r'const ENGLISH_NAME_MAP = (.*?);\n',s).group(1))
brands=['Luckin','Burger King','McDonald','KFC','Starbucks','ChaPanda','Yuanji','Manner','Peet','CoCo','Costa','Subway','HEYTEA','Nayuki','Mixue','Pizza Hut','Domino','Tim Hortons']
for name,value in old.items():
 if not any(value.startswith(b) for b in brands):
  base=re.split(r'[（(]',name)[0]
  full=latin.get(name,name)
  value=re.split(r'[（(]',full)[0].strip()
  value=re.sub(r'\s+',' ',value).title()
 old[name]=value
s=re.sub(r'const ENGLISH_NAME_MAP = .*?;\n',lambda m: 'const ENGLISH_NAME_MAP = '+json.dumps(old,ensure_ascii=True)+';\n',s,count=1)
(root/'data/display-names.json').write_text(json.dumps(old,ensure_ascii=False,indent=2))
# Use complete quality ranges on first open, so the study distribution is visible.
s=s.replace('else selectedRange[k] = {start:0, end:1}; // default: first stage only','else selectedRange[k] = {start:0, end:cfg.states.length}; // default: complete observed stage range')
# Normalize historical appended styles into the document head.
styles=re.findall(r'<style>(.*?)</style>',s,re.S); s=re.sub(r'<style>.*?</style>','',s,flags=re.S)
extra='''
.frame-controls{display:flex;gap:1px;background:#d3d7ce;border:1px solid #d3d7ce}.frame-controls button{border:0;background:#f2f1eb;color:#4e594a;padding:8px 10px;font:9px monospace;letter-spacing:.1em;cursor:pointer}.frame-controls button:hover{background:#e0e6d9}
button:focus-visible,input:focus-visible,.result:focus-visible{outline:2px solid #8bb6e8;outline-offset:3px}
.empty-results{padding:24px;color:#b1b1a7;font:11px monospace}.map-credit{position:absolute;z-index:700;bottom:8px;left:10px;font:8px/1.5 monospace;color:#626b5d;background:rgba(242,241,235,.88);padding:4px 6px}.map-credit a{color:inherit}.delivery-label{font-size:9px!important}
'''
s=s.replace('</head>','<style>'+ '\n'.join(styles)+extra+'</style></head>')
s=s.replace('<div id="map"></div>','<div id="map" aria-label="Wudaokou restaurant map"></div><div class="map-credit">REAL GEOMETRY · GRAPHIC RENDERING<br>© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap contributors</a> · ODbL<br>Restaurant CRS unverified · destination: community reference</div>')
(root/'the_real_arrival_final.html').write_text(s)
(root/'data/basemap-audit.json').write_text(json.dumps({'downloadedAt':x.get('osm3s',{}),'layers':dict(counts),'roadClasses':dict(collections.Counter(f['properties'].get('class') for f in features if f['properties']['layer']=='road')),'csvSha256':hashlib.sha256((root/'data/wudaokou_time_residual_analysis.csv').read_bytes()).hexdigest()},indent=2))
print('Delivery WGS84',point,'final bytes',len(s))
