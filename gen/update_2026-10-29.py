import json
P='data/projetos.json'
d=json.load(open(P,encoding='utf-8'))
d['gerado_em']='29/10/2026 08:20 (horário de Brasília)'
by={p.get('repo'):p for p in d['projetos'] if p.get('repo')}
a=by['abriuagora']
a['status']=("Em operação ativa, funil ainda em zero: Portão 1 em 0 de 3 amostras a 2 dias do prazo (31/10). "
 "O envio das 15 amostras diretas (10 empresas da cidade prontas para cada escritório) atrasou um dia e está agendado no servidor para 29/10 09:45, com follow-up em 30/10; a prospecção do dia ficou com teto de 5 para caber no limite de 20 envios. "
 "O CEO congelou até 01/11 tudo que não leve amostra a cliente (SEO, instalação das páginas por cidade). Parceria em 0 de 4 respostas; a linha de indicação espera o OK do CLO hoje. Conta no Asaas ainda pendente.")
a['recente']=[
 "29/10 06:02 – COO: 15 amostras diretas agendadas para hoje 09:45",
 "28/10 15:09 – prospecção com teto de 5 em 29/10 para caber o envio das amostras",
 "28/10 08:45 – CEO: congelamento até 01/11 do que não leva amostra a cliente",
]+a['recente'][:3]
a['proximos']=[
 "Envio das 15 amostras diretas hoje 09:45 e linha diária de métrica",
 "Follow-up das amostras em 30/10",
 "OK do CLO na linha de indicação em 29/10",
 "Portão 1 em 31/10; troca de oferta pronta se falhar",
 "Rodrigo: colar a chave da API no servidor e cadastrar a conta bancária no Asaas",
]
a['atualizado']='29/10/2026 06:02'
f=by['finbook']
f['status']=("finbook.com.br no ar (site 200). Ainda 0 vendas e 0 cliques em comprar (o CTO provou em 28/10 que a medição funciona); a meta de 1ª venda até 31/10 não deve ser batida. "
 "Visitas em 7 dias: 38 (meta da semana 75). Em 28/10 saíram 8 convites a afiliados (1º lote do canal C-004), o lote 5 de parceiros fechou com 0 resposta humana, ficou pronto o importador dos 12 artigos para o blog e foi criado o canal do Telegram t.me/finbookbr. "
 "O Short diário segue travado (2 versões reprovadas pela pronúncia de \"MEI\"), e o WhatsApp do número da empresa passou ao Vagas SJDR.")
f['recente']=[
 "28/10 20:25 – CEO: resumo diário (0 venda, 8 convites a afiliados)",
 "28/10 15:05 – placar do lote 5 de parceiros: 0 resposta humana",
 "28/10 12:55 – 8 convites C-004 enviados; importador dos 12 artigos pronto",
 "28/10 12:05 – canal do Telegram t.me/finbookbr criado",
 "28/10 11:15 – Short s30 reprovado no gate pela pronúncia de \"MEI\"",
 "28/10 09:25 – CTO: 26 URLs 200 e clique em comprar provado na medição",
]
f['proximos']=[
 "CMO+CLO revisarem os artigos a01–a12 até 29/10; COO publica até 30/10",
 "Posts no canal do Telegram a partir de 29/10 (T-081)",
 "Destravar o Short diário (decisão do CMO sobre o \"MEI\" falado)",
 "Follow-up único dos convites a afiliados em 01/11; revisão de oferta em 02/11 se outubro fechar sem venda",
]
f['atualizado']='29/10/2026 01:52'
v=by['vagassjdr']
v['status']=("Publicação em dia; receita de outubro em R$ 20 (cerca de 7% da meta de ~R$ 300) e 0 Pix de 22 a 28/10. Instagram com 413 mil visualizações em 30 dias. "
 "Em 28/10 a IA do Direct foi corrigida contra confirmação falsa de pagamento (28 de 28 e 87 de 87 testes sem falha), 252 rascunhos de oferta ficaram prontos (não enviados) e o WhatsApp do número da empresa foi conectado (instância vagas-sjdr, 0 envios). "
 "O fluxo do WhatsApp passou 20 de 20 no teste simulado e espera ativação; as 20 ofertas e a página \"Vagas de hoje\" dependem da conferência do CLO hoje. A aquisição ainda depende só do Instagram.")
v['recente']=[
 "29/10 04:23 – COO: fluxo do WhatsApp desligado testado (20 de 20 no simulado)",
 "28/10 18:58 – CEO: resumo (R$ 20 no mês, 413 mil visualizações em 30 dias)",
 "28/10 16:55 – IA do Direct corrigida contra pagamento falso e publicada (T-051)",
 "28/10 16:55 – 252 rascunhos de oferta prontos (não enviados)",
 "28/10 – WhatsApp da empresa conectado à instância vagas-sjdr",
]
v['proximos']=[
 "CLO confere as 20 ofertas, a página C-008 e os rascunhos em 29/10",
 "Envio das 20 ofertas e link da página nova na bio depois do CLO",
 "Ativar o fluxo do WhatsApp (credencial, webhook e teste real)",
 "Revisão das ideias de monetização em 30/10; fim do patrocínio Hub em 31/10",
 "Rodrigo: créditos da API até 04/11 (pagamento) e ok para 5 convites de collab",
]
v['atualizado']='29/10/2026 04:34'
p=by['PatentSonar']
p['status']=("Em operação: 77 primeiros contatos até 28/10 e 0 respostas (meta de 150 até 31/10, que não deve ser batida). "
 "Em 28–29/10 o crítico aprovou os follow-ups a compradores e parceiros, mais 4 compradores americanos foram importados (semana 44 com 15 contatos novos; 2 na fila de hoje) e o C11 (portais de imprensa) foi encerrado sem envio. "
 "O Panorama 2025-26 foi aprovado pelo crítico (11 de 12) e ganhou uma página-amostra grátis (ainda sem link). No site: páginas de tecnologia com a cara da home, redirecionamento das páginas sem .html e checagem de disponibilidade a cada hora.")
p['recente']=[
 "29/10 05:41 – 4 compradores importados; 2 contatos aprovados na fila de hoje",
 "29/10 05:10 – página-amostra grátis do Panorama 2025-26 (sem link ainda)",
 "29/10 05:08 – páginas de tecnologia com o visual da home; métrica de 28/10 (77 contatos, 0 respostas)",
 "28/10 13:17 – checagem de disponibilidade por hora e redirecionamento sem .html",
 "28/10 16:16 – Panorama 2025-26 aprovado pelo crítico (11 de 12)",
 "28/10 – CEO: C11 (portais de imprensa) encerrado sem envio",
]
p['proximos']=[
 "Follow-ups a parceiros e compradores a partir de 29–30/10; 5 editores em 30/10",
 "Checkpoint dos 150 contatos em 31/10",
 "Ligar a amostra do Panorama aos contatos",
 "Se em 02/11 houver 0 resposta, corretiva de oferta ou público",
]
p['atualizado']='29/10/2026 05:41'
json.dump(d,open(P,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
open(P,'a').write('\n')

B='gen/resumo_base.json'
r=json.load(open(B,encoding='utf-8'))
def setr(emp,iid,val):
  for e in r['empresas']:
    if e['nome']==emp:
      for i in e['indicadores']:
        if i['id']==iid: i['resultado']=val; return
  print('nao achei',emp,iid)
ps={"medido_em":"2026-10-29 05:08","fonte":"métrica diária do COO (docs/coo/metricas-diarias.md, linha de 28/10)"}
setr('PatentSonar','contatos',dict(texto="77",num=77,**ps))
setr('PatentSonar','resposta',dict(texto="0 de 77 (0 %)",num=0,**ps))
ab={"medido_em":"2026-10-28 08:45","fonte":"resumo do CEO de 28/10 (resumos-clevels)"}
setr('Abriu Agora','amostras',dict(texto="0",num=0,**ab))
setr('Abriu Agora','pagantes',dict(texto="0",num=0,**ab))
fb={"medido_em":"2026-10-28 08:45","fonte":"ciclo da manhã do CEO de 28/10 (ceo/diario.md)"}
setr('Finbook','vendas-out',dict(texto="0",num=0,**fb))
setr('Finbook','vendas-nov',dict(texto="0",num=0,**fb))
setr('Finbook','visitas-7d',dict(texto="38",num=38,**fb))
setr('Vagas SJDR','receita-mes',{"texto":"R$ 20","num":20,"medido_em":"2026-10-28 18:58","fonte":"resumo do CEO de 28/10 (diario.md)"})
json.dump(r,open(B,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
