'use strict';
(function(){
const $=s=>document.querySelector(s);
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const slug=p=>(p.repo||p.nome).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'')||'projeto';
let DADOS=null, RESUMO={}, CACHE={}, CANAIS=null;
const siteHref=u=>/^https:\/\//.test(u||'')?u:'';
// projeto em modo público mínimo (gen/publico_minimo.json): só nome + site
const cardMinimo=(p,largo)=>`<article class="card${largo?' largo':''}"><h2>${esc(p.nome)}</h2>`+
  (siteHref(p.site)?`<p><a href="${esc(siteHref(p.site))}" rel="noopener">${esc(p.site.replace(/^https:\/\//,'').replace(/\/$/,''))}</a></p>`:'')+
  (p.nota?`<p class="dt">${esc(p.nota)}</p>`:'')+'</article>';
const ul=(arr)=>arr&&arr.length?'<ul>'+arr.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul>':'<p class="vazio">Nada registrado.</p>';

async function carregar(){
  const r=await fetch('data/projetos.json',{cache:'no-store'}); DADOS=await r.json();
  try{const i=await (await fetch('data/detalhes/index.json',{cache:'no-store'})).json();
    (i.projetos||[]).forEach(p=>RESUMO[p.slug]=p); DADOS._det_em=i.gerado_em;}catch(e){}
  try{CANAIS=await (await fetch('data/canais.json',{cache:'no-store'})).json();}catch(e){CANAIS=null;}
  const sel=$('#seletor');
  sel.innerHTML='<option value="">Visão geral (todos os projetos)</option>'+(CANAIS&&CANAIS.empresas&&CANAIS.empresas.length?'<option value="canais">Canais de venda (todas as empresas)</option>':'')+DADOS.projetos.map(p=>`<option value="${esc(slug(p))}">${esc(p.nome)}</option>`).join('');
  sel.addEventListener('change',()=>{location.hash=sel.value?sel.value:''; if(!sel.value) rota();});
  window.addEventListener('hashchange',rota);
  $('#gerado').textContent='gerado em '+DADOS.gerado_em;
  rota();
}
function rota(){
  const h=decodeURIComponent(location.hash.replace(/^#\/?/,'')).toLowerCase();
  const p=DADOS.projetos.find(x=>slug(x)===h);
  window.scrollTo(0,0);
  if(h==='canais'&&CANAIS){$('#seletor').value='canais'; document.title='Canais de venda · Painel de Controle'; canaisGeral(); return;}
  $('#seletor').value=p?slug(p):'';
  if(p){document.title=p.nome+' · Painel de Controle'; projeto(p);} else {document.title='Painel de Controle'; geral();}
}
function resumoTopo(){
  const ps=DADOS.projetos, gh=ps.filter(p=>(p.categoria||'').startsWith('GitHub')).length, nmin=ps.filter(p=>p.publico_minimo).length;
  const rs=Object.values(RESUMO).filter(r=>!r.publico_minimo), c7=rs.reduce((a,r)=>a+(r.commits_7d||0),0);
  const pend=rs.reduce((a,r)=>a+(r.pendencias||0),0);
  const ativos=rs.filter(r=>r.commits_7d).sort((a,b)=>b.commits_7d-a.commits_7d).slice(0,3).map(r=>r.nome);
  const it=[`${ps.length} projetos`,`${gh} no GitHub`,`${ps.length-gh-nmin} fora do GitHub`];
  if(rs.length){it.push(`${c7} commits nos últimos 7 dias`); it.push(`${pend} pendências abertas`); if(ativos.length) it.push('Mais ativos na semana: '+ativos.join(', '));}
  $('#sum').innerHTML=it.map(s=>'<div>'+esc(s)+'</div>').join('');
  $('#sum').hidden=false;
}
function geral(){
  resumoTopo();
  $('#main').innerHTML=cardResumoCanais()+DADOS.projetos.map(p=>{
    if(p.publico_minimo) return cardMinimo(p,false);
    const r=RESUMO[slug(p)]||{};
    let mini='';
    if(r.arquivo){
      mini='<div class="mini">'+[
        r.ultimo_commit?`Último commit: ${r.ultimo_commit}`:null,
        `${r.commits_7d} commit${r.commits_7d==1?'':'s'} em 7 dias`,
        r.pendencias!=null?`${r.pendencias} pendência${r.pendencias==1?'':'s'}`:null,
        r.prs_abertos?`${r.prs_abertos} PR${r.prs_abertos==1?' aberto':'s abertos'}`:null,
        r.tem_kpis?'Tem indicadores':null,
        r.canais_total?`${r.canais_aquisicao_ativos} canal${r.canais_aquisicao_ativos==1?'':'is'} de aquisição ativo${r.canais_aquisicao_ativos==1?'':'s'}`+(r.canais_alerta?' ⚠':''):null].filter(Boolean).map(s=>'<span>'+esc(s)+'</span>').join('')+'</div>';
    }
    return `<article class="card"><h2>${esc(p.nome)}</h2><span class="tag">${esc(p.categoria||'')}</span>`+
      (p.url?` <a href="${esc(p.url)}">repo</a> <small>(privado)</small>`:'')+mini+
      (p.objetivo?`<p><b>Objetivo:</b> ${esc(p.objetivo)}</p>`:'')+
      `<p><b>Status:</b> ${esc(p.status)}</p>`+
      (p.proximos&&p.proximos.length?'<p><b>Próximos passos:</b></p>'+ul(p.proximos.slice(0,3)):'')+
      (p.atualizado?`<p class="dt">Última atualização: ${esc(p.atualizado)}</p>`:'')+
      `<a class="btn" href="#${esc(slug(p))}">Ver painel completo →</a></article>`;
  }).join('');
}
function grafico(dias){
  const max=Math.max(1,...dias.map(d=>d.n));
  const fmt=d=>d.dia.slice(8,10)+'/'+d.dia.slice(5,7);
  return '<div class="grafico" role="img" aria-label="Commits por dia nos últimos 30 dias">'+dias.map(d=>
    `<div class="${d.n?'':'zero'}" style="height:${d.n?Math.max(4,100*d.n/max):2}%" title="${fmt(d)}: ${d.n} commit${d.n==1?'':'s'}"></div>`).join('')+
    `</div><div class="eixo"><span>${fmt(dias[0])}</span><span>commits por dia (máx. ${max})</span><span>${fmt(dias[dias.length-1])}</span></div>`;
}
function num(n){return `<div class="num"><b>${esc(n.valor)}</b><span>${esc(n.rotulo)}</span>${n.detalhe?'<small>'+esc(n.detalhe)+'</small>':''}</div>`;}
async function projeto(p){
  $('#sum').hidden=true;
  if(p.publico_minimo){$('#main').innerHTML=cardMinimo(p,true); return;}
  const s=slug(p), r=RESUMO[s];
  let d=null;
  if(r&&r.arquivo){ try{ d=CACHE[s]||(CACHE[s]=await (await fetch(r.arquivo,{cache:'no-store'})).json()); }catch(e){} }
  if(slug(DADOS.projetos.find(x=>slug(x)===decodeURIComponent(location.hash.slice(1)).toLowerCase())||{})!==s) return;
  const c=[];
  c.push(`<article class="card largo"><h2>${esc(p.nome)}</h2><span class="tag">${esc(p.categoria||'')}</span>`+
    (p.url?` <a href="${esc(p.url)}">abrir repositório</a> <small>(privado)</small>`:'')+
    (p.objetivo?`<p><b>Objetivo:</b> ${esc(p.objetivo)}</p>`:'')+`<p><b>Status:</b> ${esc(p.status)}</p>`+
    (p.origem?`<p class="dt">Origem: ${esc(p.origem)}</p>`:'')+
    (p.atualizado?`<p class="dt">Última atualização: ${esc(p.atualizado)}</p>`:'')+'</article>');
  if(d){
    const e=d.estatisticas;
    c.push(`<article class="card"><h3>Repositório</h3><div class="nums">`+[
      {rotulo:'Último commit',valor:e.ultimo_commit||'—',detalhe:'horário de Brasília'},
      {rotulo:'Commits em 7 dias',valor:e.commits_7d},{rotulo:'Commits em 30 dias',valor:e.commits_30d+(e.commits_30d_truncado?'+':'')},
      {rotulo:'Issues abertas',valor:e.issues_abertas},{rotulo:'PRs abertos',valor:e.prs_abertos},
      {rotulo:'Linguagem principal',valor:e.linguagem||'—',detalhe:(e.linguagens||[]).map(l=>l.nome+' '+String(l.pct).replace('.',',')+'%').join(' · ')}
    ].map(num).join('')+'</div>'+grafico(e.por_dia)+'</article>');
    const pd=d.pendencias;
    c.push(`<article class="card"><h3>Pendências${pd?'<span class="cont">'+pd.itens.length+'</span>':''}</h3>`+
      (pd?(pd.itens.length?'<ul>'+pd.itens.map(i=>'<li>'+esc(i.titulo)+(i.prazo?'<span class="prazo">até '+esc(i.prazo)+'</span>':'')+'</li>').join('')+'</ul>':'<p class="vazio">Nenhuma pendência aberta.</p>')+
        `<p class="dt">Fonte: ${esc(pd.fonte)}</p>`
        :'<p class="vazio">O repositório não tem PENDENCIAS.md nem seção de pendências.</p>')+'</article>');
  } else if(p.repo){
    c.push('<article class="card"><h3>Repositório</h3><p class="vazio">Dados do repositório ainda não foram gerados.</p></article>');
  }
  c.push(`<article class="card"><h3>Próximos passos</h3>${ul(p.proximos)}</article>`);
  if(d&&d.kpis){
    const k=d.kpis;
    let h=`<article class="card largo"><h3>${esc(k.titulo)}</h3>`;
    if(k.numeros&&k.numeros.length) h+='<div class="nums">'+k.numeros.map(num).join('')+'</div>';
    (k.tabelas||[]).forEach(t=>{h+=`<p><b>${esc(t.titulo||'')}</b></p><div class="tab"><table><thead><tr>${t.colunas.map(x=>'<th>'+esc(x)+'</th>').join('')}</tr></thead><tbody>${t.linhas.map(l=>'<tr>'+l.map(x=>'<td>'+esc(x)+'</td>').join('')+'</tr>').join('')}</tbody></table></div>`;});
    (k.listas||[]).forEach(l=>{
      h+=`<p><b>${esc(l.titulo)}</b>${l.tipo==='ajustes'?'<span class="cont">'+l.itens.length+'</span>':''}</p>`;
      if(l.tipo==='ajustes') h+='<ul>'+l.itens.map(i=>`<li><span class="pri p-${esc(i.prioridade)}">${esc(i.prioridade)}</span><b>${esc(i.cargo)}</b> · ${esc(i.titulo)} <small class="dt">(${esc(i.status)})</small></li>`).join('')+'</ul>';
      else h+=ul(l.itens);
    });
    h+=`<p class="dt">Fontes: ${esc((k.fontes||[]).join(', '))}${k.nota?' · '+esc(k.nota):''}</p></article>`;
    c.push(h);
  }
  const emp=empresaCanais(p);
  if(emp) c.push(cardCanaisProjeto(emp));
  let at=`<article class="card largo"><h3>Atividade recente</h3>`;
  if(p.recente&&p.recente.length) at+='<p><b>Resumo do dia:</b></p>'+ul(p.recente);
  if(d&&d.commits&&d.commits.length) at+='<p><b>Últimos commits</b> (horário de Brasília):</p><ul class="commits">'+d.commits.map(m=>`<li><span class="q">${esc(m.quando)}</span>${esc(m.msg)} <code>${esc(m.sha)}</code></li>`).join('')+'</ul>';
  if(d) at+=`<p class="dt">Dados do repositório gerados em ${esc(d.gerado_em)} (horário de Brasília).</p>`;
  c.push(at+'</article>');
  if(!p.repo) c.push('<article class="card"><h3>Sem repositório</h3><p class="vazio">Este projeto não está no GitHub; só há os dados do resumo diário.</p></article>');
  $('#main').innerHTML=c.join('');
}

// ---------------------------------------------------------------- canais de venda
const ORDEM_ST={'ativo':0,'em teste':1,'parado':2,'planejado':3,'encerrado':4};
const COLS=[['alcance','Alcance / visitas'],['cliques','Cliques'],['leads','Leads'],['vendas','Vendas'],['receita','Receita']];
const empresaCanais=p=>CANAIS&&p.repo?(CANAIS.empresas||[]).find(e=>e.repo===p.repo):null;
const stBadge=c=>`<span class="st st-${esc(c.status.replace(' ','-'))}">${esc(c.status)}</span>`;
function valor(m,dc){
  if(!m||m.valor==null||m.valor==='') return `<span class="sd">sem dado</span>${m&&m.nota?'<small>'+esc(m.nota)+'</small>':''}`;
  const quando=m.mantido?`<small class="mant">mantido · medido em ${esc(m.medido_em||'?')}</small>`:(m.medido_em&&m.medido_em!==dc?`<small>medido em ${esc(m.medido_em)}</small>`:'');
  return `<b>${esc(m.valor)}</b>${m.nota?'<small>'+esc(m.nota)+'</small>':''}${quando}`;
}
function ordenar(l){return l.slice().sort((a,b)=>(ORDEM_ST[a.status]??9)-(ORDEM_ST[b.status]??9)||(a.tipo===b.tipo?0:a.tipo==='aquisição'?-1:1));}
function linhaCanal(c,emp){
  const det=[];
  if(c.motivo) det.push(`<b>Motivo:</b> ${esc(c.motivo)}`);
  if(c.hipotese) det.push(`<b>Hipótese:</b> ${esc(c.hipotese)}`);
  if(c.metrica) det.push(`<b>Métrica:</b> ${esc(c.metrica)}`);
  if(c.inicio||c.prazo) det.push(`<b>Início:</b> ${esc(c.inicio||'—')}${c.prazo?' · <b>Prazo:</b> '+esc(c.prazo):''}`);
  if(c.resultado) det.push(`<b>Resultado (registro do CMO):</b> ${esc(c.resultado)}`);
  (c.outros||[]).forEach(o=>det.push(`<b>${esc(o.rotulo)}:</b> ${o.valor==null?'sem dado':esc(o.valor)}${o.mantido?` <small class="mant">mantido · ${esc(o.medido_em||'')}</small>`:''}`));
  if(c.decisao) det.push(`<b>Decisão:</b> ${esc(c.decisao)}`);
  const motivoCurto=(c.status==='encerrado'||c.status==='parado')&&c.motivo?`<small class="mot">${esc(c.motivo)}</small>`:'';
  return `<tr class="${c.status==='encerrado'?'enc':''}">`+(emp?`<td data-r="Empresa"><a href="#${esc(emp.slug)}">${esc(emp.nome)}</a></td>`:'')+
    `<td data-r="Canal" class="cn"><b>${esc(c.canal)}</b>${c.canal_mantido?'<small class="mant">mantido do registro anterior</small>':''}${det.length?`<details><summary>detalhes</summary><ul>${det.map(x=>'<li>'+x+'</li>').join('')}</ul></details>`:''}</td>`+
    `<td data-r="Tipo">${esc(c.tipo)}</td><td data-r="Status">${stBadge(c)}${motivoCurto}</td>`+
    COLS.map(([k,r])=>`<td data-r="${r}" class="v">${valor((c.numeros||{})[k],c.medido_em)}</td>`).join('')+
    `<td data-r="Período / medição">${esc(c.periodo||'—')}${c.medido_em?'<small>'+(COLS.some(([k])=>c.numeros&&c.numeros[k]&&c.numeros[k].valor!=null)?'medido em ':'registro de ')+esc(c.medido_em)+'</small>':''}</td>`+
    `<td data-r="Fonte" class="fo">${esc(c.fonte||'—')}</td></tr>`;
}
function tabelaCanais(linhas,comEmpresa){
  return `<div class="tab tabc"><table class="canais"><thead><tr>${comEmpresa?'<th>Empresa</th>':''}<th>Canal</th><th>Tipo</th><th>Status</th>${COLS.map(c=>'<th>'+c[1]+'</th>').join('')}<th>Período / medição</th><th>Fonte</th></tr></thead><tbody>${linhas.join('')}</tbody></table></div>`;
}
function contagem(emp){
  const ct=emp.contagem||{};
  return [
    {rotulo:'Canais de aquisição ativos',valor:emp.aquisicao_ativos,detalhe:(emp.canais_aquisicao_ativos||[]).length>3?'ver tabela':((emp.canais_aquisicao_ativos||[]).join(' · ')||'nenhum')},
    {rotulo:'Canais de venda ativos',valor:emp.venda_ativos,detalhe:'checkout / cobrança'},
    {rotulo:'Em teste',valor:ct['em teste']||0,detalhe:'contam como ativos'},
    {rotulo:'Parados',valor:ct['parado']||0},{rotulo:'Planejados',valor:ct['planejado']||0},{rotulo:'Encerrados',valor:ct['encerrado']||0}];
}
const alertaHtml=emp=>emp.alerta?`<p class="alerta">⚠ ${esc(emp.alerta)}</p>`:'';
const legenda='<p class="dt">"sem dado" = métrica não medida na fonte. "mantido" = valor da última medição conhecida (não veio na coleta de hoje). Ativos = status ativo ou em teste; canais do mesmo grupo (ex.: ondas de e-mail) contam uma vez.</p>';
function cardCanaisProjeto(emp){
  const regs=(emp.registros_do_projeto||[]).length?'Registro de canais do projeto: '+emp.registros_do_projeto.join(', '):'O projeto ainda não tem registro de canais (canais.json ou CANAIS.md); usando o registro do painel e a extração automática.';
  return `<article class="card largo"><h3>Canais de venda<span class="cont">${emp.canais.length}</span></h3>${alertaHtml(emp)}<div class="nums">${contagem(emp).map(num).join('')}</div>`+
    tabelaCanais(ordenar(emp.canais).map(c=>linhaCanal(c,null)),false)+`<p class="dt">${esc(regs)}</p>${legenda}<p class="dt"><a href="#canais">Comparar com as outras empresas →</a></p></article>`;
}
function cardResumoCanais(){
  if(!CANAIS||!(CANAIS.empresas||[]).length) return '';
  const es=CANAIS.empresas;
  return `<article class="card largo"><h2>Canais de venda</h2><div class="mini">${es.map(e=>`<span>${esc(e.nome)}: ${e.aquisicao_ativos} canal${e.aquisicao_ativos==1?'':'is'} de aquisição ativo${e.aquisicao_ativos==1?'':'s'}${e.alerta?' ⚠':''}</span>`).join('')}</div>`+
    (es.some(e=>e.alerta)?`<p class="alerta">⚠ Só 1 canal de aquisição ativo: ${esc(es.filter(e=>e.alerta).map(e=>e.nome).join(', '))}.</p>`:'')+
    `<a class="btn" href="#canais">Ver todos os canais →</a></article>`;
}
function canaisGeral(){
  const es=CANAIS.empresas||[];
  const tot=es.reduce((a,e)=>a+e.canais.length,0), at=es.reduce((a,e)=>a+e.aquisicao_ativos,0);
  $('#sum').innerHTML=[`${es.length} empresas com canais`,`${tot} canais registrados`,`${at} canais de aquisição ativos`,`${es.filter(e=>e.alerta).length} com só 1 canal ativo`].map(s=>'<div>'+esc(s)+'</div>').join('');
  $('#sum').hidden=false;
  const c=[];
  c.push(`<article class="card largo"><h2>Canais de venda e aquisição</h2><p>Cada canal de cada empresa, com status e números principais. ${esc(CANAIS.nota||'')}</p>`+
    `<div class="tab tabc"><table class="comp"><thead><tr><th>Empresa</th><th>Aquisição ativos</th><th>Venda ativos</th><th>Em teste</th><th>Parados</th><th>Planejados</th><th>Encerrados</th><th>Alerta</th></tr></thead><tbody>`+
    es.map(e=>{const ct=e.contagem||{};return `<tr><td data-r="Empresa"><a href="#${esc(e.slug)}">${esc(e.nome)}</a></td><td data-r="Aquisição ativos"><b>${e.aquisicao_ativos}</b></td><td data-r="Venda ativos">${e.venda_ativos}</td><td data-r="Em teste">${ct['em teste']||0}</td><td data-r="Parados">${ct['parado']||0}</td><td data-r="Planejados">${ct['planejado']||0}</td><td data-r="Encerrados">${ct['encerrado']||0}</td><td data-r="Alerta">${e.alerta?'<span class="alerta-i">⚠ '+esc(e.alerta)+'</span>':'—'}</td></tr>`;}).join('')+
    `</tbody></table></div><p class="dt">Gerado em ${esc(CANAIS.gerado_em||'')}.</p>${legenda}</article>`);
  es.forEach(e=>{
    c.push(`<article class="card largo"><h3><a href="#${esc(e.slug)}">${esc(e.nome)}</a><span class="cont">${e.canais.length}</span></h3>${alertaHtml(e)}`+
      tabelaCanais(ordenar(e.canais).map(x=>linhaCanal(x,null)),false)+
      ((e.registros_do_projeto||[]).length?`<p class="dt">Registro de canais do projeto: ${esc(e.registros_do_projeto.join(', '))}</p>`:'<p class="dt">Sem registro de canais próprio do projeto: registro do painel + extração automática.</p>')+`</article>`);
  });
  $('#main').innerHTML=c.join('');
}
carregar().catch(e=>{$('#main').innerHTML='<article class="card"><h2>Erro ao carregar os dados</h2><p>'+esc(e.message)+'</p></article>';});
})();
