const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33" × 7.5"
pres.title  = "MongoDB for Relational Developers";

const BG="001E2B",GREEN="00ED64",WHITE="FFFFFF",GRAY="B8C4C2",
      CARD="023430",CODE_BG="011520",BLUE="4A9EFF",ORANGE="F97316",
      PURPLE="A855F7",RED="FF6B6B";
const F="Lexend Deca", FC="Source Code Pro";
const W=13.33, H=7.5, M=0.62, BAR_Y=7.28, BAR_H=0.22;
const mkS=()=>({type:"outer",blur:10,offset:3,color:"000000",opacity:0.28,angle:135});

// ── helpers ───────────────────────────────────────────────────────────────────
function sl(bg=BG){
  const s=pres.addSlide(); s.background={color:bg};
  s.addShape(pres.shapes.RECTANGLE,{x:0,y:BAR_Y,w:W,h:BAR_H,fill:{color:GREEN},line:{color:GREEN,width:0}});
  return s;
}
function hd(s,t,y=0.22){
  s.addText(t,{x:M,y,w:W-M*2,h:0.65,fontSize:30,bold:true,color:WHITE,fontFace:F,margin:0});
  s.addShape(pres.shapes.RECTANGLE,{x:M,y:y+0.68,w:1.4,h:0.06,fill:{color:GREEN},line:{color:GREEN,width:0}});
}
function cb(s,code,x,y,w,h){
  s.addShape(pres.shapes.RECTANGLE,{x,y,w,h,fill:{color:CODE_BG},line:{color:GREEN,width:1.2},shadow:mkS()});
  s.addText(code,{x:x+0.15,y:y+0.13,w:w-0.3,h:h-0.26,fontSize:11,fontFace:FC,color:GREEN,valign:"top",margin:0});
}
function card(s,x,y,w,h,bc=GREEN){
  s.addShape(pres.shapes.RECTANGLE,{x,y,w,h,fill:{color:CARD},line:{color:bc,width:1.5},shadow:mkS()});
}
function ab(s,x,y,h,c=GREEN){
  s.addShape(pres.shapes.RECTANGLE,{x,y,w:0.12,h,fill:{color:c},line:{color:c,width:0}});
}
function secDiv(s,n,label,sub=""){
  s.addShape(pres.shapes.RECTANGLE,{x:0,y:0,w:0.55,h:H,fill:{color:GREEN},line:{color:GREEN,width:0}});
  s.addShape(pres.shapes.OVAL,{x:9.5,y:-1,w:6,h:6,fill:{color:CARD,transparency:40},line:{color:CARD,width:0}});
  s.addText(n,{x:0.9,y:1.8,w:2.5,h:2.2,fontSize:120,bold:true,color:GREEN,fontFace:F,margin:0,transparency:20});
  s.addText(label,{x:0.9,y:4.1,w:10,h:1.2,fontSize:48,bold:true,color:WHITE,fontFace:F,margin:0});
  if(sub) s.addText(sub,{x:0.9,y:5.4,w:9,h:0.7,fontSize:18,color:GRAY,fontFace:F,italic:true,margin:0});
}

// ══════════════════════════════════════════════════════
// S1 — TITLE
// ══════════════════════════════════════════════════════
{const s=pres.addSlide(); s.background={color:BG};
s.addShape(pres.shapes.RECTANGLE,{x:0,y:0,w:0.5,h:H,fill:{color:GREEN},line:{color:GREEN,width:0}});
s.addShape(pres.shapes.OVAL,{x:9.2,y:-1.2,w:6.5,h:6.5,fill:{color:CARD,transparency:35},line:{color:CARD,width:0}});
s.addShape(pres.shapes.OVAL,{x:11.2,y:3.8,w:3.5,h:3.5,fill:{color:GREEN,transparency:82},line:{color:GREEN,width:0}});
s.addText("MongoDB for\nRelational Developers",{x:0.85,y:1.1,w:10,h:3.0,fontSize:58,bold:true,color:WHITE,fontFace:F,valign:"middle",margin:0});
s.addText("Think Documents, Not Rows",{x:0.85,y:4.25,w:9,h:0.85,fontSize:26,color:GREEN,fontFace:F,italic:true,margin:0});
s.addText("A 2-Hour Hands-On Session  ·  Developer Track",{x:0.85,y:5.2,w:8,h:0.55,fontSize:16,color:GRAY,fontFace:F,margin:0});
s.addShape(pres.shapes.RECTANGLE,{x:0,y:BAR_Y,w:W,h:BAR_H,fill:{color:GREEN},line:{color:GREEN,width:0}});
s.addNotes(`Welcome — session for developers coming from SQL Server, PostgreSQL, MySQL.\nMapping what you know to MongoDB concepts. 2 hours, demos throughout.`);}

// S2 — AGENDA
{const s=sl(); hd(s,"Agenda");
const blocks=[{n:"01",label:"Data Modeling",sub:"Documents, Embedding\nvs Referencing"},{n:"02",label:"Querying",sub:"CRUD, Filters,\nAggregation Pipeline"},{n:"03",label:"Indexes &\nPerformance",sub:"Types, Compound,\nExplain Plan"},{n:"04",label:"Transactions\n& ACID",sub:"Multi-document,\nWhen to use"},{n:"05",label:"Developer\nExperience",sub:"Compass, Atlas,\nChange Streams"}];
blocks.forEach((b,i)=>{const x=M+i*2.42; card(s,x,1.05,2.28,5.8);
  s.addText(b.n,{x,y:1.15,w:2.28,h:0.95,fontSize:48,bold:true,color:GREEN,fontFace:F,align:"center",margin:0});
  s.addShape(pres.shapes.RECTANGLE,{x:x+0.2,y:2.15,w:1.88,h:0.06,fill:{color:GREEN},line:{color:GREEN,width:0}});
  s.addText(b.label,{x:x+0.1,y:2.28,w:2.1,h:1.0,fontSize:16,bold:true,color:WHITE,fontFace:F,align:"center",margin:0,wrap:true});
  s.addText(b.sub,{x:x+0.1,y:3.42,w:2.1,h:2.5,fontSize:13,color:GRAY,fontFace:F,align:"center",margin:0,wrap:true});});
s.addNotes(`Five blocks over 2 hours. Demos woven throughout — not saved for the end.`);}

// S3 — DATABASE HISTORY (NEW)
{const s=sl(); hd(s,"Why the World Is Moving Back to Denormalization");
s.addText("A 50-year arc — and why the constraints that made normalization brilliant no longer apply",
  {x:M,y:0.98,w:W-M*2,h:0.36,fontSize:14,color:GRAY,fontFace:F,italic:true,margin:0});

const CW=3.9, CX=[0.62,4.69,8.76], CY=1.42, CH=5.3;
const eras=[
  { accent:GREEN,  icon:"🗂", era:"Era 1", years:"1970s – 2000s",
    title:"Normalization Wins",
    bullets:[
      "Disk was expensive — storing 'New York' in 10,000 rows cost real money",
      "Codd's Normal Forms: one source of truth, no update anomalies",
      "JOINs were cheap — all data lived on a single server in RAM",
      "Apps were internal, low-traffic — schemas were fixed for decades",
      "3NF became the industry standard: mathematical, provable, correct",
    ]},
  { accent:BLUE,   icon:"⚡", era:"Era 2", years:"2000s — Web Scale Arrives",
    title:"Denormalization Tried & Dropped",
    bullets:[
      "High-traffic web (Amazon, Yahoo) exposed JOIN bottlenecks under concurrency",
      "Data warehouses pre-joined tables (star schema) for analytics speed",
      "In OLTP: no tooling — hand-rolling denormalized writes was error-prone",
      "Update anomalies returned — customer name duplicated across 50 K rows",
      "3NF became cultural: DBAs called denormalization a 'bad practice'",
    ]},
  { accent:ORANGE, icon:"🌍", era:"Era 3", years:"2010s → Today",
    title:"The World Moves Back",
    bullets:[
      "Distributed systems broke JOINs — you can't JOIN across shards",
      "Reads vastly outnumber writes — optimize for the common path",
      "JSON is the API contract — why shred a nested object into 3 tables?",
      "Network latency replaced disk cost as the real constraint",
      "MongoDB / DynamoDB / Cassandra make denormalization safe and tooled",
    ]},
];

eras.forEach((e,i)=>{
  const x=CX[i];
  s.addShape(pres.shapes.RECTANGLE,{x,y:CY,w:CW,h:CH,fill:{color:CARD},line:{color:e.accent,width:1.8},shadow:mkS()});
  s.addShape(pres.shapes.RECTANGLE,{x,y:CY,w:CW,h:0.68,fill:{color:e.accent},line:{color:e.accent,width:0}});
  s.addText(e.icon+"  "+e.era,{x:x+0.15,y:CY+0.05,w:CW-0.3,h:0.32,fontSize:14,bold:true,color:BG,fontFace:F,margin:0});
  s.addText(e.years,{x:x+0.15,y:CY+0.36,w:CW-0.3,h:0.26,fontSize:10.5,color:BG,fontFace:F,margin:0});
  s.addText(e.title,{x:x+0.15,y:CY+0.78,w:CW-0.3,h:0.52,fontSize:15,bold:true,color:e.accent,fontFace:F,margin:0,wrap:true});
  s.addShape(pres.shapes.RECTANGLE,{x:x+0.15,y:CY+1.34,w:CW-0.3,h:0.04,fill:{color:e.accent,transparency:55},line:{color:e.accent,width:0}});
  e.bullets.forEach((b,j)=>{
    s.addText([{text:b,options:{bullet:true}}],
      {x:x+0.15,y:CY+1.46+j*0.72,w:CW-0.3,h:0.68,fontSize:12,fontFace:F,color:WHITE,margin:0,wrap:true});
  });
});

// punchline
s.addShape(pres.shapes.RECTANGLE,{x:M,y:6.8,w:W-M*2,h:0.38,fill:{color:"012A3A"},line:{color:GREEN,width:1.2}});
s.addText("“Normalization solved the constraints of 1975.  Embedding solves the constraints of 2025.”",
  {x:M+0.25,y:6.8,w:W-M*2-0.5,h:0.38,fontSize:13.5,bold:true,italic:true,color:GREEN,fontFace:F,align:"center",valign:"middle",margin:0});

s.addNotes(`HISTORY FRAMING — spend 2-3 minutes here. This slide earns you credibility with relational developers.

Era 1 — WHY normalization was brilliant (not wrong, just solving a different problem):
  • Disk was genuinely expensive. IBM charged per MB. Storing the same string 10,000 times was a real cost.
  • One source of truth meant no inconsistency: change a city name in one row, not thousands.
  • Codd published 12 rules in 1970 — mathematical proofs, not opinions. Hard to argue with math.
  • Internal enterprise apps (banking, ERP, HR) had stable schemas and predictable, low concurrency.

Era 2 — WHY it was tried AND why it was dropped for OLTP:
  • Amazon (2003-2007) publicly described JOIN bottlenecks. They started denormalizing. But their engineers were brilliant and had bespoke tooling.
  • Data warehouses DID successfully denormalize (star schema, Kimball) — but that's analytics, not OLTP.
  • Without tooling: if you embed a customer's name in every order row and they change their name, you write 50,000 rows. That's an update anomaly — exactly what normalization was designed to prevent.
  • So the industry concluded: "denormalization for OLTP = bad idea." That conclusion was RIGHT for that era.

Era 3 — WHY the constraint changed and why NOW is different:
  • You cannot JOIN across shards. If customer 123's data is on shard A and order data is on shard B, there is no JOIN. Period. Embedding is not optional — it's forced.
  • Read/write asymmetry flipped: modern web apps do 100:1 reads to writes. Design for the 99 reads, not the 1 write.
  • JSON IS your API. Your Node/Python app receives a nested object. Storing it shredded into 3 tables and reassembling it on every request is wasted work.
  • MongoDB provides the tooling: atomic updates to nested arrays (no update anomalies), document validation (schema enforcement), transactions for when you genuinely need them.

Punchline — say it out loud:
  "Normalization solved the constraints of 1975. Embedding solves the constraints of 2025."
  The constraints changed. The answer changed. That's not fashion — that's engineering.`);}

// S4 — SECTION 01 DIVIDER
{const s=sl(); secDiv(s,"01","Data Modeling","Documents · Embedding · Referencing · Schema Flexibility");
s.addNotes(`Section 1: Data Modeling — the biggest mental shift. Design for ACCESS PATTERNS, not normalization.`);}

// S4 — MENTAL MODEL
{const s=sl(); hd(s,"Mental Model Shift");
card(s,M,1.05,5.8,5.8,"456789");
s.addShape(pres.shapes.RECTANGLE,{x:M,y:1.05,w:5.8,h:0.62,fill:{color:"012A3A"},line:{color:"456789",width:0}});
s.addText("SQL World",{x:M,y:1.05,w:5.8,h:0.62,fontSize:18,bold:true,color:GRAY,fontFace:F,align:"center",margin:0});
["Schema","Table","Row","Column","Foreign Key / JOIN"].forEach((r,i)=>{
  s.addText(r,{x:M+0.3,y:1.82+i*0.72,w:5.2,h:0.65,fontSize:18,color:WHITE,fontFace:F,margin:0});
  s.addText("→",{x:M+5.1,y:1.87+i*0.72,w:0.7,h:0.55,fontSize:22,color:GREEN,align:"center",margin:0});});
card(s,M+6.5,1.05,6.2,5.8,GREEN);
s.addShape(pres.shapes.RECTANGLE,{x:M+6.5,y:1.05,w:6.2,h:0.62,fill:{color:"012A3A"},line:{color:GREEN,width:0}});
s.addText("MongoDB World",{x:M+6.5,y:1.05,w:6.2,h:0.62,fontSize:18,bold:true,color:GREEN,fontFace:F,align:"center",margin:0});
["Database","Collection","Document  (BSON)","Field","Embedded doc  /  $lookup"].forEach((r,i)=>{
  s.addText(r,{x:M+6.8,y:1.82+i*0.72,w:5.8,h:0.65,fontSize:18,color:WHITE,fontFace:F,margin:0});});
s.addText("BSON Types: ObjectId  ·  Date  ·  Array  ·  Nested Object  ·  Decimal128",{x:M,y:7.0,w:W-M*2,h:0.35,fontSize:13,color:GREEN,fontFace:F,align:"center",margin:0});
s.addNotes(`Each SQL concept maps directly. Documents hold arrays + nested objects natively — no junction tables.\nObjectId = auto-generated primary key (_id field).`);}

// S5 — WHEN TO CHOOSE
{const s=sl(); hd(s,"When to Choose MongoDB");
card(s,M,1.05,6.0,5.8,GREEN);
s.addText("✔  USE MongoDB when…",{x:M+0.2,y:1.12,w:5.6,h:0.6,fontSize:17,bold:true,color:GREEN,fontFace:F,margin:0});
["Flexible / evolving schema — no ALTER TABLE","Hierarchical or nested data (orders + line items)","Horizontal scale-out — sharding built-in","High write throughput & real-time workloads","Varied document shapes per record"].forEach((t,i)=>{
  s.addText([{text:t,options:{bullet:true}}],{x:M+0.25,y:1.85+i*0.78,w:5.5,h:0.7,fontSize:15,color:WHITE,fontFace:F,margin:0});});
card(s,M+6.5,1.05,6.2,5.8,"CC4444");
s.addText("✖  RECONSIDER when…",{x:M+6.7,y:1.12,w:5.8,h:0.6,fontSize:17,bold:true,color:RED,fontFace:F,margin:0});
["Complex multi-entity JOINs are a hard requirement","Heavy flat reporting / pure OLAP analytics","Enforced foreign key constraints are non-negotiable"].forEach((t,i)=>{
  s.addText([{text:t,options:{bullet:true}}],{x:M+6.75,y:1.85+i*1.1,w:5.8,h:0.95,fontSize:15,color:WHITE,fontFace:F,margin:0,wrap:true});});
s.addNotes(`Be honest — builds credibility. Atlas SQL interface covers analytics use cases.\nAsk: "What's your biggest pain point with your relational DB?" — answers map to MongoDB strengths.`);}

// ══════════════════════════════════════════════════════
// S6 — SCENARIO (NEW)
// ══════════════════════════════════════════════════════
{const s=sl(); hd(s,"The Scenario — E-Commerce Order Management");
s.addText("Every concept from here onward — SQL normalization, MongoDB modeling, queries, indexes, transactions — uses these three entities:",
  {x:M,y:0.98,w:W-M*2,h:0.48,fontSize:15,color:GRAY,fontFace:F,margin:0});

// ── Entity cards ──
const EW=3.55, EH=3.6;
function entityCard(s,x,title,fields,accent,icon){
  const y=1.56;
  s.addShape(pres.shapes.RECTANGLE,{x,y,w:EW,h:EH,fill:{color:CARD},line:{color:accent,width:2.0},shadow:mkS()});
  s.addShape(pres.shapes.RECTANGLE,{x,y,w:EW,h:0.65,fill:{color:accent},line:{color:accent,width:0}});
  s.addText(icon+"  "+title,{x:x+0.14,y:y+0.06,w:EW-0.28,h:0.55,fontSize:18,bold:true,color:BG,fontFace:F,margin:0});
  fields.forEach(([fname,ftype,isFK],i)=>{
    const fy=y+0.76+i*0.52;
    if(i%2===0) s.addShape(pres.shapes.RECTANGLE,{x:x+0.1,y:fy-0.04,w:EW-0.2,h:0.46,fill:{color:"012A3A"},line:{color:"012A3A",width:0}});
    s.addText(fname,{x:x+0.2,y:fy,w:2.1,h:0.42,fontSize:12,color:isFK?BLUE:WHITE,fontFace:FC,margin:0});
    s.addText(ftype,{x:x+2.35,y:fy,w:EW-2.55,h:0.42,fontSize:11,color:GRAY,fontFace:FC,align:"right",margin:0});
  });
}
entityCard(s,0.62,"Customer",
  [["id","INT  PK",false],["name","VARCHAR",false],["email","VARCHAR",false],["region","VARCHAR",false],["tier","ENUM",false]],
  GREEN,"👤");
entityCard(s,4.90,"Order",
  [["id","INT  PK",false],["customer_id","FK → Customer",true],["status","VARCHAR",false],["amount","DECIMAL",false],["created_at","TIMESTAMP",false]],
  BLUE,"📦");
entityCard(s,9.18,"Order Item",
  [["id","INT  PK",false],["order_id","FK → Order",true],["sku","VARCHAR",false],["qty","INT",false],["unit_price","DECIMAL",false]],
  ORANGE,"🛒");

// ── Arrows ──
const AY=3.32;
s.addShape(pres.shapes.RECTANGLE,{x:4.17,y:AY+0.08,w:0.73,h:0.05,fill:{color:GREEN},line:{color:GREEN,width:0}});
s.addShape(pres.shapes.RECTANGLE,{x:4.86,y:AY,w:0.06,h:0.22,fill:{color:GREEN},line:{color:GREEN,width:0}});
s.addText("places",{x:4.1,y:AY-0.42,w:0.88,h:0.32,fontSize:12,color:GREEN,italic:true,align:"center",margin:0});
s.addText("1 : N",{x:4.08,y:AY+0.3,w:0.88,h:0.3,fontSize:13,bold:true,color:GREEN,align:"center",margin:0});

s.addShape(pres.shapes.RECTANGLE,{x:8.45,y:AY+0.08,w:0.73,h:0.05,fill:{color:BLUE},line:{color:BLUE,width:0}});
s.addShape(pres.shapes.RECTANGLE,{x:9.14,y:AY,w:0.06,h:0.22,fill:{color:BLUE},line:{color:BLUE,width:0}});
s.addText("contains",{x:8.38,y:AY-0.42,w:0.9,h:0.32,fontSize:12,color:BLUE,italic:true,align:"center",margin:0});
s.addText("1 : N",{x:8.38,y:AY+0.3,w:0.9,h:0.3,fontSize:13,bold:true,color:BLUE,align:"center",margin:0});

// ── What we'll show ──
s.addText("What you will see modeled with these entities:",
  {x:M,y:5.3,w:W-M*2,h:0.42,fontSize:15,bold:true,color:WHITE,fontFace:F,margin:0});
[{n:"01",col:GREEN, t:"SQL — 3NF Normalized",       d:"3 separate tables · Foreign keys · JOIN query to read one order"},
 {n:"02",col:BLUE,  t:"MongoDB — Embedded Documents",d:"1 document · Items array embedded · Single read, zero joins"},
 {n:"03",col:ORANGE,t:"Queries · Indexes · Transactions",d:"Same entities, same data — SQL vs MongoDB side by side"}].forEach((c,i)=>{
  const cx=M+i*4.24;
  s.addShape(pres.shapes.RECTANGLE,{x:cx,y:5.78,w:4.1,h:1.28,fill:{color:CARD},line:{color:c.col,width:1.5}});
  s.addShape(pres.shapes.RECTANGLE,{x:cx,y:5.78,w:4.1,h:0.12,fill:{color:c.col},line:{color:c.col,width:0}});
  s.addText(c.n+"  "+c.t,{x:cx+0.18,y:5.88,w:3.8,h:0.5,fontSize:14,bold:true,color:WHITE,fontFace:F,margin:0});
  s.addText(c.d,{x:cx+0.18,y:6.4,w:3.8,h:0.58,fontSize:12,color:GRAY,fontFace:F,margin:0,wrap:true});});

s.addNotes(`SCENARIO SETUP — spend ~2 minutes here to anchor the audience.

Three entities from a familiar domain — e-commerce order management.

Walk through each entity:
• Customer: who buys. Region (APAC/EMEA/AMER) and tier (gold/silver/bronze).
• Order: what was purchased. Belongs to one customer (1:N). Status + total amount.
• Order Item: line items inside an order (1:N). SKU, quantity, unit price.

Point to relationship arrows:
  Customer places many Orders.
  Each Order contains many Order Items.

Preview what's coming:
  01 — SQL: 3 normalized tables, foreign keys, JOIN query just to display one order
  02 — MongoDB: collapses into ONE document — items embedded inside the order, customer referenced by ID
  03 — Every query, index, and transaction demo uses these exact entities — SQL vs MongoDB side by side

Say: "Keep these three entities in your head. By the end of this section you will have seen the same data modeled two completely different ways — and understand WHY MongoDB makes the choices it does."`);}

// ══════════════════════════════════════════════════════
// S7 — SQL NORMALIZED (NEW)
// ══════════════════════════════════════════════════════
{const s=sl(); hd(s,"SQL Normalized Schema — The Starting Point");
s.addText("A single order requires 3 tables and 2 JOINs to display completely:",
  {x:M,y:1.0,w:W-M*2,h:0.42,fontSize:15,color:GRAY,fontFace:F,margin:0});

const TW=3.7, TH=3.5, ty=1.52;
function sqlTable(s,x,title,pkCol,cols,accent){
  s.addShape(pres.shapes.RECTANGLE,{x,y:ty,w:TW,h:TH,fill:{color:CARD},line:{color:accent,width:1.5}});
  s.addShape(pres.shapes.RECTANGLE,{x,y:ty,w:TW,h:0.55,fill:{color:accent},line:{color:accent,width:0}});
  s.addText(title,{x:x+0.12,y:ty+0.05,w:TW-0.24,h:0.48,fontSize:16,bold:true,color:BG,fontFace:F,margin:0});
  const ry=ty+0.62;
  s.addShape(pres.shapes.RECTANGLE,{x:x+0.12,y:ry,w:TW-0.24,h:0.38,fill:{color:"012A3A"},line:{color:"012A3A",width:0}});
  s.addText("🔑 "+pkCol,{x:x+0.2,y:ry+0.02,w:TW-0.4,h:0.34,fontSize:12,bold:true,color:GREEN,fontFace:FC,margin:0});
  cols.forEach((col,i)=>{
    const isFK=col.startsWith("FK:");
    s.addText(isFK?"🔗 "+col.replace("FK:",""):"   "+col,
      {x:x+0.2,y:ry+0.44+i*0.42,w:TW-0.4,h:0.38,fontSize:12,color:isFK?BLUE:WHITE,fontFace:FC,margin:0});
  });
}
sqlTable(s,0.62,"customers","id  INT  PK",
  ["   name  VARCHAR","   email  VARCHAR","   region  VARCHAR","   tier  VARCHAR"],GREEN);
sqlTable(s,4.82,"orders","id  INT  PK",
  ["FK: customer_id → customers","   status  VARCHAR","   amount  DECIMAL","   created_at  TIMESTAMP"],BLUE);
sqlTable(s,9.02,"order_items","id  INT  PK",
  ["FK: order_id → orders","   sku  VARCHAR","   qty  INT","   unit_price  DECIMAL"],"F97316");

// Arrows
const AY2=3.22;
s.addShape(pres.shapes.RECTANGLE,{x:4.32,y:AY2+0.08,w:0.5,h:0.05,fill:{color:GREEN},line:{color:GREEN,width:0}});
s.addShape(pres.shapes.RECTANGLE,{x:4.78,y:AY2,w:0.06,h:0.22,fill:{color:GREEN},line:{color:GREEN,width:0}});
s.addText("1 : N",{x:4.15,y:AY2-0.36,w:0.8,h:0.3,fontSize:11,bold:true,color:GREEN,align:"center",margin:0});
s.addShape(pres.shapes.RECTANGLE,{x:8.52,y:AY2+0.08,w:0.5,h:0.05,fill:{color:BLUE},line:{color:BLUE,width:0}});
s.addShape(pres.shapes.RECTANGLE,{x:8.98,y:AY2,w:0.06,h:0.22,fill:{color:BLUE},line:{color:BLUE,width:0}});
s.addText("1 : N",{x:8.35,y:AY2-0.36,w:0.8,h:0.3,fontSize:11,bold:true,color:BLUE,align:"center",margin:0});

cb(s,`SELECT c.name, c.region, o.status, o.amount, oi.sku, oi.qty, oi.unit_price\nFROM   customers   c\nJOIN   orders      o   ON  o.customer_id = c.id\nJOIN   order_items oi  ON  oi.order_id   = o.id\nWHERE  c.id = 42;`,
  M,5.18,W-M*2,1.82);
s.addText("→  In MongoDB this is ONE document read — no JOINs, no multiple round-trips",
  {x:M,y:7.04,w:W-M*2,h:0.3,fontSize:13,color:GREEN,fontFace:F,italic:true,margin:0});

s.addNotes(`Sets up the "why embedding matters" story.

Walk through the three tables — classic 3NF normalization.
Point to the JOIN query: "To display ONE order with its items and customer, you need 3 tables, 2 JOINs."

Then say: "In MongoDB, this entire result is stored as ONE document. One read. No joins."
This leads directly into the next slide — Embedding vs Referencing.

Key insight: normalization was invented to save disk space in the 1970s.
MongoDB trades some redundancy for dramatically simpler reads — usually the right trade for modern apps.`);}

// S8 — EMBEDDING VS REFERENCING
{const s=sl(); hd(s,"Embedding vs Referencing — The #1 Design Decision");
card(s,M,1.05,5.95,5.8,GREEN);
s.addText("EMBED  (nest inside document)",{x:M+0.2,y:1.12,w:5.5,h:0.55,fontSize:16,bold:true,color:GREEN,fontFace:F,margin:0});
["Data always accessed together","One-to-few relationship","Child data rarely changes alone","Read performance is priority"].forEach((t,i)=>{
  s.addText([{text:t,options:{bullet:true}}],{x:M+0.25,y:1.78+i*0.6,w:5.45,h:0.55,fontSize:14,color:WHITE,fontFace:F,margin:0});});
cb(s,`// Order with embedded line items\n{\n  _id: ObjectId("ord001"),\n  customer: "Acme Corp",\n  status: "completed",\n  items: [\n    { sku:"A1", qty:2, price:10.00 },\n    { sku:"B3", qty:1, price:25.00 }\n  ]\n}`,M+0.15,4.3,5.6,2.35);
s.addText("vs",{x:M+5.95+0.15,y:3.6,w:0.8,h:0.6,fontSize:22,color:GRAY,align:"center",margin:0});
card(s,M+7.15,1.05,5.6,5.8,BLUE);
s.addText("REFERENCE  (store _id pointer)",{x:M+7.35,y:1.12,w:5.2,h:0.55,fontSize:16,bold:true,color:BLUE,fontFace:F,margin:0});
["Data accessed independently","One-to-many-large relationship","Many-to-many relationships","Child data updated frequently"].forEach((t,i)=>{
  s.addText([{text:t,options:{bullet:true}}],{x:M+7.4,y:1.78+i*0.6,w:5.1,h:0.55,fontSize:14,color:WHITE,fontFace:F,margin:0});});
cb(s,`// Order references customer by ID\n{\n  _id: ObjectId("ord001"),\n  customerId: ObjectId("cust42"),\n  items: [...]\n}\n\n// Customer lives in its own collection\n// — fetch independently when needed`,M+7.3,4.3,5.3,2.35);
s.addNotes(`Replaces the normalization conversation. Design for ACCESS PATTERNS, not normalization.\n\nEmbed: data accessed together, one-to-few, read performance priority.\nReference: independent access, one-to-many-large, many-to-many.\n\nFrom the scenario: items EMBED (always with order). Customer REFERENCE (queried independently).`);}

// S9 — SCHEMA FLEXIBILITY
{const s=sl(); hd(s,"Schema Flexibility — No Migrations Needed");
s.addText("Old and new document shapes coexist in the same collection:",{x:M,y:1.0,w:W-M*2,h:0.45,fontSize:16,color:GRAY,fontFace:F,margin:0});
cb(s,`// v1 document — deployed 2022\n{\n  _id: ObjectId("aaa111"),\n  name:  "Alice",\n  email: "alice@acme.com"\n}`,M,1.55,5.75,2.45);
s.addText("→",{x:M+5.75+0.35,y:2.55,w:0.8,h:0.6,fontSize:32,color:GREEN,align:"center",margin:0});
cb(s,`// v2 document — deployed 2024, same collection\n{\n  _id: ObjectId("bbb222"),\n  name:  "Bob",\n  email: "bob@acme.com",\n  phone: "+1-555-0199",\n  preferences: { theme:"dark", lang:"en" },\n  tier: "premium",\n  createdAt: ISODate("2024-03-10")\n}`,M+7.1,1.55,5.6,2.95);
const pts=["No ALTER TABLE — ship new app version instantly, new fields appear automatically","Old documents remain valid — app code handles missing fields gracefully","Optional: enforce shape with JSON Schema validation ($jsonSchema) for guardrails","Perfect for microservices, iterative product builds, and A/B rollouts"];
s.addText(pts.map((p,i)=>({text:p,options:{bullet:true,breakLine:i<pts.length-1}})),{x:M,y:4.65,w:W-M*2,h:2.2,fontSize:15,color:WHITE,fontFace:F,margin:0});
s.addNotes(`No migration scripts. No downtime windows. No ALTER TABLE locking 500M rows.\nv1 (3 fields) and v2 (7 fields) coexist in the same collection. Your new code writes new fields, old code still reads old docs.\n$jsonSchema: validationAction:"warn" during migration, then "error" once all docs updated.`);}

// S10 — SECTION 02
{const s=sl(); secDiv(s,"02","Querying","CRUD · Filter Operators · Arrays · Aggregation Pipeline");
s.addNotes(`Section 2: Every SQL clause has a MongoDB equivalent. You will be writing queries in minutes.`);}

// S11 — CRUD
{const s=sl(); hd(s,"SQL ↔ MongoDB CRUD — Side by Side");
const H2={fill:{color:"012A3A"},color:GREEN,bold:true,fontSize:14,fontFace:F,align:"center"};
const RN={color:WHITE,fontSize:12,fontFace:FC,fill:{color:CARD}};
const RA={color:WHITE,fontSize:12,fontFace:FC,fill:{color:"011F2E"}};
const rows=[
  [{text:"Operation",options:H2},{text:"SQL",options:H2},{text:"MongoDB",options:H2}],
  [{text:"Read all",options:{...RN}},{text:"SELECT * FROM users",options:{...RN}},{text:"db.users.find({})",options:{...RN,color:GREEN}}],
  [{text:"Read + filter",options:{...RA}},{text:"SELECT * FROM users WHERE age > 30",options:{...RA}},{text:"db.users.find({ age:{ $gt:30 } })",options:{...RA,color:GREEN}}],
  [{text:"Read + project",options:{...RN}},{text:"SELECT name, email FROM users WHERE active=1",options:{...RN}},{text:"db.users.find({active:1},{name:1,email:1})",options:{...RN,color:GREEN}}],
  [{text:"Insert",options:{...RA}},{text:"INSERT INTO users VALUES (...)",options:{...RA}},{text:'db.users.insertOne({ name:"Ana", age:28 })',options:{...RA,color:GREEN}}],
  [{text:"Update",options:{...RN}},{text:"UPDATE users SET name='Bob' WHERE id=1",options:{...RN}},{text:'db.users.updateOne({_id:1},{$set:{name:"Bob"}})',options:{...RN,color:GREEN}}],
  [{text:"Delete",options:{...RA}},{text:"DELETE FROM users WHERE id=1",options:{...RA}},{text:"db.users.deleteOne({ _id: ObjectId('...') })",options:{...RA,color:GREEN}}],
  [{text:"Count",options:{...RN}},{text:"SELECT COUNT(*) FROM users WHERE active=1",options:{...RN}},{text:"db.users.countDocuments({ active:1 })",options:{...RN,color:GREEN}}],
];
s.addTable(rows,{x:M,y:1.02,w:W-M*2,h:6.0,colW:[2.0,5.25,5.25],border:{pt:1,color:"012A3A"},rowH:0.67});
s.addNotes(`Reference card — keep this visible during the first Compass demo.\nALWAYS use $set in updateOne — without it you REPLACE the entire document.\nfindOneAndUpdate(): atomic find+modify, great for counters and state machines.`);}

// S12 — FILTERS
{const s=sl(); hd(s,"Filter Operators — SQL Equivalents");
const ops=[{op:"$eq",sql:"= value",ex:'{ age: { $eq: 25 } }  // same as { age: 25 }'},{op:"$gt/$lt",sql:"> and <",ex:'{ price: { $gt: 10, $lt: 100 } }'},{op:"$in",sql:"IN (...)",ex:'{ status: { $in: ["active","pending"] } }'},{op:"$ne",sql:"!= value",ex:'{ role: { $ne: "guest" } }'},{op:"$regex",sql:"LIKE '%x%'",ex:'{ email: { $regex: /gmail\\.com$/ } }'},{op:"$and",sql:"AND",ex:'{ $and: [{ age:{$gt:18} }, { active:true }] }'},{op:"$or",sql:"OR",ex:'{ $or: [{ city:"NYC" }, { city:"LA" }] }'},{op:"$exists",sql:"IS NOT NULL",ex:'{ phone: { $exists: true } }'}];
ops.forEach((o,i)=>{const col=i<4?0:1,row=i%4,x=M+col*6.35,y=1.08+row*1.52;
  s.addShape(pres.shapes.RECTANGLE,{x,y,w:6.18,h:1.42,fill:{color:CARD},line:{color:"023A50",width:1}});
  s.addText(o.op,{x:x+0.15,y:y+0.08,w:1.6,h:0.58,fontSize:20,bold:true,color:GREEN,fontFace:FC,margin:0});
  s.addText(`≈ ${o.sql}`,{x:x+1.85,y:y+0.1,w:4.2,h:0.5,fontSize:14,color:GRAY,fontFace:F,margin:0});
  s.addText(o.ex,{x:x+0.15,y:y+0.72,w:5.88,h:0.6,fontSize:11.5,color:"AADDCC",fontFace:FC,margin:0});});
s.addNotes(`Filters are JSON objects — no SQL injection, composable as variables.\n$gt+$lt combined = BETWEEN. $in array built dynamically. $exists great during schema migrations.`);}

// S13 — ARRAYS
{const s=sl(); hd(s,"Querying Arrays & Nested Fields");
cb(s,`// Sample document\n{\n  _id: 1, name: "Alice",\n  address: { city:"NYC", zip:"10001" },\n  tags: ["mongodb","backend","nodejs"],\n  orders: [\n    { item:"Book", qty:2,  price:12.99 },\n    { item:"Pen",  qty:10, price:1.49  }\n  ]\n}`,M,1.05,5.75,3.55);
const qs=[{label:"Dot notation — nested field",code:'// Find users in NYC\ndb.users.find({ "address.city": "NYC" })'},{label:"Array contains value",code:'// Has "mongodb" tag\ndb.users.find({ tags: "mongodb" })'},{label:"$elemMatch — array element conditions",code:'// Any order with qty > 5\ndb.users.find({\n  orders: { $elemMatch: { qty:{$gt:5} } }\n})'},{label:"Array size / $all",code:'// Exactly 3 tags\ndb.users.find({ tags: { $size: 3 } })\n// Has BOTH tags\ndb.users.find({ tags: { $all:["mongodb","backend"] } })'}];
qs.forEach((q,i)=>{const y=1.05+i*1.6;
  s.addText(q.label,{x:M+6.4,y,w:6.3,h:0.42,fontSize:15,bold:true,color:GREEN,fontFace:F,margin:0});
  cb(s,q.code,M+6.4,y+0.44,6.3,1.1);});
s.addNotes(`{ tags:"mongodb" } replaces a full SQL junction table JOIN — one line.\n$elemMatch: both conditions on the SAME array element.\n$slice in projection: return only first N array elements.`);}

// S14 — AGGREGATION
{const s=sl(); hd(s,"Aggregation Pipeline — Your New Best Friend");
const stages=[{stage:"$match",sql:"WHERE",color:"00A550"},{stage:"$lookup",sql:"LEFT JOIN",color:"007CC2"},{stage:"$group",sql:"GROUP BY",color:"7B2FBE"},{stage:"$project",sql:"SELECT",color:"E05C00"},{stage:"$sort",sql:"ORDER BY",color:"C41230"},{stage:"$limit",sql:"LIMIT",color:"8B6914"}];
stages.forEach((st,i)=>{const x=M+i*2.03;
  s.addShape(pres.shapes.RECTANGLE,{x,y:1.05,w:1.88,h:1.55,fill:{color:st.color},line:{color:st.color,width:0},shadow:mkS()});
  s.addText(st.stage,{x,y:1.18,w:1.88,h:0.68,fontSize:17,bold:true,color:WHITE,fontFace:FC,align:"center",margin:0});
  s.addText(`≈ ${st.sql}`,{x,y:1.88,w:1.88,h:0.48,fontSize:13,color:WHITE,fontFace:F,align:"center",margin:0});
  if(i<stages.length-1) s.addText("▶",{x:x+1.88,y:1.72,w:0.15,h:0.38,fontSize:13,color:GRAY,align:"center",margin:0});});
cb(s,`db.orders.aggregate([\n  { $match:   { status: "completed" } },\n  { $lookup:  { from:"customers", localField:"custId",\n               foreignField:"_id", as:"customer" } },\n  { $unwind:  "$customer" },\n  { $group:   { _id: "$customer.region",\n               totalRevenue: { $sum: "$amount" },\n               orderCount:  { $sum: 1 } } },\n  { $project: { region:"$_id", totalRevenue:1, orderCount:1, _id:0 } },\n  { $sort:    { totalRevenue: -1 } },\n  { $limit:   10 }\n])`,M,2.82,W-M*2,4.32);
s.addNotes(`Each stage transforms data and passes to the next — a Unix pipe for data.\nAlways put $match first. $unwind flattens $lookup array. $group uses $sum, $avg, $addToSet.\nOther: $addFields, $bucket (ranges), $facet (parallel), $out (write to collection).`);}

// S15 — AGG DEMO
{const s=sl(); hd(s,"Live Demo — Convert This SQL to Aggregation");
s.addText("SQL query we'll port together  (3-table JOIN · GROUP BY · ORDER BY):",{x:M,y:1.0,w:W-M*2,h:0.48,fontSize:16,color:GRAY,fontFace:F,margin:0});
cb(s,`-- Find top 5 regions by total revenue (completed orders only)\nSELECT\n    c.region,\n    COUNT(o.id)                    AS order_count,\n    SUM(oi.qty * oi.unit_price)    AS total_revenue\nFROM   orders       o\nJOIN   customers    c   ON  o.customer_id  = c.id\nJOIN   order_items  oi  ON  oi.order_id    = o.id\nWHERE  o.status = 'completed'\nGROUP  BY c.region\nORDER  BY total_revenue DESC\nLIMIT  5;`,M,1.58,W-M*2,3.55);
s.addText("→  Build the equivalent pipeline stage-by-stage in Compass Aggregation Builder — one stage at a time",{x:M,y:5.3,w:W-M*2,h:0.52,fontSize:16,color:GREEN,fontFace:F,italic:true,margin:0});
s.addText("Watch the live preview update after every stage you add",{x:M,y:5.88,w:W-M*2,h:0.42,fontSize:14,color:GRAY,fontFace:F,margin:0});
s.addNotes(`LIVE DEMO — centerpiece. 10-12 minutes.\nCompass Aggregation Builder: add one stage at a time. Preview updates live after each stage.\nAfter building: Export to Language → Node.js → free driver code.\nNote: this query uses the SAME entities from our scenario — customers, orders, order_items.`);}

// S16 — SECTION 03
{const s=sl(); secDiv(s,"03","Indexes & Performance","Single · Compound · Multikey · Explain Plan");
s.addNotes(`Section 3: Indexes — same concept as SQL, with extra power for arrays and TTL.`);}

// S17 — INDEXES
{const s=sl(); hd(s,"Indexes — Same Idea, More Power");
const types=[{name:"Single Field",sql:"CREATE INDEX ON users(age)",mongo:'db.users.createIndex({ age: 1 })',note:'1=ascending, -1=descending. Background by default.'},{name:"Compound",sql:"CREATE INDEX ON orders(status, createdAt)",mongo:'db.orders.createIndex({ status: 1, createdAt: -1 })',note:'Order matters — prefix rule same as SQL Server / PostgreSQL.'},{name:"Multikey (Arrays)",sql:"No direct equivalent — needs junction table",mongo:'db.posts.createIndex({ tags: 1 })',note:'Indexes every array element. { tags:"mongodb" } uses this.'},{name:"Text Index",sql:"FULLTEXT INDEX on articles(body)",mongo:'db.articles.createIndex({ title:"text", body:"text" })',note:'Query: { $text: { $search: "mongodb aggregation" } }'}];
types.forEach((t,i)=>{const y=1.05+i*1.48;
  s.addShape(pres.shapes.RECTANGLE,{x:M,y,w:W-M*2,h:1.38,fill:{color:CARD},line:{color:"023A50",width:1}});
  ab(s,M,y,1.38);
  s.addText(t.name,{x:M+0.28,y:y+0.06,w:3.2,h:0.52,fontSize:18,bold:true,color:GREEN,fontFace:F,margin:0});
  s.addText(`SQL: ${t.sql}`,{x:M+3.6,y:y+0.08,w:8.5,h:0.44,fontSize:13,color:GRAY,fontFace:F,margin:0,italic:true});
  s.addText(t.mongo,{x:M+0.28,y:y+0.64,w:7.5,h:0.48,fontSize:13,color:"AADDCC",fontFace:FC,margin:0});
  s.addText(`⚑  ${t.note}`,{x:M+7.9,y:y+0.66,w:4.5,h:0.48,fontSize:12,color:GRAY,fontFace:F,italic:true,margin:0});});
s.addNotes(`ESR Rule: Equality fields first, Sort fields second, Range fields last.\nTTL: { expireAfterSeconds:3600 } — auto-expire sessions, temp data, logs.\nSparse: only indexes docs where field exists — saves space for optional fields.`);}

// S18 — EXPLAIN
{const s=sl(); hd(s,"Explain Plan — Find Your Slow Queries");
s.addText('SQL: EXPLAIN SELECT ...      MongoDB: db.collection.explain("executionStats").find(...)',{x:M,y:1.0,w:W-M*2,h:0.52,fontSize:14,color:GRAY,fontFace:FC,margin:0});
cb(s,`db.orders\n  .explain("executionStats")\n  .find(\n    { customerId: ObjectId("abc123"), status: "completed" },\n    { amount: 1, createdAt: 1 }\n  )`,M,1.62,W-M*2,1.58);
const fields=[{f:"winningPlan.stage",m:'"COLLSCAN" = full table scan (bad)   ·   "IXSCAN" = index used (good)'},{f:"executionStats.totalDocsExamined",m:"Rows scanned — if >> nReturned, index missing or not selective"},{f:"executionStats.nReturned",m:"Documents returned — ideal: equal to totalDocsExamined"},{f:"winningPlan.inputStage.indexName",m:"Which index the planner chose — confirm it is the right one"},{f:"executionTimeMillis",m:"Total time — run BEFORE and AFTER adding index to compare"}];
fields.forEach((f,i)=>{
  s.addShape(pres.shapes.RECTANGLE,{x:M,y:3.32+i*0.72,w:W-M*2,h:0.66,fill:{color:i%2===0?CARD:"011F2E"},line:{color:"012A3A",width:1}});
  s.addText(f.f,{x:M+0.2,y:3.36+i*0.72,w:5.5,h:0.55,fontSize:13,color:GREEN,fontFace:FC,margin:0});
  s.addText(f.m,{x:M+5.9,y:3.36+i*0.72,w:6.6,h:0.55,fontSize:13,color:WHITE,fontFace:F,margin:0});});
s.addNotes(`Identical to EXPLAIN ANALYZE in PostgreSQL. COLLSCAN = alarm. IXSCAN = good.\ntotalDocsExamined >> nReturned → missing or wrong index.\nIn Compass: visual tree view, color-coded. Atlas Performance Advisor: automatic recommendations.`);}

// S19 — INDEX DEMO
{const s=sl(); hd(s,"Live Demo — Index Before & After");
card(s,M,1.05,5.9,6.0,"CC4444");
s.addText("BEFORE  Index",{x:M+0.2,y:1.12,w:5.5,h:0.62,fontSize:20,bold:true,color:RED,fontFace:F,margin:0});
cb(s,`db.orders\n  .explain("executionStats")\n  .find({ customerId: id })`,M+0.15,1.85,5.5,1.2);
s.addText([{text:'stage: ',options:{color:GRAY}},{text:'"COLLSCAN"',options:{color:RED,bold:true}},{text:"\ntotalDocsExamined: ",options:{color:GRAY}},{text:"500,000",options:{color:RED,bold:true}},{text:"\nnReturned: ",options:{color:GRAY}},{text:"12",options:{color:WHITE}},{text:"\nexecutionTime: ",options:{color:GRAY}},{text:"890 ms",options:{color:RED,bold:true}}],{x:M+0.2,y:3.18,w:5.5,h:2.4,fontSize:18,fontFace:FC,margin:0});
s.addText("→",{x:M+5.9+0.25,y:3.65,w:0.85,h:0.78,fontSize:38,color:GREEN,align:"center",margin:0});
cb(s,`db.orders.createIndex(\n  { customerId: 1 }\n)`,M+5.9+0.22,4.85,5.6,1.0);
card(s,M+7.3,1.05,5.4,6.0,GREEN);
s.addText("AFTER  Index",{x:M+7.5,y:1.12,w:5.0,h:0.62,fontSize:20,bold:true,color:GREEN,fontFace:F,margin:0});
cb(s,`db.orders\n  .explain("executionStats")\n  .find({ customerId: id })`,M+7.45,1.85,5.1,1.2);
s.addText([{text:'stage: ',options:{color:GRAY}},{text:'"IXSCAN"',options:{color:GREEN,bold:true}},{text:"\ntotalDocsExamined: ",options:{color:GRAY}},{text:"12",options:{color:GREEN,bold:true}},{text:"\nnReturned: ",options:{color:GRAY}},{text:"12",options:{color:WHITE}},{text:"\nexecutionTime: ",options:{color:GRAY}},{text:"2 ms",options:{color:GREEN,bold:true}}],{x:M+7.5,y:3.18,w:5.0,h:2.4,fontSize:18,fontFace:FC,margin:0});
s.addNotes(`LIVE DEMO. 500,000 doc orders collection. Do NOT pre-create index.\n1. Run explain → COLLSCAN, 500K examined, ~890ms\n2. createIndex({ customerId:1 })\n3. Same query → IXSCAN, 12 examined, 2ms\n"Same query. Same data. One line. 445x faster."\nAtlas Performance Advisor finds these automatically.`);}

// S20 — SECTION 04
{const s=sl(); secDiv(s,"04","Transactions & ACID","Multi-document · Cross-collection · When to use");
s.addNotes(`Section 4: Address the #1 misconception — "MongoDB doesn't have transactions." It does, since v4.0.`);}

// S21 — TRANSACTIONS
{const s=sl(); hd(s,"Transactions & ACID — Yes, MongoDB Has Them");
s.addText("Multi-document ACID transactions available since MongoDB 4.0  (2018)",{x:M,y:1.02,w:W-M*2,h:0.52,fontSize:18,color:GREEN,fontFace:F,bold:true,margin:0});
cb(s,`const session = client.startSession();\nsession.startTransaction();\ntry {\n  // 1. Deduct inventory\n  await inventory.updateOne(\n    { sku:"A1" }, { $inc:{ qty:-2 } }, { session }\n  );\n  // 2. Create order\n  await orders.insertOne(\n    { customerId, items, total }, { session }\n  );\n  // 3. Write audit log\n  await auditLog.insertOne(\n    { action:"order_placed", ts:new Date() }, { session }\n  );\n  await session.commitTransaction();\n} catch (err) {\n  await session.abortTransaction();\n} finally { session.endSession(); }`,M,1.65,7.0,5.5);
const pts=[{h:"ACID compliant",b:"Atomicity, Consistency, Isolation, Durability — same guarantees as PostgreSQL"},{h:"Use sparingly",b:"Good embedding often eliminates the need. Transactions have overhead."},{h:"Cross-collection",b:"Update orders + inventory + auditLog in one atomic operation"},{h:"Replica Set req.",b:"Need at least 1-node replica set. Atlas always has this."}];
pts.forEach((p,i)=>{const y=1.65+i*1.38;
  s.addShape(pres.shapes.RECTANGLE,{x:M+7.5,y,w:5.2,h:1.25,fill:{color:CARD},line:{color:"023A50",width:1}});
  ab(s,M+7.5,y,1.25);
  s.addText(p.h,{x:M+7.75,y:y+0.08,w:4.88,h:0.48,fontSize:16,bold:true,color:GREEN,fontFace:F,margin:0});
  s.addText(p.b,{x:M+7.75,y:y+0.58,w:4.88,h:0.58,fontSize:13,color:WHITE,fontFace:F,margin:0,wrap:true});});
s.addNotes(`"Best transaction is the one you don't need." Embedding often makes transactions unnecessary.\nWhen you DO need them: money transfers, seat booking, inventory reservation + order + audit.`);}

// S22 — SECTION 05
{const s=sl(); secDiv(s,"05","Developer Experience","Compass · Atlas · Change Streams · Node.js Driver");
s.addNotes(`Section 5: The ecosystem around MongoDB that makes daily developer life easy.`);}

// S23 — DEV EXPERIENCE
{const s=sl(); hd(s,"Developer Experience");
const tools=[{label:"Compass GUI",desc:"Visual query builder, aggregation pipeline preview, explain plan tree — your SSMS/pgAdmin equivalent"},{label:"Atlas Cloud",desc:"Managed MongoDB: 2-min setup, Performance Advisor, auto-index suggestions, free 512MB tier"},{label:"Change Streams",desc:"Real-time data change reactions — no polling, no cron. Replaces CDC pipelines for many use cases"},{label:"Node.js Driver",desc:"Official drivers for Node, Python, Java, Go, .NET. Results are plain objects — no ORM required"}];
tools.forEach((t,i)=>{const col=i%2,row=Math.floor(i/2),x=M+col*6.4,y=1.05+row*2.02;
  s.addShape(pres.shapes.RECTANGLE,{x,y,w:6.15,h:1.85,fill:{color:CARD},line:{color:GREEN,width:1.5},shadow:mkS()});
  s.addShape(pres.shapes.RECTANGLE,{x,y,w:6.15,h:0.14,fill:{color:GREEN},line:{color:GREEN,width:0}});
  s.addText(t.label,{x:x+0.2,y:y+0.22,w:5.8,h:0.58,fontSize:20,bold:true,color:WHITE,fontFace:F,margin:0});
  s.addText(t.desc,{x:x+0.2,y:y+0.85,w:5.8,h:0.88,fontSize:14,color:GRAY,fontFace:F,margin:0,wrap:true});});
cb(s,`// Node.js — async/await, results are plain JS objects\nconst users = await db.collection("users")\n  .find({ age: { $gt: 30 }, active: true })\n  .sort({ name: 1 }).limit(20)\n  .project({ name:1, email:1, _id:0 })\n  .toArray();`,M,5.12,W-M*2,1.65);
s.addNotes(`Compass: visual Aggregation Builder exports to driver code. Atlas free tier: 2 min to live cluster.\nChange Streams: db.orders.watch([{ $match:{"fullDocument.status":"shipped"} }]) — event-driven.\nTypeScript: full type inference with typed collections.`);}

// S24 — MIGRATION
{const s=sl(); hd(s,"Migration Path — Relational → MongoDB");
const steps=[{n:"1",t:"Analyze",d:"Map access patterns. What does the app actually query? Design for reads, not normalization."},{n:"2",t:"Redesign",d:"Embed vs reference per collection. Do NOT map tables 1:1. Redesign for your queries."},{n:"3",t:"Migrate",d:"ETL: SQL SELECT → insertMany. Or use Atlas Live Migration / AWS DMS."},{n:"4",t:"Dual-Write",d:"Strangler Fig: write to both DBs, shift reads to MongoDB gradually."},{n:"5",t:"Cutover",d:"Validate data parity, switch traffic, monitor, decommission SQL."}];
steps.forEach((st,i)=>{const x=M+i*2.42;
  s.addShape(pres.shapes.RECTANGLE,{x,y:1.05,w:2.28,h:0.82,fill:{color:GREEN},line:{color:GREEN,width:0}});
  s.addText(st.n,{x,y:1.05,w:0.58,h:0.82,fontSize:28,bold:true,color:BG,fontFace:F,align:"center",margin:0});
  s.addText(st.t,{x:x+0.58,y:1.05,w:1.7,h:0.82,fontSize:18,bold:true,color:BG,fontFace:F,valign:"middle",margin:0});
  s.addShape(pres.shapes.RECTANGLE,{x,y:1.89,w:2.28,h:4.6,fill:{color:CARD},line:{color:"023A50",width:1}});
  s.addText(st.d,{x:x+0.15,y:2.02,w:1.98,h:4.3,fontSize:14,color:WHITE,fontFace:F,wrap:true,valign:"top",margin:0});
  if(i<steps.length-1) s.addText("→",{x:x+2.28,y:1.22,w:0.14,h:0.48,fontSize:18,color:GREEN,align:"center",margin:0});});
s.addText("Tools: mongodump/mongorestore  ·  Atlas Live Migration  ·  AWS DMS  ·  Custom ETL (Python/Node)",{x:M,y:6.62,w:W-M*2,h:0.42,fontSize:14,color:GRAY,fontFace:F,align:"center",margin:0});
s.addNotes(`#1 mistake: mapping SQL tables 1:1 to MongoDB collections without rethinking the model.\nStrangler Fig: keep SQL alive in parallel, shift reads incrementally, decommission only after validation.`);}

// S25 — RESOURCES
{const s=pres.addSlide(); s.background={color:BG};
s.addShape(pres.shapes.RECTANGLE,{x:0,y:0,w:W,h:0.28,fill:{color:GREEN},line:{color:GREEN,width:0}});
s.addShape(pres.shapes.RECTANGLE,{x:0,y:BAR_Y,w:W,h:BAR_H,fill:{color:GREEN},line:{color:GREEN,width:0}});
s.addText("Resources & Q&A",{x:M,y:0.38,w:W-M*2,h:0.85,fontSize:36,bold:true,color:WHITE,fontFace:F,margin:0});
const res=[{label:"MongoDB University",url:"university.mongodb.com  —  Free courses, M001 (intro), M121 (aggregation)"},{label:"Official Docs",url:"docs.mongodb.com  —  Operator reference, runnable examples, tutorials"},{label:"MongoDB Compass",url:"mongodb.com/products/compass  —  Free GUI, visual aggregation builder"},{label:"Atlas Free Tier",url:"mongodb.com/atlas  —  512 MB free, sample data pre-loaded, no credit card"},{label:"Schema Design Patterns",url:"mongodb.com/developer  —  Bucket, Computed, Extended Reference patterns"},{label:"Node.js Quick Start",url:"mongodb.com/docs/drivers/node  —  5-minute guide, TypeScript support"}];
res.forEach((r,i)=>{const col=i%2,row=Math.floor(i/2),x=M+col*6.38,y=1.42+row*1.72;
  s.addShape(pres.shapes.RECTANGLE,{x,y,w:6.12,h:1.58,fill:{color:CARD},line:{color:"023A50",width:1}});
  ab(s,x,y,1.58);
  s.addText(r.label,{x:x+0.28,y:y+0.1,w:5.7,h:0.5,fontSize:16,bold:true,color:GREEN,fontFace:F,margin:0});
  s.addText(r.url,{x:x+0.28,y:y+0.65,w:5.7,h:0.82,fontSize:12,color:GRAY,fontFace:F,margin:0,wrap:true});});
s.addText("Thank you!  Start with Atlas Free Tier today — your first cluster is live in 2 minutes.",{x:M,y:6.72,w:W-M*2,h:0.45,fontSize:18,color:GREEN,bold:true,fontFace:F,align:"center",margin:0});
s.addNotes(`Learning path: Atlas free account → M001 → M121. Homework: redesign a 2-3 table SQL schema as MongoDB docs. That exercise solidifies everything.`);}

// DEMO DIVIDER
{const s=pres.addSlide(); s.background={color:"011520"};
s.addShape(pres.shapes.RECTANGLE,{x:0,y:0,w:0.7,h:H,fill:{color:GREEN},line:{color:GREEN,width:0}});
s.addShape(pres.shapes.OVAL,{x:8.5,y:-1.5,w:7.5,h:7.5,fill:{color:CARD,transparency:40},line:{color:CARD,width:0}});
s.addText("LIVE\nDEMO",{x:1.1,y:0.9,w:11,h:4.5,fontSize:100,bold:true,color:WHITE,fontFace:F,valign:"middle"});
s.addText("Hands-on queries — follow along in Compass or mongosh",{x:1.1,y:5.65,w:10,h:0.75,fontSize:22,color:GREEN,fontFace:F,italic:true});
s.addShape(pres.shapes.RECTANGLE,{x:0,y:BAR_Y,w:W,h:BAR_H,fill:{color:GREEN},line:{color:GREEN,width:0}});
s.addNotes(`Open Compass → connect to Atlas or localhost. Demos: Dataset setup · CRUD · Aggregation · Indexes · Node.js · Transactions`);}

// DEMO 1 — DATASET
{const s=sl(); hd(s,"Demo 1 — Sample Dataset Setup");
s.addText("Load the e-commerce dataset (same entities from the scenario):",{x:M,y:1.0,w:W-M*2,h:0.45,fontSize:16,color:GRAY,fontFace:F,margin:0});
cb(s,`use shop\n\ndb.customers.insertMany([\n  { _id: ObjectId("cust001"), name:"Alice Chen",  region:"APAC", tier:"gold"   },\n  { _id: ObjectId("cust002"), name:"Bob Patel",   region:"EMEA", tier:"silver" },\n  { _id: ObjectId("cust003"), name:"Carol Smith", region:"AMER", tier:"gold"   },\n  { _id: ObjectId("cust004"), name:"David Kim",   region:"APAC", tier:"bronze" },\n])\n\n// Orders with embedded line items — no order_items table needed!\ndb.orders.insertMany([\n  { _id:ObjectId("ord001"), custId:ObjectId("cust001"), status:"completed",\n    amount:340.00, createdAt:new Date("2024-01-15"),\n    items:[{ sku:"A1", qty:2, price:120 }, { sku:"B3", qty:1, price:100 }] },\n  { _id:ObjectId("ord002"), custId:ObjectId("cust002"), status:"completed",\n    amount:89.50,  createdAt:new Date("2024-02-20"),\n    items:[{ sku:"C5", qty:3, price:29.83 }] },\n  { _id:ObjectId("ord003"), custId:ObjectId("cust001"), status:"pending",\n    amount:215.00, createdAt:new Date("2024-03-01"),\n    items:[{ sku:"A1", qty:1, price:120 }, { sku:"D7", qty:1, price:95 }] },\n  { _id:ObjectId("ord004"), custId:ObjectId("cust003"), status:"completed",\n    amount:560.00, createdAt:new Date("2024-03-10"),\n    items:[{ sku:"E2", qty:4, price:140 }] },\n  { _id:ObjectId("ord005"), custId:ObjectId("cust004"), status:"completed",\n    amount:45.00,  createdAt:new Date("2024-04-05"),\n    items:[{ sku:"C5", qty:1, price:45  }] },\n])`,M,1.55,W-M*2,5.6);
s.addNotes(`Same Customer → Order → Order Item entities from the scenario slide.\nNotice: NO order_items collection. Items are EMBEDDED inside orders.\ncustomers collection + orders collection = 2 collections instead of 3 SQL tables.\nRun db.orders.findOne() to show the full document with embedded items.`);}

// DEMO 2 — CRUD
{const s=sl(); hd(s,"Demo 2 — CRUD Operations");
cb(s,`// READ: completed orders > $100 (filter + projection)\ndb.orders.find(\n  { status:"completed", amount:{ $gt:100 } },\n  { _id:0, custId:1, amount:1, status:1 }\n)\n\n// READ: orders containing item sku "A1" (dot-notation on embedded array)\ndb.orders.find({ "items.sku": "A1" })\n// SQL equiv: SELECT * FROM orders o JOIN order_items oi ON oi.order_id=o.id WHERE oi.sku='A1'\n\n// UPDATE: mark order shipped, add timestamp\ndb.orders.updateOne(\n  { _id: ObjectId("ord003") },\n  { $set: { status:"shipped", shippedAt: new Date() } }\n)\n\n// UPDATE: add tracking to a specific line item (positional $ operator)\ndb.orders.updateOne(\n  { _id:ObjectId("ord003"), "items.sku":"A1" },\n  { $set: { "items.$.tracking": "TRK-99021" } }   // $ = matched array element\n)\n\n// DELETE: remove pending orders older than 30 days\ndb.orders.deleteMany({\n  status:   "pending",\n  createdAt:{ $lt: new Date(Date.now() - 30*24*60*60*1000) }\n})`,M,1.05,W-M*2,6.1);
s.addNotes(`"items.sku":"A1" — replaces the SQL JOIN query shown in the SQL Normalized slide. One line.\n$set REQUIRED for partial update — without it you replace the entire document.\nPositional $ — updates ONLY the matched array element.`);}

// DEMO 3 — AGGREGATION
{const s=sl(); hd(s,"Demo 3 — Aggregation Pipeline (SQL → MongoDB)");
cb(s,`// SQL equivalent: SELECT c.region, COUNT(*) AS orders, SUM(o.amount) AS revenue\n// FROM orders o JOIN customers c ON o.custId=c._id WHERE o.status='completed'\n// GROUP BY c.region ORDER BY revenue DESC\n\ndb.orders.aggregate([\n  { $match:   { status: "completed" } },\n  { $lookup:  { from:"customers", localField:"custId",\n               foreignField:"_id", as:"customer" } },\n  { $unwind:  "$customer" },\n  { $group:   { _id:"$customer.region",\n               totalRevenue:{ $sum:"$amount" }, orderCount:{ $sum:1 },\n               avgOrder:{ $avg:"$amount" }, tiers:{ $addToSet:"$customer.tier" } } },\n  { $project: { _id:0, region:"$_id", totalRevenue:1, orderCount:1,\n               avgOrder:{ $round:["$avgOrder",2] }, tiers:1 } },\n  { $sort:    { totalRevenue: -1 } }\n])`,M,1.05,W-M*2,6.1);
s.addNotes(`Build in Compass Aggregation Builder one stage at a time. Show live preview after each stage.\n$addToSet: collect unique tiers per region. $round: expression operator.\nAfter: Export to Language → Node.js → free driver code.`);}

// DEMO 4 — INDEXES
{const s=sl(); hd(s,"Demo 4 — Index Creation & Explain Plan");
cb(s,`// Step 1: Check existing indexes\ndb.orders.getIndexes()  // → only _id index\n\n// Step 2: Explain BEFORE index — spot COLLSCAN\ndb.orders.explain("executionStats")\n  .find({ custId: ObjectId("cust001"), status: "completed" })\n// → stage:"COLLSCAN"  totalDocsExamined:5\n\n// Step 3: Create compound index (ESR: Equality → Sort → Range)\ndb.orders.createIndex(\n  { custId: 1, status: 1 },\n  { name: "idx_custId_status" }\n)\n\n// Step 4: Explain AFTER — confirm IXSCAN\ndb.orders.explain("executionStats")\n  .find({ custId: ObjectId("cust001"), status: "completed" })\n// → stage:"IXSCAN"  indexName:"idx_custId_status"  totalDocsExamined:1\n\n// Step 5: TTL index — auto-expire pending orders after 7 days\ndb.orders.createIndex(\n  { createdAt: 1 },\n  { expireAfterSeconds:604800,\n    partialFilterExpression:{ status:"pending" } }\n)\n\n// Step 6: Text index on customer name\ndb.customers.createIndex({ name: "text" })\ndb.customers.find({ $text: { $search: "Alice Chen" } })\n\n// Step 7: Sparse index — only where shippedAt exists\ndb.orders.createIndex({ shippedAt: 1 }, { sparse: true })`,M,1.05,W-M*2,6.1);
s.addNotes(`Step 2: COLLSCAN visible. "On 5M docs this is your 3am incident."\nStep 4: Confirm IXSCAN, totalDocsExamined=nReturned — perfect selectivity.\nStep 5: TTL only for pending — shipped/completed kept forever (partialFilterExpression).`);}

// DEMO 5 — NODE.JS
{const s=sl(); hd(s,"Demo 5 — Node.js Application Code");
cb(s,`const { MongoClient, ObjectId } = require("mongodb");\n\nasync function main() {\n  const client = new MongoClient(process.env.MONGO_URI);\n  await client.connect();\n  const db = client.db("shop");\n\n  // 1. Find completed orders for a customer, sorted by amount\n  const orders = await db.collection("orders")\n    .find({ custId: new ObjectId("cust001"), status: "completed" })\n    .sort({ amount: -1 })\n    .project({ items:1, amount:1, createdAt:1, _id:0 })\n    .toArray();\n\n  // 2. Upsert — insert if not exists, update if exists\n  await db.collection("customers").updateOne(\n    { email: "eve@example.com" },\n    { $set:{ name:"Eve Adams", region:"AMER", tier:"silver" },\n      $setOnInsert:{ createdAt: new Date() } },  // only on INSERT\n    { upsert: true }\n  );\n\n  // 3. Aggregation — revenue by region\n  const revenue = await db.collection("orders").aggregate([\n    { $match:  { status:"completed" } },\n    { $lookup: { from:"customers", localField:"custId",\n                 foreignField:"_id", as:"customer" } },\n    { $unwind: "$customer" },\n    { $group:  { _id:"$customer.region", total:{ $sum:"$amount" } } },\n    { $sort:   { total: -1 } }\n  ]).toArray();\n\n  // 4. Change Stream — react to new completed orders in real-time\n  const stream = db.collection("orders").watch(\n    [{ $match: { "fullDocument.status":"completed" } }],\n    { fullDocument: "updateLookup" }\n  );\n  stream.on("change", e => console.log("New order:", e.fullDocument.amount));\n\n  await client.close();\n}\nmain().catch(console.error);`,M,1.05,W-M*2,6.1);
s.addNotes(`$setOnInsert: only runs on INSERT path of upsert — createdAt never overwritten on update.\nChange Streams: event-driven, no poll interval. fullDocument:"updateLookup" returns full doc on update.\nTypeScript: db.collection<Order>("orders") → full type inference.`);}

// DEMO 6 — TRANSACTIONS
{const s=sl(); hd(s,"Demo 6 — Multi-Document Transaction");
s.addText("Scenario: place an order — atomically deduct inventory, create order, write audit log",{x:M,y:1.0,w:W-M*2,h:0.46,fontSize:16,color:GRAY,fontFace:F,margin:0});
cb(s,`db.inventory.insertMany([ { sku:"A1", qty:50 }, { sku:"B3", qty:20 } ])\n\nasync function placeOrder(client, custId, items) {\n  const session = client.startSession();\n  session.startTransaction({ readConcern:{level:"snapshot"}, writeConcern:{w:"majority"} });\n  try {\n    const db = client.db("shop");\n    // 1. Check & deduct inventory (compare-and-swap)\n    for (const item of items) {\n      const res = await db.collection("inventory").updateOne(\n        { sku:item.sku, qty:{ $gte:item.qty } },  // only if enough stock\n        { $inc:{ qty:-item.qty } }, { session }\n      );\n      if (res.matchedCount === 0) throw new Error(\`Insufficient stock: \${item.sku}\`);\n    }\n    // 2. Create order\n    const total = items.reduce((s,i)=>s+i.qty*i.price, 0);\n    const orderId = new ObjectId();\n    await db.collection("orders").insertOne(\n      { _id:orderId, custId, items, total, status:"pending", createdAt:new Date() }, { session }\n    );\n    // 3. Audit log\n    await db.collection("auditLog").insertOne(\n      { action:"order_placed", orderId, custId, total, ts:new Date() }, { session }\n    );\n    await session.commitTransaction();\n    return orderId;\n  } catch(err) {\n    await session.abortTransaction();  // ALL 3 operations rolled back\n    throw err;\n  } finally { session.endSession(); }\n}`,M,1.55,W-M*2,5.6);
s.addNotes(`Demo: insert inventory qty:2 for "A1". Try order qty:3 → thrown, abortTransaction, inventory unchanged. Order qty:1 → succeeds.\nDesign insight: "If order embeds items, creating an order IS one atomic write — no transaction needed. Embed first, transact when necessary."`);}

// ── Write ─────────────────────────────────────────────────────────────────────
pres.writeFile({fileName:"MongoDB_for_Relational_Developers.pptx"})
  .then(()=>console.log("✅  MongoDB_for_Relational_Developers.pptx — 33 slides, clean build"))
  .catch(e=>{console.error("❌",e);process.exit(1);});
