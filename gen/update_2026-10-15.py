import json, html
src='/tmp/projetos.json'
d=json.load(open(src,encoding='utf-8'))
P={p['nome']:p for p in d['projetos']}
GH='https://github.com/ratbragaia/'
d['gerado_em']='15/10/2026 08:20 (horário de Brasília)'

p=P['Abriu Agora']
p['status']='Em operação ativa: pipeline mensal e prospecção por e-mail rodando; a onda 1 terminou com 0 pedidos de amostra em 40 convidados, e a onda 2 vai com o assunto B.'
p['recente']=['15/10 00:05 – marco do plano: 0 pedidos de amostra em 40 convidados, onda 2 segue com o assunto B (regra de decisão ajustada)','14/10 19:26 – CLAUDE.md adicionado']+p['recente'][:3]
p['proximos']=['Disparar a onda 2 com o assunto B e medir pedidos de amostra','Confirmar estabilidade da carga da base após a correção de memória','Seguir o checklist de 15/10 do plano']
p['atualizado']='15/10/2026 00:05'

# PatentSonar: modo público mínimo (gen/publico_minimo.json) — bloco removido em 22/10/2026

p=P['BlueBed']
p['status']='Site no ar em bluebed.com.br; em 14/10 entraram rascunhos de proposta comercial e uma página "em construção". Repositório ainda sem README.'
p['recente']=['14/10 – propostas comerciais em HTML (rascunho e versão com efeitos)','14/10 – página "Em construção" e ajuste no script publicar.py','14/10 19:26 – CLAUDE.md adicionado','12/10 11:26 – site no ar em bluebed.com.br']
p['proximos']=['Fechar a proposta comercial','Criar README com objetivo e estado','Executar o PASSO-A-PASSO da página do Facebook']
p['atualizado']='14/10/2026 21:35'

p=P['Vagas SJDR']
p['status']='Coleta ativa: fila com 61 vagas pendentes de aprovação (02/10 a 14/10); marca do Facebook criada. Sem README.'
p['recente']=['14/10 – 28 vagas novas na fila (12 a 14/10)','14/10 – capa e foto de perfil do Facebook','14/10 – scripts n8n para gravar empresa e ajustar retry do container','14/10 19:27 – CLAUDE.md adicionado','12/10 11:01 – primeiro commit (PLANO, rotinas, scripts e fluxos n8n)']
p['proximos']=['Aprovar ou descartar as 61 vagas pendentes','Publicar a página do Facebook com a marca nova','Ativar o fluxo de post pago/cobrança (status real não está claro)','Criar README']
p['atualizado']='14/10/2026 21:36'

p=P['Editallido']
p['status']='Em construção/teste com dados reais; preparando o e-mail frio com revisores. Sem README.'
p['recente']=['14/10 – prompts dos revisores do e-mail frio','14/10 – ajuste no script de contatos do PNCP','14/10 19:26 – CLAUDE.md adicionado']+p['recente'][:2]
p['atualizado']='14/10/2026 21:35'

p=P['Lígia Daher – site']
p['recente']=['14/10 – documentos do projeto migrados do Drive e CLAUDE.md']+p['recente'][:3]
p['atualizado']='14/10/2026 19:26'

p=P['Carteira de Locação']
p['status']='App funcional com muitos módulos; sem código novo desde 30/09 (em 14/10 só entraram logo e favicon novos).'
p['recente']=['14/10 – logo e favicon laranja adicionados']+p['recente']
p['atualizado']='14/10/2026 17:35'

p=P['InfluNet']
p['recente']=['14/10 – documentos do projeto migrados do Drive e CLAUDE.md']+p['recente'][:3]
p['atualizado']='14/10/2026 19:26'

p=P['Base de Conhecimento']
p['status']='PR #4 (vigia no Telegram, teto de tempo no ytkit e Whisper offline) integrado em 14/10; 7 PRs ainda abertos. README pode estar desatualizado.'
p['recente']=['14/10 17:35 – merge do PR #4: vigia no Telegram, teto de tempo no ytkit e Whisper offline']+p['recente'][:3]
p['proximos']=['Revisar e integrar os 7 PRs abertos','Atualizar o README com o estado real']
p['atualizado']='14/10/2026 17:35'

def novo(nome,repo,objetivo,status,recente,proximos,atualizado):
    return dict(nome=nome,repo=repo,objetivo=objetivo,status=status,recente=recente,proximos=proximos,atualizado=atualizado,url=GH+repo,categoria='GitHub')

P['Assistente Pessoal']=novo('Assistente Pessoal','assistente-pessoal',
 'Assistente pessoal do Rodrigo no Claude: mapa dos negócios e do Drive, roteiro do assistente, funções C-level e plano de memória e skills.',
 'Migrado do Drive para D:\\IA e versionado no GitHub em 14/10; espelhado de hora em hora.',
 ['14/10 – arquivos da pasta .ASSISTENTE migrados do Drive','14/10 17:19 – commit inicial (migração para D:\\IA)'],
 ['Seguir o ROTEIRO-ASSISTENTE-PESSOAL.md','Executar o PLANO-memoria-e-skills.md'],'14/10/2026 22:35')
P['Milhas e Cartões']=novo('Milhas e Cartões','milhas-e-cartoes',
 'Hub pessoal de decisões sobre cartões de crédito, milhas e passagens, com radar diário de promoções e revisão mensal.',
 'Em operação: radar diário atualizou as pendências em 14/10.',
 ['14/10 – radar diário: pendências, histórico de decisões e skills atualizados','14/10 17:20 – commit inicial (migração para D:\\IA)'],
 ['Atualizar os saldos dos programas na planilha (lembrete mensal atrasado)','Revisão mensal em 01/11'],'14/10/2026 21:36')
P['Curso de IA']=novo('Curso de IA','curso-de-ia',
 'Material do curso de IA que o Rodrigo dá (slides). Objetivo ainda não descrito no CLAUDE.md.',
 'Migrado para o GitHub em 14/10 com os slides; sem atividade nova.',
 ['14/10 – slides do curso migrados do Drive','14/10 17:19 – commit inicial (migração para D:\\IA)'],
 ['Preencher objetivo e próximos passos no CLAUDE.md'],'14/10/2026 21:35')
P['Juventude Empreendedora']=novo('Juventude Empreendedora','juventude-empreendedora',
 'Iniciativa de desenvolvimento juvenil com apresentação institucional (V1.6). Objetivo ainda não descrito no CLAUDE.md.',
 'Migrado para o GitHub em 14/10; sem atividade nova.',
 ['14/10 – apresentação institucional e lista de melhorias versionadas','14/10 17:19 – commit inicial (migração para D:\\IA)'],
 ['Preencher objetivo e próximos passos no CLAUDE.md','Aplicar as melhorias listadas na apresentação'],'14/10/2026 21:35')
P['Redes Sociais']=novo('Redes Sociais','redes-sociais',
 'Redes sociais pessoais: recomeçar do zero o fluxo de posts do LinkedIn (ideia no Telegram, imagem, aprovação e publicação).',
 'Fluxo antigo apagado em 30/09; os três fluxos do n8n que ficaram estão desligados. Migrado para o GitHub em 14/10.',
 ['14/10 – arquivos migrados do Drive e CLAUDE.md','14/10 17:20 – commit inicial (migração para D:\\IA)','30/09 – decisão de refazer o fluxo do LinkedIn do zero'],
 ['Mover os arquivos antigos para _lixo-2026-09-30','Montar o novo fluxo passo a passo: ideia no Telegram, imagem, aprovação, publicação'],'14/10/2026 21:36')
P['ytkit']=novo('ytkit','ytkit',
 'Programa local (janela em Python) para catalogar canais do YouTube, transcrever vídeos e consolidar cursos, rodando na própria máquina.',
 'Funcionando como programa próprio desde 30/09; usado pelo vigia da Base de Conhecimento. Migrado para o GitHub em 14/10.',
 ['14/10 – ajustes em config, testes sem janela e prompt de consolidação de materiais','14/10 17:22 – commit inicial (migração para D:\\IA)'],
 ['Resolver a seção de pendências própria do projeto'],'14/10/2026 18:37')

p=P['Finbook']
p['repo']='finbook'; p['url']=GH+'finbook'; p['categoria']='GitHub + Assistente Grok Bot'
p['status']='finbook.com.br no ar (calculadoras DAS/limite, ~12 artigos); 0 vendas até 15/10 de manhã; 5 Shorts no YouTube/TikTok; posts diários na página do Facebook.'
p['recente']=['15/10 06:58 – Short 05 "Pix no CPF" publicado no YouTube e TikTok','15/10 – post 05 (limite do MEI) na página do Facebook','14/10 17:30 – projeto versionado no GitHub privado (sem segredos nem entregáveis pagos)','14/10 – revisão técnica do site + IndexNow']
p['proximos']=['1 Short/dia e posts diários','Pin 4 do Pinterest depende do Rodrigo','Reddit em 17/10','Convites a parceiros em 19/10']
p['atualizado']='15/10/2026 06:58'
p['origem']='Arquivos do assistente Finbook (Grok Bot) e repositório ratbragaia/finbook'

ordem=['Abriu Agora','PatentSonar','Finbook','Vagas SJDR','BlueBed','Base de Conhecimento','Editallido','Milhas e Cartões','Assistente Pessoal','ytkit','Redes Sociais','Curso de IA','Juventude Empreendedora','Lígia Daher – site','Carteira de Locação','InfluNet','Agente de Saúde','Hub Rockfort']
assert set(ordem)==set(P), set(P)^set(ordem)
d['projetos']=[P[n] for n in ordem]
json.dump(d,open('/workspace/painel/site/data/projetos.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)

e=lambda s: html.escape(s)
head=open('/tmp/index.html',encoding='utf-8').read().split('</style>')[0]+'</style>'
ngh=sum(1 for p in d['projetos'] if p['categoria'].startswith('GitHub'))
nfora=sum(1 for p in d['projetos'] if p['categoria'].startswith('Fora'))
sumd=[f"{len(d['projetos'])} projetos",f"{ngh} no GitHub",f"{nfora} fora do GitHub",'1 assistente Grok Bot (Finbook)','Ativos hoje: PatentSonar, Abriu Agora, Finbook','Parados: InfluNet (jul), Agente de Saúde (set)']
out=[head,f"</head><body><header><h1>Painel de Controle</h1><p>Projetos do Rodrigo · gerado em {e(d['gerado_em'])}</p><div class=\"sum\">\n"+''.join(f'<div>{e(s)}</div>' for s in sumd)+'</div></header>\n<main>']
for p in d['projetos']:
    c=f"<article class=\"card\"><h2>{e(p['nome'])}</h2><span class=\"tag\">{e(p['categoria'])}</span>"
    if p.get('url'): c+=f" <a href=\"{e(p['url'])}\">repo</a> <small>(privado)</small>"
    if p.get('objetivo'): c+=f"<p><b>Objetivo:</b> {e(p['objetivo'])}</p>"
    c+=f"<p><b>Status:</b> {e(p['status'])}</p>"
    if p.get('recente'): c+='<p><b>Recente:</b></p><ul>'+''.join(f'<li>{e(x)}</li>' for x in p['recente'])+'</ul>'
    if p.get('proximos'): c+='<p><b>Próximos passos:</b></p><ul>'+''.join(f'<li>{e(x)}</li>' for x in p['proximos'])+'</ul>'
    if p.get('origem'): c+=f"<p class=\"dt\">Origem: {e(p['origem'])}</p>"
    if p.get('atualizado'): c+=f"<p class=\"dt\">Última atualização: {e(p['atualizado'])}</p>"
    out.append(c+'</article>')
out.append('</main><footer>Dados em <a href="data/projetos.json">data/projetos.json</a>. Datas no horário de Brasília.</footer></body></html>\n')
open('/workspace/painel/site/index.html','w',encoding='utf-8').write(''.join(out))
print(ngh,nfora,len(d['projetos']))
