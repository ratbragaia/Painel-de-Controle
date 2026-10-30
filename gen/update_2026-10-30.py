import json
P='data/projetos.json'
d=json.load(open(P,encoding='utf-8'))
d['gerado_em']='30/10/2026 08:15 (horário de Brasília)'
by={p.get('repo'):p for p in d['projetos'] if p.get('repo')}
a=by['abriuagora']
a['status']=("Em operação ativa: Portão 1 em 1 de 3 a 1 dia do prazo (31/10), com o 1º pedido real de amostra vindo do envio de 27/10 (20 enviados, 19 entregues). "
 "As 15 amostras diretas saíram em 29/10 (12:08–12:15) e foram entregues, ainda sem resposta; follow-up de 48h no sábado 31/10. "
 "Parceria segue em 0 de 4 respostas (mantida sem ampliar, fecha em 06/11 se seguir zero). Política v1.5 publicada e exemplos públicos sem nome de pessoa prontos no código para instalar antes de 01/11. Pagantes 0, receita R$ 0.")
a['recente']=[
 "30/10 06:06 – COO: exemplos públicos sem nome de pessoa prontos (CI verde), instalação pedida",
 "30/10 00:01 – envio de 27/10: 19 entregues e 1 pedido real de amostra; Portão 1 em 1 de 3",
 "29/10 12:15 – 15 amostras diretas enviadas e entregues (0 respostas até agora)",
 "29/10 18:03 – Política v1.5 concluída",
 "29/10 08:40 – CEO: prospecção volta a 20 por dia a partir de 30/10",
]+a['recente'][:2]
a['proximos']=[
 "Follow-up de 48h das 15 amostras em 31/10",
 "Decisão do Portão 1 em 30/10, confirmada em 02/11 com os dados de 31/10",
 "Instalar os exemplos públicos antes de 01/11",
 "Post na Página da empresa no LinkedIn em 01/11",
 "Rodrigo: colar a chave da API no servidor e cadastrar a conta bancária no Asaas",
]
a['atualizado']='30/10/2026 06:06'
f=by['finbook']
f['status']=("finbook.com.br no ar (site 200, sitemap com 38 URLs). Ainda 0 vendas e 0 cliques em comprar; a meta de 1ª venda até 31/10 não deve ser batida e a oferta e o funil serão revistos em 02/11. "
 "Em 29/10 entraram no ar os 12 artigos novos do blog (revisados pelo CLO), a Política de Privacidade v2 e o 1º Short desde 24/10 (s30, YouTube e TikTok, narração sem \"MEI\" falado). "
 "Visitas em 7 dias: 30 (meta da semana 75, não batida). Convites a afiliados do C-004: 0 resposta humana.")
f['recente']=[
 "29/10 12:55 – Short s30 postado no TikTok (em análise)",
 "29/10 11:05 – 12 artigos novos no blog, Privacidade v2 em produção e Short s30 no YouTube",
 "29/10 09:20 – CLO: 12 de 12 artigos aprovados com correção; regras do Telegram e da Kiwify conferidas",
 "29/10 08:45 – CEO: 30 visitas em 7 dias, 0 clique; fim do impasse do \"MEI\" falado",
 "28/10 12:55 – 8 convites a afiliados enviados",
]
f['proximos']=[
 "1º post no canal do Telegram (T-081)",
 "Short diário a partir dos pacotes, com \"microempreendedor\" na narração",
 "Fechar a verificação do app \"fluke\" (CTO, novo prazo 30/10)",
 "Follow-up dos convites a afiliados em 01/11; revisão de oferta e funil em 02/11",
]
f['atualizado']='29/10/2026 22:58'
v=by['vagassjdr']
v['status']=("Publicação em dia; receita de outubro em R$ 20 (cerca de 7% da meta de ~R$ 300). Em 29/10 saíram 10 ofertas de POST pago pelo Direct (2 respostas, 0 Pix; 1 \"Sim\" não reconhecido por um bug já corrigido). "
 "O fluxo do WhatsApp passou no teste real às 21:53 e, desde 30/10 8h, o grupo recebe 1 post por vaga nova (Status e Pix ainda desligados). "
 "O registro de vagas não espelha desde 28/10 por o notebook estar desligado; o plano de levar a rotina das 17h para a VPS está pronto e espera escolha do Rodrigo. A aquisição ainda depende só do Instagram.")
v['recente']=[
 "30/10 08:00 – grupo do WhatsApp passa a 1 post por vaga nova",
 "29/10 22:38 – COO: teste real do WhatsApp ok e plano da rotina das 17h na VPS pronto",
 "29/10 19:05 – CEO: resumo (10 ofertas, 2 respostas, mês R$ 20)",
 "29/10 12:09 – 10 ofertas de POST pago enviadas pelo Direct",
 "29/10 10:41 – trava contra oferta duplicada publicada",
]
v['proximos']=[
 "Responder a empresa que disse \"Sim\" e gerar o Pix",
 "5 convites de collab, ofertas e troca do endereço da Página do Facebook em 30/10",
 "Revisão das ideias de monetização em 30/10; fim do patrocínio Hub em 31/10",
 "Rodrigo: escolher como espelhar o registro de vagas e decidir a 1ª parte da rotina das 17h na VPS",
 "Nota fiscal em toda venda (com o contador, prazo 05/11)",
]
v['atualizado']='30/10/2026 04:35'
p=by['PatentSonar']
p['status']=("Em operação: 77 primeiros contatos até 28/10 e 0 respostas (meta de 150 até 31/10, projeção de 80 a 82). "
 "Em 29/10 o site comprador passou no crítico (12 de 12), saiu a página do trecho grátis do Panorama 2025–26 (ainda sem link), a semana 44 chegou a 15 compradores nomeados com 2 contatos na fila e começaram os follow-ups a parceiros. "
 "Nenhuma resposta de prospect até agora; se seguir em 0 em 02/11, entra a corretiva de oferta ou público.")
p['recente']=[
 "29/10 – CEO: placar de outubro (77 de 150, 0 respostas, US$ 0 de receita recorrente)",
 "29/10 05:41 – +4 compradores nomeados (semana 44 com 15); 2 contatos na fila",
 "29/10 05:10 – página do trecho grátis do Panorama 2025–26 (sem link ainda)",
 "29/10 05:08 – páginas de tecnologia com o visual da home (crítico 12 de 12)",
 "29/10 – follow-ups a parceiros a partir de hoje",
]
p['proximos']=[
 "Follow-ups a 2 parceiros e 5 editores em 30/10",
 "Checkpoint dos 150 contatos em 31/10",
 "Ligar o trecho grátis do Panorama ao formulário da página técnica",
 "Se em 02/11 houver 0 resposta, corretiva de oferta ou público",
]
p['atualizado']='29/10/2026 08:41'
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
ab={"medido_em":"2026-10-30 00:01","fonte":"rodada do COO de 30/10 00:01 (resumos-clevels e registro-ajustes.md)"}
setr('Abriu Agora','amostras',dict(texto="1",num=1,**ab))
setr('Abriu Agora','pagantes',dict(texto="0",num=0,**ab))
fb={"medido_em":"2026-10-29 08:45","fonte":"ciclo da manhã do CEO de 29/10 (ceo/diario.md)"}
setr('Finbook','vendas-out',dict(texto="0",num=0,**fb))
setr('Finbook','vendas-nov',dict(texto="0",num=0,**fb))
setr('Finbook','visitas-7d',dict(texto="30",num=30,**fb))
setr('Vagas SJDR','receita-mes',{"texto":"R$ 20","num":20,"medido_em":"2026-10-29 19:05","fonte":"resumo do CEO de 29/10 (diario.md)"})
json.dump(r,open(B,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
