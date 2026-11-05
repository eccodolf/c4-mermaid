// Optional live browser test. Use pre-provisioned Playwright and Chromium; never download them.
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs/promises'),path=require('node:path');
const {chromium}=require(process.env.C4_PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),output=process.env.C4_TEST_OUTPUT||path.join(process.cwd(),'work','c4-mermaid-browser-review');

function geometrySignature(group,ox,oy){
 const tags=new Set(['path','rect','ellipse','circle','line','polyline','polygon']),allowed=new Set(['d','x','y','cx','cy','x1','x2','y1','y2','width','height','rx','ry','r','fill','stroke','stroke-width','stroke-dasharray','transform']);
 const round=value=>Math.round(value*10000)/10000;
 const result=[];
 for(const element of group.querySelectorAll('*')){
  if(!tags.has(element.localName))continue;
  const attrs={};
  for(const attribute of element.attributes){
   const key=attribute.name,value=attribute.value;if(!allowed.has(key))continue;
   if(key==='d'){
    const tokens=value.match(/[A-Za-z]|[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?/g),values=[];let command,index=0;
    const counts={M:2,L:2,C:6,Q:4,H:1,V:1,Z:0};
    while(index<tokens.length){if(/^[A-Za-z]$/.test(tokens[index])){command=tokens[index++];values.push(command);}assertCommand(command);const count=counts[command];if(!count){command=null;continue;}for(let i=0;i<count;i++)values.push(round(Number(tokens[index+i])-(command==='H'||(command!=='V'&&i%2===0)?ox:oy)));index+=count;}
    attrs.d=values;
    function assertCommand(command){if(!(command in counts))throw Error('Unexpected native path command: '+command);}
   }else if(['x','cx','x1','x2'].includes(key))attrs[key]=round(Number(value)-ox);
   else if(['y','cy','y1','y2'].includes(key))attrs[key]=round(Number(value)-oy);
   else if(['width','height','rx','ry','r','stroke-width'].includes(key))attrs[key]=round(Number(value));
   else if(key==='transform'&&value.startsWith('rotate(')){const numbers=value.match(/[-+]?(?:\d*\.\d+|\d+\.?)/g).map(Number);attrs.transform=['rotate',numbers[0],round(numbers[1]-ox),round(numbers[2]-oy)];}
   else attrs[key]=value.toLowerCase();
  }
  result.push({tag:element.localName,attrs});
 }
 return result;
}

(async()=>{
 await fs.mkdir(output,{recursive:true});
 const options={headless:true};if(process.env.C4_BROWSER_EXECUTABLE)options.executablePath=process.env.C4_BROWSER_EXECUTABLE;
 const browser=await chromium.launch(options);
 const report={mermaid:'12.3.0',drawio:'32.6.10',examples:[],geometryMatches:0,rejections:[],externalRequests:[]};
 try{
  const context=await browser.newContext({acceptDownloads:true,viewport:{width:2000,height:1400}});
  await context.route('**/*',route=>route.request().url().startsWith('file:')?route.continue():(report.externalRequests.push(route.request().url()),route.abort()));
  const page=await context.newPage();await page.goto('file:///'+path.join(root,'assets/offline/viewer.html').replaceAll('\\','/'));
  async function render(source,overrideLegend){
   const legend=overrideLegend??source.split('\n').filter(line=>line.startsWith('%% legend:')).map(line=>line.slice(10).trim()).join('\n');
   await page.locator('#source').fill(source);await page.locator('#legend').fill(legend);await page.locator('#render').click();
   await page.waitForFunction(()=>!document.querySelector('#status').textContent.startsWith('Rendering...'),null,{timeout:30000});
   const status=await page.locator('#status').innerText();assert.equal(await page.locator('#download-png').isDisabled(),await page.locator('#download').isDisabled(),'PNG and SVG must share validation gates.');return {status,success:!(await page.locator('#download').isDisabled())};
  }
  async function save(name){const pending=page.waitForEvent('download');await page.locator('#download').click();await(await pending).saveAs(path.join(output,name+'.svg'));}
  for(const name of (await fs.readdir(path.join(root,'assets/templates'))).filter(name=>name.endsWith('.mmd'))){
   const source=await fs.readFile(path.join(root,'assets/templates',name),'utf8'),result=await render(source);assert.equal(result.success,true,name+': '+result.status);
   if(source.startsWith('drawioC4'))assert.equal(await page.locator('#preview svg').getAttribute('data-c4-native-renderer'),'drawio-32.6.10');
   await save(name.replace('.mmd',''));report.examples.push(name);
   const pendingPng=page.waitForEvent('download');await page.locator('#download-png').click();const target=path.join(output,name.replace('.mmd','-viewer.png'));await(await pendingPng).saveAs(target);const bytes=await fs.readFile(target);assert.equal(bytes.subarray(0,8).toString('hex'),'89504e470d0a1a0a',name+' must export a real PNG.');assert.ok(bytes.readUInt32BE(16)>0&&bytes.readUInt32BE(20)>0);
  }
  const catalog=await fs.readFile(path.join(root,'assets/drawio/shapes.mmd'),'utf8');
  const model=JSON.parse(await fs.readFile(path.join(root,'assets/drawio/shapes.json'),'utf8'));
  const reference=JSON.parse(await fs.readFile(path.join(root,'assets/drawio-c4/native-fidelity.json'),'utf8'));
  for(const scheme of ['light','dark']){
   await page.emulateMedia({colorScheme:scheme});const result=await render(catalog);assert.equal(result.success,true,result.status);
   const raw=await page.evaluate(model=>Object.fromEntries(model.pages[0].elements.map(node=>[node.id,[...document.querySelector('[data-c4-id="'+node.id+'"] [data-c4-shape]').querySelectorAll('*')].map(element=>({localName:element.localName,attributes:[...element.attributes].map(attribute=>({name:attribute.name,value:attribute.value}))}))])),model);
   const actual=Object.fromEntries(model.pages[0].elements.map(node=>[node.id,geometrySignature({querySelectorAll:()=>raw[node.id]},node.x,node.y)]));
   for(const[id,shape]of Object.entries(reference.shapes))assert.deepEqual(actual[id],shape.primitives,scheme+': '+id+' differs from actual draw.io vector geometry.');
   const svg=await page.locator('#preview svg').evaluate(svg=>svg.outerHTML);assert.equal(/<image\b|<foreignObject\b|light-dark\(/.test(svg),false,'Exact SVG must use standalone native vector primitives and fixed colors.');
   const resources=await page.locator('#preview svg').evaluate(svg=>[...svg.querySelectorAll('*')].flatMap(element=>[...element.attributes].flatMap(attribute=>[...attribute.value.matchAll(/url\(\s*["']?([^\)"']+)["']?\s*\)/g)].map(match=>match[1]))));assert.ok(resources.every(reference=>reference.startsWith('#')),'Export contains a document/external resource reference.');
   report.geometryMatches=Object.keys(actual).length;
  }
  await page.emulateMedia({colorScheme:'light'});await render(catalog);await save('shapes-mermaid');
  const source=await fs.readFile(path.join(root,'assets/drawio/container.mmd'),'utf8');assert.equal((await render(source)).success,true);await save('container-mermaid');
  const expectedEdges=JSON.parse(await fs.readFile(path.join(root,'assets/drawio/container.json'),'utf8')).pages[0].relationships;
  const paintedEdges=await page.locator('[data-c4-relationship]').evaluateAll(edges=>edges.map(edge=>({id:edge.getAttribute('data-c4-relationship'),source:edge.getAttribute('data-c4-source'),target:edge.getAttribute('data-c4-target'),arrow:!!edge.querySelector('[data-c4-arrowhead="target"]')})));
  assert.deepEqual(paintedEdges,expectedEdges.map(edge=>({id:edge.id,source:edge.source,target:edge.target,arrow:true})));
  const pngPending=page.waitForEvent('download');await page.locator('#download-png').click();const pngPath=path.join(output,'container-browser.png');await(await pngPending).saveAs(pngPath);const png=await fs.readFile(pngPath);assert.equal(png.subarray(0,8).toString('hex'),'89504e470d0a1a0a');assert.ok(png.readUInt32BE(16)>0&&png.readUInt32BE(20)>0);report.pngExport={width:png.readUInt32BE(16),height:png.readUInt32BE(20)};
  const inverted=source.replace('Rel(customer, web,','Rel(web, customer,');assert.equal((await render(inverted)).success,false,'Swapped semantic endpoints must fail against routing metadata.');report.rejections.push('reversed source endpoints');
  const originalStyle=await page.evaluate(()=>C4_DRAWIO_DATA.entries['Relationship with description and technology'].style);await page.evaluate(()=>{C4_DRAWIO_DATA.entries['Relationship with description and technology'].style=C4_DRAWIO_DATA.entries['Relationship with description and technology'].style.replace('endArrow=blockThin','endArrow=none');});assert.equal((await render(source)).success,false,'Missing painted arrowhead must block rendering.');report.rejections.push('missing arrowhead');await page.evaluate(style=>{C4_DRAWIO_DATA.entries['Relationship with description and technology'].style=style;},originalStyle);
  const escaped=catalog.replace('System(sample_2, "System"','System(sample_2, "A&amp;B &quot;Q&quot; &lt;svc&gt; &bsol; P"');assert.equal((await render(escaped)).success,true);const escapedText=await page.locator('[data-c4-id="sample_2"]').textContent();assert.ok(escapedText.includes('A&B "Q" <svc> \\ P'),JSON.stringify(escapedText));
  const line=catalog.split('\n').find(line=>line.startsWith('%% drawio-layout:'));
  const layout=JSON.parse(line.slice('%% drawio-layout:'.length));
  const substitutions=[['semantic override',()=>{const value=structuredClone(layout);value.nodes.sample_2.type='container';return catalog.replace(line,'%% drawio-layout: '+JSON.stringify(value));}],['wrong data-store shape',()=>{const value=structuredClone(layout);value.nodes.sample_7.subtype='browser';return catalog.replace(line,'%% drawio-layout: '+JSON.stringify(value));}],['overlapping cells',()=>{const value=structuredClone(layout);value.nodes.sample_external_person.x=value.nodes.sample_1.x;return catalog.replace(line,'%% drawio-layout: '+JSON.stringify(value));}],['text overflow',()=>catalog.replace('"Vector shape sample"','"'+('Very long text '.repeat(150))+'"')],['missing layout',()=>catalog.replace(line,'')],['plain simplified C4',()=> 'C4Context\nPerson(p,"Person")\n%% legend: Person = actor.'],['generic flowchart',()=> 'flowchart LR\nA[Person]-->B[System]\n%% legend: Actor and system.'],['remote source',()=>catalog+'\nclick person "https://invalid.example"']];
  for(const[name,make]of substitutions){const result=await render(make());assert.equal(result.success,false,name+' was not rejected.');report.rejections.push(name);}
  assert.equal((await render(source,' ')).success,false);report.rejections.push('blank legend');
  assert.equal((await render(source)).success,true,'Renderer must recover after rejected inputs.');
  assert.deepEqual(report.externalRequests,[],'No network request may be made by the renderer.');
  await fs.writeFile(path.join(output,'review.json'),JSON.stringify(report,null,2)+'\n');
  process.stdout.write('Exact Mermaid browser checks passed: 9 examples, 12/12 native vector shapes in light/dark modes, 11 rejected invalid inputs and local PNG export, no network requests.\n');
 }finally{await browser.close();}
})().catch(error=>{process.stderr.write(error.stack+'\n');process.exit(1);});
