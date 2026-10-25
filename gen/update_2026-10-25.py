import json
P='data/projetos.json'
d=json.load(open(P,encoding='utf-8'))
d['gerado_em']='25/10/2026 08:15 (horário de Brasília)'
by={p.get('repo'):p for p in d['projetos']}
a=by['abriuagora']
a['status']=("Em operação ativa: onda 2 ligou em 20/10; a onda 3 segue sem ligar (0 pedidos de amostra vindos de lead). "
 "Em 24 e 25/10 entraram ajustes de conversão: formulário da amostra com campo Ramo e linha de aceite abaixo do botão, e a página /para-contadores enxugada para até 600 palavras visíveis. "
 "As 4 parcerias de 23/10 seguem sem resposta registrada; os assuntos novos da prospecção começam em 26/10. "
 "Portão 1 segue em 0 de 3 amostras; conta no Asaas ainda pendente.")
a['recente']=[
 "25/10 06:05 – /para-contadores com até 600 palavras visíveis",
 "24/10 18:07 – formulário da amostra: campo Ramo e linha de aceite abaixo do botão",
]+a['recente'][:3]
a['atualizado']='25/10/2026 06:05'
f=by['finbook']
f['status']=("finbook.com.br no ar (site 200). Ainda 0 vendas (CCO em 24/10); meta de 1ª venda até 31/10. "
 "Em 24/10 o Short 10 foi aprovado na 3ª revisão e publicado no YouTube e no TikTok, o lote 5 de parceiros foi enviado (10 de 10), a página de obrigado da compra ganhou o botão da área de membros da Kiwify e o checklist em PDF e a página de obrigado da newsletter passaram a levar à calculadora do limite do MEI. "
 "A troca de capas antigas no TikTok travou (o TikTok só permite nos 7 primeiros dias do post).")
f['recente']=[
 "24/10 22:57 – COO: obrigado da newsletter sem formulário repetido, com chamada para a calculadora do limite",
 "24/10 20:53 – COO: checklist em PDF com chamada para a calculadora do limite",
 "24/10 20:30 – CEO: lote 5 de parceiros enviado (10 de 10)",
 "24/10 20:17 – CEO: resumo diário no formato curto (0 venda)",
 "24/10 16:59 – COO: Short 10 público no TikTok; troca de capas antigas travada pelo limite de 7 dias",
 "24/10 15:00 – COO: Short 10 aprovado na 3ª revisão e publicado no YouTube e no TikTok",
]
f['proximos']=[
 "Rodrigo: verificação por telefone do YouTube (T-036 b)",
 "CMO decidir em 27/10 se republica posts para trocar capas no TikTok",
 "Concluir os ajustes de conversão T-038 até 27/10",
 "CLO conferir os termos da Hotmart e abrir a conta (T-057)",
]
f['atualizado']='24/10/2026 22:57'
v=by['vagassjdr']
v['status']=("O n8n voltou e as vagas de 23/10 saíram: 8 publicadas automaticamente e 2 enviadas para aprovação. "
 "Em 24/10 a coleta trouxe 1 vaga nova, enviada para aprovação. Pendente: arquivar 2 fluxos temporários no n8n (aguardando ok escrito). Sem README.")
v['recente']=["24/10 17:36 – 1 vaga nova de 24/10 enviada para aprovação",
 "24/10 15:36 – vagas de 23/10: 8 publicadas automaticamente, 2 aguardando aprovação"]+v['recente'][1:4]
v['proximos']=[x for x in v['proximos'] if not x.startswith('Publicar as vagas de 23/10')]
v['atualizado']='24/10/2026 17:36'
m=by['milhas-e-cartoes']
m['status']=("Em operação: radar de 24/10 sem promoção aplicável (Livelo → Latam Pass 25% e Smiles até 70% encerraram em 23/10; Livelo → Etihad até 40% fora da estratégia). "
 "Novos planos do Clube Livelo entram na revisão de 01/11. Nenhuma campanha Nubank → Azul/Smiles/Latam de 2026 vigente. Saldos na planilha seguem desatualizados.")
m['recente']=["24/10 – radar diário: nada aplicável; novos planos do Clube Livelo vão para a revisão de 01/11"]+m['recente'][:4]
m['atualizado']='24/10/2026 08:35'
ap=by['assistente-pessoal']
ap['status']=("Versionado no GitHub e espelhado de hora em hora. Em 24/10 o modelo de funções C-Level passou a prever o resumo curto do CEO ao Rodrigo (só \"O que precisa de você\" e \"Resultados\"), e o assistente ganhou a regra de abrir sozinho o navegador quando a extensão não estiver conectada.")
ap['recente']=["24/10 18:35 – Funcoes-C-Level: formato curto do resumo do CEO ao Rodrigo",
 "24/10 14:35 – regra: abrir o navegador sozinho quando a extensão não estiver conectada"]+ap['recente'][:3]
ap['atualizado']='24/10/2026 18:35'
json.dump(d,open(P,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
open(P,'a').write('\n')
