// Minimal DOM stub: runs script.js against the ids present in each dashboard page, reports thrown errors.
const fs=require('fs');
const pages=['dashboard','monitor','analytics','zones','controls'];
let bad=0;
for(const p of pages){
  const src=fs.readFileSync(p+'.html','utf8');
  const ids=[...src.matchAll(/id="([^"]+)"/g)].map(m=>m[1]);
  const els={};
  const mk=(id)=>{const e={id,dataset:{},style:{},hidden:false,value:'',textContent:'',innerHTML:'',className:'',disabled:false,options:[],width:1000,height:300,
    classList:{add(){},remove(){},toggle(){}},setAttribute(){},appendChild(){},querySelector:()=>mk('x'),addEventListener(){},
    getContext:()=>new Proxy({},{get:(t,k)=>k==='measureText'?()=>({width:0}):()=>{},set:()=>true})};return e;};
  ids.forEach(i=>els[i]=mk(i));
  if(els.area)els.area.value='residential'; if(els.period)els.period.value='day'; if(els.calib)els.calib.value='90';
  global.window=global; global.document={getElementById:i=>els[i]||null,documentElement:{dataset:{}},createElement:()=>mk('c'),body:{appendChild(){}}};
  global.getComputedStyle=()=>({getPropertyValue:()=>'#4f46e5'});
  global.localStorage={getItem:()=>null,setItem(){}}; global.MutationObserver=function(){this.observe=()=>{}};
  global.addEventListener=()=>{}; global.navigator={}; global.confirm=()=>true;
  global.SN_USER='a@b.c'; delete global.SN_DATA;
  try{
    eval(fs.readFileSync('data/demo-data.js','utf8')); eval(fs.readFileSync('script.js','utf8'));
    if(els.startDemo){els.startDemo.onclick(); }
    if(els.stop&&els.stop.onclick)els.stop.onclick();
    if(els.exportCsv&&els.exportCsv.onclick)els.exportCsv.onclick();
    console.log('OK  ',p);
  }catch(e){bad++;console.log('FAIL',p,e.message)}
}
process.exit(bad?1:0);
