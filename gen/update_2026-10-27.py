import json
P='data/projetos.json'
d=json.load(open(P,encoding='utf-8'))
d['gerado_em']='27/10/2026 08:15 (horário de Brasília)'
by={p.get('repo'):p for p in d['projetos']}
a=by['abriuagora']
a['status']=("Em operação ativa: onda 2 ligou em 20/10; a onda 3 segue sem ligar (0 pedidos de amostra vindos de lead). "
 "Em 26/10 o servidor foi atualizado (home com um só botão de assinar e /obrigado com o mês real no ar), a Política de Privacidade 1.4 passou a mostrar o encarregado e a Página da Abriu Agora no LinkedIn foi criada. "
 "Em 27/10 ficou pronta a simulação da oferta de troca (plano anual), que segue desligada até 30/10. A linha de indicação espera o OK do CLO em 29/10. "
 "Portão 1 segue em 0 de 3 amostras; conta no Asaas ainda pendente.")
a['recente']=[
 "27/10 06:10 – simulação da oferta de troca pronta (segue desligada até 30/10)",
 "26/10 18:03 – Página da Abriu Agora no LinkedIn criada e preenchida",
 "26/10 16:51 – Política de Privacidade 1.4 com o encarregado publicado",
 "26/10 11:49 – servidor atualizado: home com um botão de assinar e /obrigado novo no ar",
]+a['recente'][:2]
a['atualizado']='27/10/2026 06:10'
f=by['finbook']
f['status']=("finbook.com.br no ar (site 200). Ainda 0 vendas (CCO em 26/10); meta de 1ª venda até 31/10. "
 "No resumo do CEO de 26/10: 38 visitas e 49 pageviews em 7 dias; o Short 10 do perdão chegou a 197 views; Página do Finbook no LinkedIn no ar; Hotmart descartada por exigir exclusividade. "
 "O Kit foi testado no Google Planilhas e a projeção anual do Controle do Limite foi corrigida no gerador (T-068). WhatsApp e Telegram próprios seguem parados até haver um chip que receba SMS.")
f['recente']=[
 "26/10 20:55 – COO: corrige a projeção anual do Controle do Limite (T-068)",
 "26/10 20:25 – CEO: resumo diário (0 venda; 38 visitas em 7 dias)",
 "26/10 19:10 – CEO: Página do Finbook no LinkedIn no ar; Kit testado no Google Planilhas",
 "26/10 18:55 – COO: ferramenta de deploy atualizada, prévia com 25/25 páginas ok",
 "26/10 12:59 – CEO: YouTube verificado; legenda, capa e banners da Kiwify",
]
f['proximos']=[
 "Rodrigo: confirmar se o chip da IA recebe SMS ou aprovar um chip novo (gasto)",
 "CMO/CLO liberarem a página GEO e o post do perdão (T-063, T-065)",
 "T-064 em 28/10; prévias do Kit corrigido junto com a T-040",
]
f['atualizado']='26/10/2026 22:52'
v=by['vagassjdr']
v['status']=("Publicação em dia: 5 vagas em 26/10, 17 desde 23/10 e 124 em outubro. Instagram com 354.737 visualizações em 28 dias e 124 conversas no Direct. "
 "Receita de outubro em R$ 20 (cerca de 7% da meta de ~R$ 300, que não será batida). "
 "Em 26/10 a IA do Direct passou a nunca dizer \"vou confirmar\" e a encaminhar a dúvida; o CEO aprovou começar um canal novo em escada a partir de 02/11, após o CLO. "
 "A aquisição ainda depende só do Instagram.")
v['recente']=[
 "26/10 22:37 – COO: regra da IA do Direct de encaminhar em vez de \"vou confirmar\" testada 3/3",
 "26/10 19:00 – CEO: resumo (124 vagas em outubro, receita R$ 20)",
 "26/10 16:40 – COO: prévia recusada no Telegram conferida (vaga fora da área)",
]+v['recente'][:2]
v['proximos']=[
 "CMO: 1º teste de canal novo em 27/10",
 "CEO/CFO decidirem o preço do Fixado (T-037)",
 "Canal novo em escada a partir de 02/11, após o CLO (T-035)",
 "Rodrigo: créditos da API até 04/11 (pagamento)",
]
v['atualizado']='27/10/2026 04:37'
p=by['PatentSonar']
p['status']=("Em operação: 69 primeiros contatos enviados até agora e 0 respostas humanas (meta de 150 até 31/10; projeção de 74). "
 "Em 27/10 o COO preparou o lote 2 da semana 44 (3 compradores de programas públicos e eventos, mais 1 rascunho refeito), revisado pelo crítico e ainda sem envio, "
 "e fez o acabamento do site (página de obrigado, páginas de tecnologia, 404 e páginas legais). A edição passou a ler a data de prioridade correta de cada patente. "
 "A Eslovênia ficou só com contato autorizado. Um item de segurança travou porque exige versões maiores proibidas pela tarefa.")
p['recente']=[
 "27/10 07:25 – lote 2 da semana 44 revisado pelo crítico (3 liberados, 1 refeito, 1 segurado); sem envio",
 "27/10 07:20 – checkpoint: 69 primeiros contatos, 0 respostas, projeção de 74 de 150",
 "27/10 05:15 – acabamento do site: obrigado, tecnologia, 404 e páginas legais",
 "27/10 04:14 – edição passa a usar a data de prioridade correta de cada patente",
 "26/10 16:14 – aviso no Telegram quando o servidor fica parado 6 horas úteis",
]
p['proximos']=[
 "Liberar o lote 2 da semana 44",
 "Checkpoint dos 150 contatos em 31/10",
 "Resolver o item de segurança travado (exige versões maiores)",
]
p['atualizado']='27/10/2026 07:25'
json.dump(d,open(P,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
open(P,'a').write('\n')

B='gen/resumo_base.json'
r=json.load(open(B,encoding='utf-8'))
for e in r['empresas']:
  if e['nome']=='PatentSonar':
    for i in e['indicadores']:
      if i['id']=='contatos':
        i['resultado']={"texto":"69","num":69,"medido_em":"2026-10-27 06:21","fonte":"pipeline §9 do COO, checkpoint de 27/10"}
      if i['id']=='resposta':
        i['resultado']={"texto":"0 de 69 (0 %)","num":0,"medido_em":"2026-10-27 06:21","fonte":"pipeline §9 do COO, checkpoint de 27/10"}
json.dump(r,open(B,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
