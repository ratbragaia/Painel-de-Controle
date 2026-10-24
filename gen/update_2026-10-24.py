import json
P='data/projetos.json'
d=json.load(open(P,encoding='utf-8'))
d['gerado_em']='24/10/2026 08:10 (horário de Brasília)'
by={p.get('repo'):p for p in d['projetos']}
a=by['abriuagora']
a['status']=("Em operação ativa: onda 2 ligou em 20/10; a onda 3 segue sem ligar (0 pedidos de amostra vindos de lead). "
 "Envios de 22/10 (18 de 20 entregues) e 23/10 (20 de 20) sem cliques nem pedidos de amostra de lead; as 4 parcerias de 23/10 ainda sem resposta. "
 "Em 23/10 as páginas por cidade e a home passaram a mostrar setembro de 2026 (6.123 aberturas nas 19 cidades), e a prospecção ganhou assuntos novos (a partir de 26/10) e convites, D+3 e D+7 mais curtos. "
 "Portão 1 segue em 0 de 3 amostras; conta no Asaas ainda pendente.")
a['recente']=[
 "24/10 00:04 – prospecção: convite A/B, D+3 e D+7 curtos, preço de fundador só no D+7 e rodapé curto",
 "23/10 19:46 – setembro de 2026 nas 19 páginas por cidade e na faixa da home (6.123 aberturas)",
 "23/10 18:04 – envios de 22 e 23/10 registrados no git: 0 clique e 0 pedido de amostra de lead",
 "23/10 18:04 – assuntos novos da prospecção a partir de 26/10",
 "23/10 06:01 – Política de Privacidade v1.3 e ajuste na descrição da home",
]
a['proximos']=[
 "Acompanhar as respostas das 4 parcerias enviadas em 23/10",
 "Medir os assuntos novos da prospecção a partir de 26/10",
 "Resolver a lista do mês 2026-09 atrasada",
 "Rodrigo cadastrar a conta bancária no Asaas; Portão 1: ~170 convites até 30/10",
]
a['atualizado']='24/10/2026 00:04'
f=by['finbook']
f['status']=("finbook.com.br no ar (site 200). Resumo semanal do CEO de 23/10: 0 vendas, 61 pageviews e 52 visitas em 7 dias; meta de 1ª venda até 31/10. "
 "Em 23/10 o vídeo longo do C-001 saiu no YouTube, o banner do canal entrou no ar, os Termos de Uso foram publicados e a página do perdão das dívidas do MEI (LC 238) foi para produção. "
 "O Short 10 teve 6 reprovações seguidas no controle de qualidade e aguarda decisão do CEO; a sequência de e-mails de parceiros (T-058) está pronta só em rascunho, sem envio.")
f['recente']=[
 "23/10 22:55 – COO: sequência T-058 no gerador, só rascunho e teste sem envio",
 "23/10 21:00 – COO: Short 10 reprovado pela 6ª vez no controle de qualidade; decisão do CEO",
 "23/10 20:27 – CEO resumo semanal: 0 vendas, 61 pageviews e 52 visitas em 7 dias",
 "23/10 16:55 – COO: banner do canal do YouTube no ar",
 "23/10 13:05 – COO: Termos de Uso no ar",
 "23/10 11:05 – COO: vídeo longo do C-001 publicado no YouTube; página da LC 238 em produção",
]
f['proximos']=[
 "CEO decidir o destino do Short 10 (T-059)",
 "Rodrigo: ok do lote 5 (T-008), passos da Kiwify (T-034) e verificação do YouTube (T-036 b)",
 "CLO conferir os termos da Hotmart e abrir a conta (T-057)",
 "Abrir o Canal do WhatsApp \"MEI em dia\" com o número da empresa (T-056)",
]
f['atualizado']='23/10/2026 22:55'
v=by['vagassjdr']
v['status']=("Em 23/10 a coleta juntou as vagas do dia com artes, mas nada foi publicado: o servidor do n8n ficou fora do ar das 17:05 às 17:16, e as vagas ficaram prontas numa pasta para publicar quando ele voltar. "
 "Pendente: arquivar 2 fluxos temporários no n8n (aguardando ok escrito). Sem README.")
v['recente']=["23/10 17:36 – vagas de 23/10 prontas, não publicadas (n8n fora do ar)"]+v['recente'][:4]
v['proximos']=["Publicar as vagas de 23/10 quando o n8n voltar e conferir o servidor"]+v['proximos']
v['atualizado']='23/10/2026 17:36'
m=by['milhas-e-cartoes']
m['status']=("Em operação: radar de 23/10 sem promoção aplicável (Livelo → Latam Pass 25% e Smiles até 70% abaixo do gatilho de 80%). "
 "Nenhuma campanha Nubank → Azul/Smiles de 2026 confirmada. Saldos na planilha seguem desatualizados.")
m['recente']=["23/10 – radar diário: nada aplicável; Livelo → Latam Pass 25% e pontos+dinheiro acima do teto"]+m['recente'][:4]
m['proximos']=[
 "Vigiar Nubank Ultravioleta → Azul/Smiles/Latam com 50% ou mais",
 "Atualizar os saldos dos programas na planilha (lembrete mensal atrasado)",
 "Revisão mensal em 01/11 (inclui o crédito dos 2.000 pontos extras da Livelo)",
]
m['atualizado']='23/10/2026 11:10'
json.dump(d,open(P,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
open(P,'a').write('\n')
