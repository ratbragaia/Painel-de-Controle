'use strict';
(function(){
const $=s=>document.querySelector(s);
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const slug=p=>(p.repo||p.nome).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'')||'projeto';
let DADOS=null, RESUMO={}, CACHE={};
const ul=(arr)=>arr&&arr.length?'<ul>'+arr.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul>':'<p class="vazio">Nada registrado.</p>';

async function carregar(){
  const r=await fetch('data/projetos.json',{cache:'no-store'}); DADOS=await r.json();
  try{const i=await (await fetch('data/detalhes/index.json',{cache:'no-store'})).json();
    (i.projetos||[]).forEach(p=>RESUMO[p.slug]=p); DADOS._det_em=i.gerado_em;}catch(e){}
  const sel=$('#seletor');
  sel.innerHTML='<option value="">Visão geral (todos os projetos)</option>'+DADOS.projetos.map(p=>`<option value="${esc(slug(p))}">${esc(p.nome)}</option>`).join('');
  sel.addEventListener('change',()=>{location.hash=sel.value?sel.value:''; if(!sel.value) rota();});
  window.addEventListener('hashchange',rota);
  $('#gerado').textContent='gerado em '+DADOS.gerado_em;
  rota();
}
function rota(){
  const h=decodeURIComponent(location.hash.replace(/^#\/?/,'')).toLowerCase();
  const p=DADOS.projetos.find(x=>slug(x)===h);
  $('#seletor').value=p?slug(p):'';
  window.scrollTo(0,0);
  if(p){document.title=p.nome+' · Painel de Controle'; projeto(p);} else {document.title='Painel de Controle'; geral();}
}
function resumoTopo(){
  const ps=DADOS.projetos, gh=ps.filter(p=>(p.categoria||'').startsWith('GitHub')).length;
  const rs=Object.values(RESUMO), c7=rs.reduce((a,r)=>a+(r.commits_7d||0),0);
  const pend=rs.reduce((a,r)=>a+(r.pendencias||0),0);
  const ativos=rs.filter(r=>r.commits_7d).sort((a,b)=>b.commits_7d-a.commits_7d).slice(0,3).map(r=>r.nome);
  const it=[`${ps.length} projetos`,`${gh} no GitHub`,`${ps.length-gh} fora do GitHub`];
  if(rs.length){it.push(`${c7} commits nos últimos 7 dias`); it.push(`${pend} pendências abertas`); if(ativos.length) it.push('Mais ativos na semana: '+ativos.join(', '));}
  $('#sum').innerHTML=it.map(s=>'<div>'+esc(s)+'</div>').join('');
  $('#sum').hidden=false;
}
function geral(){
  resumoTopo();
  $('#main').innerHTML=DADOS.projetos.map(p=>{
    const r=RESUMO[slug(p)]||{};
    let mini='';
    if(r.arquivo){
      mini='<div class="mini">'+[
        r.ultimo_commit?`Último commit: ${r.ultimo_commit}`:null,
        `${r.commits_7d} commit${r.commits_7d==1?'':'s'} em 7 dias`,
        r.pendencias!=null?`${r.pendencias} pendência${r.pendencias==1?'':'s'}`:null,
        r.prs_abertos?`${r.prs_abertos} PR${r.prs_abertos==1?' aberto':'s abertos'}`:null,
        r.tem_kpis?'Tem indicadores':null].filter(Boolean).map(s=>'<span>'+esc(s)+'</span>').join('')+'</div>';
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
  let at=`<article class="card largo"><h3>Atividade recente</h3>`;
  if(p.recente&&p.recente.length) at+='<p><b>Resumo do dia:</b></p>'+ul(p.recente);
  if(d&&d.commits&&d.commits.length) at+='<p><b>Últimos commits</b> (horário de Brasília):</p><ul class="commits">'+d.commits.map(m=>`<li><span class="q">${esc(m.quando)}</span>${esc(m.msg)} <code>${esc(m.sha)}</code></li>`).join('')+'</ul>';
  if(d) at+=`<p class="dt">Dados do repositório gerados em ${esc(d.gerado_em)} (horário de Brasília).</p>`;
  c.push(at+'</article>');
  if(!p.repo) c.push('<article class="card"><h3>Sem repositório</h3><p class="vazio">Este projeto não está no GitHub; só há os dados do resumo diário.</p></article>');
  $('#main').innerHTML=c.join('');
}
carregar().catch(e=>{$('#main').innerHTML='<article class="card"><h2>Erro ao carregar os dados</h2><p>'+esc(e.message)+'</p></article>';});
})();
