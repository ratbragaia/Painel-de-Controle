import json
P='data/projetos.json'
d=json.load(open(P,encoding='utf-8'))
d['gerado_em']='26/10/2026 08:10 (horário de Brasília)'
by={p.get('repo'):p for p in d['projetos']}
a=by['abriuagora']
a['status']=("Em operação ativa: onda 2 ligou em 20/10; a onda 3 segue sem ligar (0 pedidos de amostra vindos de lead). "
 "Seguem os ajustes de conversão do CMO: em 25/10 a home passou a ter um só botão principal de assinar, e em 26/10 a página /obrigado ganhou o mês real, aviso para olhar Promoções/Spam e um só botão. "
 "As 4 parcerias de 23/10 seguem sem resposta registrada; os assuntos novos da prospecção começam em 26/10. "
 "Portão 1 segue em 0 de 3 amostras; conta no Asaas ainda pendente.")
a['recente']=[
 "26/10 06:06 – página /obrigado: mês real, aviso de Promoções/Spam e um só botão",
 "25/10 18:01 – home com um só botão principal de assinar",
]+a['recente'][:3]
a['atualizado']='26/10/2026 06:06'
f=by['finbook']
f['status']=("finbook.com.br no ar (site 200). Ainda 0 vendas (CCO em 25/10); meta de 1ª venda até 31/10. "
 "Em 25/10: 51 visitas e 63 pageviews em 7 dias; o Short 10 no TikTok chegou a 143 views e 5 curtidas; parceria da Qipu só com resposta automática. "
 "A fila do COO ficou sem itens executáveis no domingo (aguardando CLO, CMO em 27/10 e o lote de parceiros). O envio do próximo lote de parceiros passou a ser decisão do CEO.")
f['recente']=[
 "25/10 20:24 – CEO: resumo diário (0 venda; 51 visitas em 7 dias)",
 "25/10 15:50 – CCO: 0 venda, cliente ou parceiro",
 "25/10 10:58 – COO: capa do Short 10 no TikTok conferida (143 views, 5 curtidas)",
 "25/10 09:05 – CISO: varredura de segurança sem achados",
 "24/10 22:57 – COO: obrigado da newsletter sem formulário repetido, com chamada para a calculadora do limite",
]
f['proximos']=[
 "Rodrigo: verificação por telefone do YouTube (T-036 b)",
 "CEO decidir o envio do lote de parceiros (T-008) no ciclo de 26/10",
 "CMO decidir em 27/10 se republica posts para trocar capas no TikTok",
 "CLO conferir os termos da Hotmart e abrir a conta (T-057)",
]
f['atualizado']='25/10/2026 22:55'
v=by['vagassjdr']
v['status']=("O n8n voltou e as vagas de 23/10 saíram: 8 publicadas automaticamente e 2 enviadas para aprovação. "
 "Em 24 e 25/10 a coleta trouxe 1 vaga nova por dia, enviadas para aprovação. Pendente: arquivar 2 fluxos temporários no n8n (aguardando ok escrito). Sem README.")
v['recente']=["25/10 17:35 – 1 vaga nova de 25/10 enviada para aprovação"]+v['recente'][:4]
v['atualizado']='25/10/2026 17:35'
m=by['milhas-e-cartoes']
m['status']=("Em operação: radar de 25/10 sem promoção aplicável (Nomad → Azul vale só para conta nova; Livelo → Etihad fora da estratégia). "
 "Novos planos do Clube Livelo entram na revisão de 01/11. Nenhuma campanha Nubank → Azul/Smiles/Latam de 2026 vigente. Saldos na planilha seguem desatualizados.")
m['recente']=["25/10 – radar diário: nada aplicável (Nomad → Azul só para conta nova)"]+m['recente'][:4]
m['atualizado']='25/10/2026 12:59'
json.dump(d,open(P,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
open(P,'a').write('\n')
