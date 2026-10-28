import json
P='data/projetos.json'
d=json.load(open(P,encoding='utf-8'))
d['gerado_em']='28/10/2026 08:20 (horário de Brasília)'
by={p.get('repo'):p for p in d['projetos']}
a=by['abriuagora']
a['status']=("Em operação ativa, mas o funil segue em zero: Portão 1 em 0 de 3 amostras a 3 dias do prazo (31/10), ~141 e-mails de prospecção entregues, 120 convites e 1 clique em 14 dias. "
 "Em 27/10 entraram no ar 438 páginas de busca por cidade e ramo com dados reais (teto de US$ 35 no crédito da API) e a amostra direta: até 15 escritórios recebem 10 empresas da cidade prontas, com envio previsto para 28/10 09:45. "
 "A oferta de troca (plano anual) segue pronta e desligada até 30/10; a linha de indicação espera o OK do CLO em 29/10. Conta no Asaas ainda pendente.")
a['recente']=[
 "27/10 23:39 – amostra direta: até 15 escritórios recebem 10 empresas da cidade prontas",
 "27/10 21:27 – páginas por cidade e ramo: lote 2 com 56 páginas",
 "27/10 20:45 – 438 páginas de busca por cidade e ramo com dados reais",
 "27/10 12:08 – chamada para a amostra logo abaixo dos números nas 19 páginas de cidade",
 "27/10 08:45 – CEO: Portão 1 em 0 de 3; canal novo da semana cobrado",
]+a['recente'][:1]
a['proximos']=[
 "Envio das 15 amostras diretas em 28/10 09:45 e métrica diária",
 "Leitura do teste de parceria em 28/10 (decisão em 04/11)",
 "OK do CLO na linha de indicação em 29/10",
 "Portão 1 em 31/10; troca de oferta pronta se falhar",
 "Rodrigo cadastrar a conta bancária no Asaas",
]
a['atualizado']='28/10/2026 06:07'
f=by['finbook']
f['status']=("finbook.com.br no ar (site 200). Ainda 0 vendas; meta de 1ª venda até 31/10 provavelmente não será batida. "
 "Visitas em 7 dias: 38 (meta da semana 75); o Short 10 do perdão chegou a 228 views. Em 27/10 a página do perdão foi alinhada à FAQ da PGFN, a página GEO entrou no ar e o post 10 saiu na Página do Facebook. "
 "O canal novo da semana é a indexação das 2 calculadoras no Google/Bing. À noite ficaram prontos 12 artigos e 25 Shorts + 3 vídeos longos em texto, e o CEO decidiu (D-022) publicar o estoque antes de produzir mais: ≥1 Short por dia com link do artigo.")
f['recente']=[
 "27/10 23:26 – CEO D-022: estoque primeiro, 1 Short por dia e métrica diária",
 "27/10 22:23 – 12 artigos SEO/GEO e Shorts s37–s51 prontos",
 "27/10 20:41 – 25 Shorts e 3 vídeos longos em texto prontos",
 "27/10 20:23 – CEO: resumo diário (0 venda)",
 "27/10 11:00 – página do perdão alinhada à PGFN e página GEO no ar; post 10 no Facebook",
]
f['proximos']=[
 "CMO+CLO revisarem os artigos a01–a12 até 29/10; COO publica até 30/10",
 "≥1 Short por dia com link do artigo (T-074)",
 "Placar do lote 5 de parceiros e 1º lote do C-004 em 28/10",
 "WhatsApp/Telegram próprios no chip da empresa (T-077)",
]
f['atualizado']='27/10/2026 23:26'
v=by['vagassjdr']
v['status']=("Publicação em dia: 124 vagas em outubro e a 1ª vaga aprovada pelo Telegram publicada em 27/10. Receita de outubro em R$ 20 (cerca de 7% da meta de ~R$ 300, que não será batida); 0 Pix desde 20/10. "
 "Instagram com 354.737 visualizações em 28 dias. Em 27/10 o CMO abriu o canal novo da semana, a página \"Vagas de hoje em SJDR\" (no ar, link ainda não divulgado), e o Instagram passou a usar o número da empresa. "
 "Achado novo para o CTO hoje: a IA do Direct aceitou uma confirmação de pagamento falsa (T-051, urgente). A aquisição ainda depende só do Instagram.")
v['recente']=[
 "27/10 22:40 – COO: mensagem dupla corrigida; achado de pagamento falso para o CTO (T-051)",
 "27/10 18:55 – CEO: resumo (124 vagas em outubro, receita R$ 20)",
 "27/10 12:39 – 1ª vaga aprovada pelo Telegram publicada",
 "27/10 10:58 – página \"Vagas de hoje em SJDR\" no ar (link ainda não divulgado)",
 "27/10 08:30 – CEO: Fixado mantém a regra atual (T-037)",
]
v['proximos']=[
 "CTO: corrigir a IA do Direct contra pagamento falso (T-051, 28/10)",
 "Rascunhos prontos para o CLO até 28/10 22h; CLO confere em 29/10",
 "Divulgar o link da página nova e contar 14 dias de teste",
 "Rodrigo: créditos da API até 04/11 (pagamento)",
]
v['atualizado']='28/10/2026 04:37'
p=by['PatentSonar']
p['status']=("Em operação: 72 primeiros contatos enviados até 27/10 e 0 respostas (meta de 150 até 31/10). "
 "Em 27–28/10 o COO montou a estratégia da semana (follow-up dos contatos, Panorama como isca, métrica diária): 11 follow-ups a compradores, 4 a parceiros e 5 à imprensa ficaram na fila após o crítico, 4 primeiros contatos novos foram preparados e a semana 44 já tem 11 contatos novos. "
 "Com o crédito promocional da API foram coletadas 929 famílias para o Panorama 2025-26 e 906 para 2023-24 (US$ 3,54 de US$ 35). Site com home mais curta e descrições novas; nas buscas, 128 impressões e 0 cliques em 8 páginas. Atualizações de segurança feitas (0 vulnerabilidades).")
p['recente']=[
 "28/10 07:10 – Panorama 2023-24 coletado (906 famílias; US$ 3,54 de 35 no total)",
 "28/10 05:48 – 4 primeiros contatos novos na fila após o crítico; 11 novos na semana 44",
 "28/10 05:28 – 11 follow-ups a compradores na fila após o crítico",
 "28/10 05:08 – linha de base da busca: 128 impressões, 0 cliques; descrições novas",
 "28/10 04:08 – Panorama 2025-26 coletado e documento gerado (929 famílias)",
 "27/10 13:16 – atualizações de segurança: 0 vulnerabilidades",
]
p['proximos']=[
 "Enviar os follow-ups em fila a partir de 29–30/10",
 "Checkpoint dos 150 contatos em 31/10",
 "Usar o Panorama como isca nos contatos",
]
p['atualizado']='28/10/2026 07:10'
json.dump(d,open(P,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
open(P,'a').write('\n')

B='gen/resumo_base.json'
r=json.load(open(B,encoding='utf-8'))
def setr(emp,iid,val):
  for e in r['empresas']:
    if e['nome']==emp:
      for i in e['indicadores']:
        if i['id']==iid: i['resultado']=val
setr('PatentSonar','contatos',{"texto":"72","num":72,"medido_em":"2026-10-28 05:09","fonte":"métrica diária do COO (fila de 28/10, dado de 27/10)"})
setr('PatentSonar','resposta',{"texto":"0 de 72 (0 %)","num":0,"medido_em":"2026-10-28 05:09","fonte":"métrica diária do COO (fila de 28/10, dado de 27/10)"})
ab={"medido_em":"2026-10-27 08:45","fonte":"resumo do CEO de 27/10 (resumos-clevels)"}
setr('Abriu Agora','amostras',dict(texto="0",num=0,**ab))
setr('Abriu Agora','pagantes',dict(texto="0",num=0,**ab))
fb={"medido_em":"2026-10-27 08:40","fonte":"ciclo da manhã do CEO de 27/10 (ceo/diario.md)"}
setr('Finbook','vendas-out',dict(texto="0",num=0,**fb))
setr('Finbook','vendas-nov',dict(texto="0",num=0,**fb))
setr('Finbook','visitas-7d',dict(texto="38",num=38,**fb))
vg={"medido_em":"2026-10-27 18:55","fonte":"resumo do CEO de 27/10 (diario.md)"}
setr('Vagas SJDR','receita-mes',dict(texto="R$ 20",num=20,**vg))
setr('Vagas SJDR','vagas-mes',{"texto":"124","num":124,"medido_em":"2026-10-27 18:55","fonte":"resumo do CEO de 27/10 (registro-publicadas.csv)"})
json.dump(r,open(B,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
