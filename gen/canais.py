"""Canais de venda e aquisição — coleta para o Painel de Controle.

Chamado por build_detalhes.py. Para cada projeto monta a lista de canais a partir de,
em ordem de força (quem vem depois sobrepõe quem vem antes):
  1. gen/canais_base.json            registro de reserva mantido no painel (números com data e fonte);
  2. data/canais.json anterior       o que já estava publicado (rede de segurança: "mantido");
  3. extração automática             números que o gerador lê todo dia nos arquivos de cada projeto;
  4. registro do CMO (CANAIS.md / canais.md / canais-aquisicao.md, no repositório ou na pasta local);
  5. canais.json do projeto          formato padrão (ver gen/COMO-ATUALIZAR.md).
Para cada número vale o valor com a data de medição mais recente; empate → a fonte mais forte.
Nada é estimado: sem valor = "sem dado" no site. Tudo passa por limpar() (site público).
"""
import csv, datetime as dt, io, json, os, re, unicodedata

METRICAS = ('alcance', 'cliques', 'leads', 'vendas', 'receita')
FORCA = {'anterior': 0, 'registro do painel': 1, 'extraído': 2, 'registro do CMO': 3, 'canais.json do projeto': 4}
FRESCO = {'extraído', 'registro do CMO', 'canais.json do projeto'}
STATUS = ('ativo', 'em teste', 'planejado', 'parado', 'encerrado')

LOCAIS_PADRAO = {
    'abriuagora': [os.environ.get('ABRIU_LOCAL') or '/workspace/abriuagora'],
    'PatentSonar': [os.environ.get('PATENT_LOCAL') or '/workspace/patentsonar/clevels'],
    'finbook': [os.environ.get('FINBOOK_LOCAL') or '/workspace/kit-mei-em-dia'],
}

# ------------------------------------------------------------------ util
def norm(s):
    s = unicodedata.normalize('NFD', (s or '').lower())
    return re.sub(r'[^a-z0-9]+', ' ', ''.join(c for c in s if unicodedata.category(c) != 'Mn')).strip()

def slug(s):
    return norm(s).replace(' ', '-')[:60] or 'canal'

def iso(d, ano=None):
    """'21/10/2026', '21/10', '2026-10-21' → '2026-10-21' (ou None)."""
    if not d: return None
    d = str(d).strip()
    m = re.search(r'(\d{4})-(\d{2})-(\d{2})', d)
    if m: return m.group(0)
    m = re.search(r'\b(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\b', d)
    if m:
        a = m.group(3) or str(ano or dt.date.today().year)
        if len(a) == 2: a = '20' + a
        try: return dt.date(int(a), int(m.group(2)), int(m.group(1))).isoformat()
        except ValueError: return None
    return None

def br(isod):
    try: return dt.date.fromisoformat(isod).strftime('%d/%m/%Y')
    except Exception: return isod or ''

def sem_nomes(s):
    """Tira parênteses sem números (em geral nomes de pessoas/contatos) e negrito."""
    s = re.sub(r'\s*\((?![^)]*\d)[^)]*\)', '', s or '')
    return s

def status_de(texto):
    """Normaliza um texto livre de status → (status, motivo)."""
    t = re.sub(r'\*\*|__|`', '', texto or '').strip()
    if not t or t in ('—', '-'): return None, ''
    low = t.lower()
    regras = [('encerrado', r'encerrad|fechad|vetad|descartad|banid'),
              ('planejado', r'planejad|pronto para|candidat|proposta|a definir'),
              ('em teste', r'em teste|\btestando\b'),
              ('parado', r'parad|pausad|adiad|travad|aguard|passiv|bloquead|suspens'),
              ('ativo', r'\bativ[oa]s?\b|\bno ar\b|ligad')]
    melhor = None
    for st, rx in regras:
        m = re.search(rx, low)
        if m and (melhor is None or m.start() < melhor[1]): melhor = (st, m.start(), m.end())
    if not melhor: return None, ''
    palavra = re.match(r'[\w ]*?(?=[\s:;,.—–→(-]|$)', low[melhor[1]:]).group(0) if melhor[0] != 'em teste' else 'em teste'
    if melhor[1] == 0 and norm(palavra) in ('ativo', 'ativa', 'em teste', 'planejado', 'parado', 'pausado', 'encerrado', 'no ar', 'ligado'):
        resto = t[len(palavra):]          # tira só a palavra de status do começo
    else:
        resto = t                         # "ADIADO pelo Rodrigo…", "Candidato da semana…": o texto inteiro é o motivo
    resto = re.sub(r'^\s*\((.*)\)\s*$', r'\1', resto.strip(' :;,.—–-→'))
    return melhor[0], resto.strip(' :;,.—–-→')

def tipo_de(t):
    t = norm(t)
    if 'vend' in t: return 'venda'
    if 'aquis' in t or t: return 'aquisição'
    return 'aquisição'

def metrica(v, nota='', data=None, origem='registro do painel'):
    if isinstance(v, dict):
        nota = v.get('nota') or nota; data = iso(v.get('medido_em')) or data; v = v.get('valor')
    if v is None or (isinstance(v, str) and (not v.strip() or norm(v) in ('sem dado', 'n d', 'nd'))):
        return {'valor': None, 'nota': nota, 'medido_em': data, 'origem': origem}
    return {'valor': str(v), 'nota': nota, 'medido_em': data, 'origem': origem}

# ------------------------------------------------------------------ leitura dos formatos
def de_padrao(e, origem, data_arquivo, limpar):
    """Entrada no formato padrão (canais.json / canais_base.json) → canal interno."""
    data = iso(e.get('medido_em')) or data_arquivo
    st, mot = status_de(e.get('status'))
    nums = e.get('numeros') or {}
    out = {
        'id': e.get('id') or slug(e.get('canal')), 'canal': limpar(e.get('canal'), 110),
        'grupo': limpar(e.get('grupo') or e.get('canal'), 80), 'tipo': tipo_de(e.get('tipo')),
        'status': st or 'ativo', 'motivo': limpar(e.get('motivo') or mot, 160),
        'inicio': iso(e.get('inicio')), 'hipotese': limpar(e.get('hipotese'), 220),
        'metrica': limpar(e.get('metrica'), 140), 'decisao': limpar(e.get('decisao'), 200),
        'periodo': limpar(e.get('periodo'), 80), 'fonte': limpar(e.get('fonte'), 140),
        'palavras': [norm(p) for p in e.get('palavras') or []],
        'numeros': {k: metrica(nums.get(k), data=data, origem=origem) for k in METRICAS},
        'outros': [],
        'origem': origem, 'medido_em': data,
    }
    for k, m in out['numeros'].items():
        m['nota'] = limpar(m['nota'], 90)
    outros = nums.get('outros') or {}
    if isinstance(outros, dict): outros = [{'rotulo': k, 'valor': v} for k, v in outros.items()]
    for o in outros:
        m = metrica(o.get('valor'), data=iso(o.get('medido_em')) or data, origem=origem)
        m['rotulo'] = limpar(o.get('rotulo'), 60); m['valor'] = limpar(m['valor'], 90) if m['valor'] else None
        out['outros'].append(m)
    return out

COLS = {
    'canal': ('canal de venda', 'canal'), 'tipo': ('tipo',), 'status': ('status', 'estado', 'situacao'),
    'veredito': ('veredito', 'decisao'), 'inicio': ('inicio', 'desde'), 'hipotese': ('hipotese',),
    'metrica': ('metrica',), 'resultado': ('resultado', 'numeros'), 'prazo': ('prazo', 'fim'), 'id': ('id',),
}
def tabelas_md(texto):
    blocos, atual = [], []
    for l in texto.splitlines() + ['']:
        if l.strip().startswith('|'): atual.append(l)
        else:
            if len(atual) >= 3: blocos.append(atual)
            atual = []
    for b in blocos:
        cel = lambda l: [c.strip().replace('\\|', '/') for c in re.split(r'(?<!\\)\|', l.strip().strip('|'))]
        cab = [norm(c) for c in cel(b[0])]
        linhas = [cel(l) for l in b[2:]]
        yield cab, linhas

def de_markdown(texto, origem, data_arquivo, limpar, hoje):
    """Tabelas de um CANAIS.md / canais.md do CMO → canais internos (só tabelas com Canal + Status/Estado/Situação/Veredito/Resultado)."""
    out, vistos = [], set()
    for cab, linhas in tabelas_md(texto):
        idx = {}
        for chave, nomes in COLS.items():
            for i, c in enumerate(cab):
                if chave not in idx and any(c == n or c.startswith(n + ' ') for n in nomes):
                    idx[chave] = i
        if 'canal' not in idx: continue
        if not any(k in idx for k in ('status', 'veredito', 'resultado')): continue
        for l in linhas:
            g = lambda k: l[idx[k]] if k in idx and idx[k] < len(l) else ''
            bruto = g('canal')
            if not bruto or bruto in ('—', '-') or norm(bruto).startswith('a definir'): continue
            nome = re.sub(r'\*\*', '', bruto)
            m = re.search(r'\b(C-?\d{1,3})\b', ' '.join([g('id'), bruto]))
            codigo = m.group(1).replace('-', '').upper() if m else None
            chave = codigo or norm(nome)[:40]
            if chave in vistos: continue
            vistos.add(chave)
            texto_status = next((x for x in (g('status'), g('veredito'), g('resultado')) if x and x not in ('—', '-') and status_de(x)[0]), '')
            st, mot = status_de(texto_status)
            ini = iso(g('inicio'), int(hoje[:4]))
            if not st:
                st = 'planejado' if (not ini or ini > hoje) else 'em teste'
            nome_curto = limpar(sem_nomes(nome), 110)
            if codigo and not nome_curto.upper().startswith(codigo):
                nome_curto = f'{codigo} · {nome_curto}'
            out.append({
                'id': slug(codigo or nome), 'canal': nome_curto, 'grupo': nome_curto, 'tipo': tipo_de(g('tipo') or ('venda' if 'venda' in norm(bruto) else '')),
                'status': st, 'motivo': limpar(sem_nomes(mot), 120), 'inicio': ini,
                'hipotese': limpar(sem_nomes(g('hipotese')), 220), 'metrica': limpar(sem_nomes(g('metrica')), 140),
                'decisao': limpar(sem_nomes(g('veredito')), 160) if g('veredito') not in ('', '—', '-') else '',
                'prazo': iso(g('prazo'), int(hoje[:4])),
                'resultado': limpar(sem_nomes(g('resultado')), 220) if g('resultado') not in ('', '—', '-') else '',
                'periodo': '', 'fonte': '', 'palavras': [],
                'numeros': {k: metrica(None, data=data_arquivo, origem=origem) for k in METRICAS},
                'outros': [], 'origem': origem, 'medido_em': data_arquivo, '_bruto': norm(nome),
            })
    return out

# ------------------------------------------------------------------ extração automática (números do dia)
def _ultimo(pasta, rx):
    try: arqs = sorted((f for f in os.listdir(pasta) if re.match(rx, f)), reverse=True)
    except OSError: return []
    return [os.path.join(pasta, f) for f in arqs]

def _ler(p):
    try: return open(p, encoding='utf-8').read()
    except Exception: return None

def _n(rx, t, g=1, flags=re.I):
    m = re.search(rx, t or '', flags)
    return m.group(g) if m else None

def x_abriuagora(ler_repo, caminhos, locais, hoje):
    upd = []
    pasta = os.path.join(locais[0], 'resumos-clevels') if locais else None
    for p in (_ultimo(pasta, r'\d{4}-\d{2}-\d{2}-ceo\.md$') if pasta else [])[:1]:
        t = _ler(p) or ''; d = os.path.basename(p)[:10]; fonte = 'resumos-clevels/' + os.path.basename(p) + ' (CEO)'
        conv = re.search(r'Convites \(só o 1º e-mail\):\s*(\d+)\s*÷\s*(\d+)', t)
        ent = _n(r'(\d+) e-mails entregues', t); cli = _n(r'Cliques e visitas de prospecção:\s*(\d+)', t)
        amo = _n(r'Amostras \(Portão 1\):\s*(\d+)', t)
        pag = re.search(r'Pagantes\s*(\d+),\s*receita\s*(R\$\s*[\d.,]*\d)', t)
        nums = {}
        if ent: nums['alcance'] = (ent, 'e-mails entregues')
        if cli: nums['cliques'] = (cli, 'cliques e visitas de prospecção')
        if amo: nums['leads'] = (amo, 'pedidos de amostra (meta 3)')
        if pag: nums['vendas'] = (pag.group(1), 'pagantes')
        outros = {'Convites (1º e-mail)': f'{conv.group(1)} de {conv.group(2)} esperados'} if conv else {}
        if nums or outros:
            upd.append({'id': 'email-acumulado', 'numeros': nums, 'outros': outros, 'medido_em': d, 'fonte': fonte, 'periodo': f'13/10 a {br(d)}'})
        if pag:
            upd.append({'id': 'asaas', 'numeros': {'vendas': (pag.group(1), 'pagantes'), 'receita': (pag.group(2), 'receita recebida')}, 'medido_em': d, 'fonte': fonte})
    return upd

def x_patentsonar(ler_repo, caminhos, locais, hoje):
    upd = []
    base = locais[0] if locais else None
    # revisão diária do crítico de e-mail (repositório)
    revs = sorted((p for p in caminhos if re.match(r'docs/reviews/email/\d{4}-\d{2}-\d{2}\.md$', p)), reverse=True)
    for p in revs[:1]:
        t = ler_repo(p) or ''; d = p[-13:-3]
        m = re.search(r'(\d+) human replies of (\d+) cold', t)
        if m:
            upd.append({'id': 'email-frio', 'numeros': {'alcance': (m.group(2), '1º contatos enviados (meta 150 em 31/10)'), 'leads': (m.group(1), 'respostas humanas')},
                        'medido_em': d, 'fonte': p, 'periodo': f'01/10 a {br(d)}'})
    if base:
        t = _ler(os.path.join(base, 'meta-mensal.md')) or ''
        d = iso(_n(r'Realizado (\d{1,2}/\d{1,2})', t), int(hoje[:4]))
        if t and d:
            nums, outros = {}, {}
            v = _n(r'E-mails de 1º contato[^|]*\|[^|]*\|\s*(\d+)\s*cold', t)
            if v: nums['alcance'] = (v, '1º contatos enviados (meta 150 em 31/10)')
            v = _n(r'(\d+) respostas humanas\s*/\s*\d+\s*cold', t)
            if v: nums['leads'] = (v, 'respostas humanas')
            v = _n(r'mail-tester (\d+(?:,\d+)?)/10', t)
            if v: outros['Entregabilidade (mail-tester)'] = v + '/10'
            if nums or outros:
                upd.append({'id': 'email-frio', 'numeros': nums, 'outros': outros, 'medido_em': d, 'fonte': 'meta-mensal.md (CEO)', 'periodo': f'01/10 a {br(d)}'})
            m = re.search(r'Clientes pagantes / MRR \|[^|]*\|\s*(\d+)\s*/\s*(US\$\s*[\d.,]+)', t)
            if m:
                upd.append({'id': 'assinatura', 'numeros': {'vendas': (m.group(1), 'clientes pagantes'), 'receita': (m.group(2).strip(), 'MRR')}, 'medido_em': d, 'fonte': 'meta-mensal.md (CEO)'})
        for p in _ultimo(os.path.join(base, 'resumos'), r'cmo-\d{4}-\d{2}-\d{2}.*\.md$'):
            t = _ler(p) or ''
            m = re.search(r'Search Console 28 dias:\s*([\d.]+) impressões,\s*(\d+) clique', t)
            if m:
                d = re.search(r'\d{4}-\d{2}-\d{2}', os.path.basename(p)).group(0)
                nums = {'alcance': (m.group(1), 'impressões no Google (28 dias)'), 'cliques': (m.group(2), 'clique(s) da busca (28 dias)')}
                a = re.search(r'(\d+) pedidos de amostra desde (\d{1,2}/\d{1,2})', t)
                if a: nums['leads'] = (a.group(1), f'pedidos de amostra desde {a.group(2)}')
                upd.append({'id': 'busca-organica', 'numeros': nums, 'medido_em': d, 'fonte': 'clevels/resumos/' + os.path.basename(p) + ' (CMO)', 'periodo': f'28 dias até {br(d)}'})
                break
    return upd

def x_finbook(ler_repo, caminhos, locais, hoje):
    upd, ano = [], int(hoje[:4])
    t = ler_repo('ceo/diario.md') if 'ceo/diario.md' in caminhos else None
    if t:
        i = t.rfind('### Placar')
        if i >= 0:
            cab = list(re.finditer(r'^## CEO:[^\n]*?(\d{1,2}/\d{1,2})', t[:i], re.M))
            d = iso(cab[-1].group(1), ano) if cab else None
            bloco = t[i:i + 6000]
            fim = re.search(r'\n### (?!Placar)', bloco[5:])
            if fim: bloco = bloco[:fim.start() + 5]
            if d:
                f = 'ceo/diario.md (placar do CEO)'
                pv = re.search(r'(\d+) pageviews\s*/\s*(\d+) visitas em 7d', bloco)
                ori = re.search(r'Origem:\s*(\d+) diretas,\s*(\d+) Facebook,\s*(\d+) buscador', bloco)
                ins = _n(r'\*\*Inscritos:\*\*\s*\**(\d+)', bloco)
                cc = _n(r'(\d+) `clique_comprar`', bloco)
                calc = sum(int(x) for x in re.findall(r'`calc_\w+_uso` \d{1,2}/\d{1,2} = (\d+)', bloco))
                nums, outros = {}, {}
                if pv: nums['alcance'] = (pv.group(1), f'pageviews em 7 dias ({pv.group(2)} visitas)')
                if cc: nums['cliques'] = (cc, 'cliques em comprar')
                if ins: nums['leads'] = (ins, 'inscrito(s) na newsletter')
                if ori: outros['Origem das visitas (7 dias)'] = f'{ori.group(1)} diretas, {ori.group(2)} Facebook, {ori.group(3)} buscador'
                if calc: outros['Usos de calculadora'] = str(calc)
                if nums or outros: upd.append({'id': 'site', 'numeros': nums, 'outros': outros, 'medido_em': d, 'fonte': f, 'periodo': f'7 dias até {br(d)}'})
                yt = re.search(r'canal (\d+) inscritos?;\s*(\d+) Shorts públicos = (\d+) views(?:,\s*(\d+) comentários)?', bloco)
                utm_yt = re.search(r'visita_utm_youtube` (\d{1,2}/\d{1,2}) = (\d+)', bloco)
                if yt or utm_yt:
                    nums, outros = {}, {}
                    if yt:
                        nums['alcance'] = (yt.group(3), f'views em {yt.group(2)} Shorts públicos'); outros['Inscritos no canal'] = yt.group(1)
                        if yt.group(4) is not None: outros['Comentários'] = yt.group(4)
                    if utm_yt: nums['cliques'] = (utm_yt.group(2), f'visitas com UTM do YouTube ({utm_yt.group(1)})')
                    upd.append({'id': 'youtube', 'numeros': nums, 'outros': outros, 'medido_em': d, 'fonte': f, 'periodo': f'acumulado até {br(d)}'})
                utm_fb = re.search(r'visita_utm_facebook` (\d{1,2}/\d{1,2}) = (\d+)', bloco)
                if utm_fb: upd.append({'id': 'facebook', 'numeros': {'cliques': (utm_fb.group(2), f'visitas com UTM do Facebook ({utm_fb.group(1)})')}, 'medido_em': d, 'fonte': f, 'periodo': utm_fb.group(1) + f'/{ano}'})
                si = _n(r'`site:finbook\.com\.br` = (\d+)', bloco)
                if si or ori:
                    nums = {}
                    if si: nums['alcance'] = (si, 'páginas no índice do Google (site:)')
                    if ori: nums['cliques'] = (ori.group(3), 'visitas de buscador em 7 dias')
                    upd.append({'id': 'busca-google-bing', 'numeros': nums, 'medido_em': d, 'fonte': f, 'periodo': br(d)})
                vd = _n(r'\*\*Vendas:\*\*\s*(\d+)', bloco)
                if vd or cc:
                    nums = {}
                    if vd: nums['vendas'] = (vd, 'vendas')
                    if cc: nums['cliques'] = (cc, 'cliques em comprar')
                    upd.append({'id': 'kiwify', 'numeros': nums, 'medido_em': d, 'fonte': f, 'periodo': f'acumulado até {br(d)}'})
        tk = list(re.finditer(r'^.*TikTok \(só o short ?(\d+) tem views, (\d+); os outros (\d+) com 0.*$', t, re.M))
        if tk:
            l = tk[-1]; d = iso(_n(r'\((\d{1,2}/\d{1,2})\)', l.group(0)), ano)
            if d: upd.append({'id': 'tiktok', 'numeros': {'alcance': (l.group(2), f'views (só o Short {l.group(1)}; os outros {l.group(3)} com 0)')}, 'medido_em': d, 'fonte': 'ceo/diario.md (COO)', 'periodo': f'até {br(d)}'})
    if 'ceo/financeiro.csv' in caminhos:
        linhas = list(csv.DictReader(io.StringIO(ler_repo('ceo/financeiro.csv') or '')))
        datas = [l['date'] for l in linhas if l.get('date')]
        if datas:
            s = 0.0
            for l in linhas:
                try:
                    if l.get('type') != 'custo': s += float(l.get('gross') or 0)
                except ValueError: pass
            upd.append({'id': 'kiwify', 'numeros': {'receita': ('R$ ' + f'{s:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'), 'receita bruta registrada')},
                        'medido_em': max(datas)[:10], 'fonte': 'ceo/financeiro.csv'})
    if 'ceo/envios/convite_parceiros.jsonl' in caminhos:
        n = 0
        for l in (ler_repo('ceo/envios/convite_parceiros.jsonl') or '').splitlines():
            try: n += str(json.loads(l).get('status')) in ('200', '201', '202', 'enviado')
            except Exception: pass
        if n: upd.append({'id': 'parceiros', 'numeros': {'alcance': (str(n), 'convites enviados')}, 'medido_em': hoje, 'fonte': 'ceo/envios/convite_parceiros.jsonl (contagem)'})
    return upd

def x_vagassjdr(ler_repo, caminhos, locais, hoje):
    upd = []
    if 'registro-publicadas.csv' in caminhos:
        linhas = list(csv.DictReader(io.StringIO(ler_repo('registro-publicadas.csv') or '')))
        datas = sorted(l['data'] for l in linhas if l.get('data'))
        if linhas: upd.append({'id': 'instagram', 'numeros': {'leads': (str(len(linhas)), f'vagas publicadas desde {br(datas[0]) if datas else "?"}')}, 'medido_em': hoje, 'fonte': 'registro-publicadas.csv (contagem)'})
    if 'PLANO-VagasSJDR.md' in caminhos:
        t = ler_repo('PLANO-VagasSJDR.md') or ''
        m = re.search(r'Atualização (\d{1,2}/\d{1,2}/\d{4}):\s*([\d.]+) visualizações em 30 dias \(([\d.]+) visualizadores', t)
        if m:
            d = iso(m.group(1))
            upd.append({'id': 'instagram', 'numeros': {'alcance': (m.group(2), f'visualizações em 30 dias ({m.group(3)} contas)')}, 'medido_em': d,
                        'fonte': 'PLANO-VagasSJDR.md', 'periodo': f'30 dias até {br(d)}'})
    return upd

EXTRATORES = {'abriuagora': x_abriuagora, 'PatentSonar': x_patentsonar, 'finbook': x_finbook, 'vagassjdr': x_vagassjdr}

# ------------------------------------------------------------------ registro do projeto (canais.json / CANAIS.md)
NOMES_JSON = ('canais.json',)
NOMES_MD = ('canais.md', 'canais-aquisicao.md')
def achar_registros(caminhos, locais):
    """Devolve [(tipo, onde, caminho)] em ordem crescente de força: md repo, md local, json repo, json local."""
    rep_md = sorted((p for p in caminhos if os.path.basename(p).lower() in NOMES_MD), key=lambda p: (p.count('/'), p))
    rep_js = sorted((p for p in caminhos if os.path.basename(p).lower() in NOMES_JSON), key=lambda p: (p.count('/'), p))
    loc_md, loc_js = [], []
    for base in locais or []:
        if not os.path.isdir(base): continue
        for raiz, dirs, arqs in os.walk(base):
            dirs[:] = [x for x in dirs if not x.startswith('.') and x not in ('node_modules', 'tmp', 'site', 'backups')]
            if raiz[len(base):].count(os.sep) >= 2: dirs[:] = []
            for a in arqs:
                p = os.path.join(raiz, a)
                if a.lower() in NOMES_MD: loc_md.append(p)
                elif a.lower() in NOMES_JSON: loc_js.append(p)
    loc_md.sort(key=lambda p: (p.count(os.sep), p)); loc_js.sort(key=lambda p: (p.count(os.sep), p))
    out = [('md', 'local', loc_md[0])] if loc_md else [('md', 'repo', p) for p in rep_md[:1]]
    out += [('json', 'local', loc_js[0])] if loc_js else [('json', 'repo', p) for p in rep_js[:1]]
    return out

# ------------------------------------------------------------------ mescla
def _vence(novo, velho):
    """True se a métrica nova deve substituir a velha (data mais recente; empate → fonte mais forte)."""
    if novo.get('valor') is None: return velho.get('valor') is None and FORCA.get(novo['origem'], 0) >= FORCA.get(velho['origem'], 0)
    if velho.get('valor') is None: return True
    dn, dv = novo.get('medido_em') or '', velho.get('medido_em') or ''
    if dn != dv: return dn > dv
    return FORCA.get(novo['origem'], 0) >= FORCA.get(velho['origem'], 0)

TEXTO = ('canal', 'grupo', 'tipo', 'status', 'motivo', 'inicio', 'hipotese', 'metrica', 'decisao', 'periodo', 'fonte', 'prazo', 'resultado')
def sobrepor(base, novo, forca_texto=True):
    """Aplica 'novo' sobre 'base' (mesmo canal)."""
    for k in TEXTO:
        v = novo.get(k)
        if v and (forca_texto or not base.get(k)):
            if k in ('canal', 'grupo') and base.get(k) and novo.get('origem') == 'registro do CMO': continue  # mantém o nome do registro
            base[k] = v
    for k in METRICAS:
        n = novo['numeros'].get(k)
        if n and _vence(n, base['numeros'].get(k) or {'valor': None, 'origem': 'anterior'}): base['numeros'][k] = n
    idx = {norm(o['rotulo']): i for i, o in enumerate(base['outros'])}
    for o in novo.get('outros') or []:
        i = idx.get(norm(o['rotulo']))
        if i is None: base['outros'].append(o); idx[norm(o['rotulo'])] = len(base['outros']) - 1
        elif _vence(o, base['outros'][i]): base['outros'][i] = o
    return base

def montar(repo, nome, slug_proj, caminhos, ler_repo, limpar, anterior, hoje, base_json, locais=None):
    """Monta o bloco de canais de um projeto. Devolve (empresa|None, log)."""
    log = []
    locais = locais if locais is not None else LOCAIS_PADRAO.get(repo, [])
    canais, ordem = {}, []
    def por(cid): return canais.get(cid)
    def add(c):
        if c['id'] not in canais: ordem.append(c['id']); canais[c['id']] = c
        else: sobrepor(canais[c['id']], c)
    # 1. registro do painel
    cat = base_json.get(repo) or {}
    for e in cat.get('canais') or []:
        add(de_padrao(e, 'registro do painel', iso(cat.get('atualizado_em')), limpar))
    # 2. anterior (só números/canais que sumiram; não mexe em status do registro atual)
    ant = {c.get('id'): c for c in (anterior or {}).get('canais') or []}
    for cid, c in ant.items():
        velho = json.loads(json.dumps(c))
        for k in METRICAS:
            m = velho.get('numeros', {}).get(k) or {}
            if m.get('origem') != 'anterior': m['origem'] = 'anterior'
            m['medido_em'] = iso(m.get('medido_em'))
            velho.setdefault('numeros', {})[k] = m if m else {'valor': None, 'origem': 'anterior'}
        for o in velho.get('outros') or []:
            o['origem'] = 'anterior'; o['medido_em'] = iso(o.get('medido_em'))
        velho.pop('canal_mantido', None)
        velho['inicio'] = iso(velho.get('inicio')); velho['prazo'] = iso(velho.get('prazo')); velho['origem'] = 'anterior'
        velho.setdefault('outros', []); velho.setdefault('palavras', [])
        if cid in canais:
            atual = canais[cid]
            if velho.get('registros'):   # status/textos vieram do registro do projeto: valem mais que o registro do painel
                for k in ('status', 'motivo', 'hipotese', 'metrica', 'decisao', 'inicio', 'prazo'):
                    if k in velho: atual[k] = velho[k]
                atual['registros'] = [r if r.endswith('(anterior)') else r + ' (anterior)' for r in velho['registros']]
            for k in METRICAS:
                if _vence(velho['numeros'][k], atual['numeros'][k]) and velho['numeros'][k].get('valor') is not None:
                    atual['numeros'][k] = velho['numeros'][k]
            sobrepor(atual, {'numeros': {}, 'outros': [o for o in velho['outros'] if norm(o.get('rotulo')) not in {norm(x['rotulo']) for x in atual['outros']}]}, forca_texto=False)
        else:
            velho['status'] = velho.get('status') or 'ativo'
            velho['_so_anterior'] = True
            canais[cid] = velho; ordem.append(cid)
    # 3. extração automática
    fx = EXTRATORES.get(repo)
    if fx:
        try:
            for u in fx(ler_repo, caminhos, locais, hoje):
                c = por(u['id'])
                if not c: continue
                d = iso(u.get('medido_em')) or hoje
                novo = {'numeros': {k: {'valor': str(v[0]), 'nota': limpar(v[1], 90), 'medido_em': d, 'origem': 'extraído'} for k, v in (u.get('numeros') or {}).items()},
                        'outros': [{'rotulo': limpar(k, 60), 'valor': limpar(str(v), 90), 'medido_em': d, 'origem': 'extraído'} for k, v in (u.get('outros') or {}).items()]}
                antes = json.dumps(c['numeros'], sort_keys=True)
                sobrepor(c, novo, forca_texto=False)
                if json.dumps(c['numeros'], sort_keys=True) != antes or novo['outros']:
                    if u.get('fonte'): c['fonte'] = limpar(u['fonte'], 140)
                    if u.get('periodo'): c['periodo'] = limpar(u['periodo'], 80)
        except Exception as ex:
            log.append(f'extração automática falhou ({ex}); valores anteriores mantidos')
    # 4/5. registros do projeto
    registros = []
    for tipo, onde, p in achar_registros(caminhos, locais):
        texto = ler_repo(p) if onde == 'repo' else _ler(p)
        if not texto: continue
        if onde == 'local':
            data_arq = dt.datetime.fromtimestamp(os.path.getmtime(p)).date().isoformat()
            rotulo = os.path.relpath(p, locais[0]) if locais else os.path.basename(p)
        else:
            data_arq = hoje; rotulo = p
        rotulo = limpar(rotulo + (' (pasta local)' if onde == 'local' else ' (repositório)'), 120)
        try:
            if tipo == 'json':
                js = json.loads(texto)
                lista = js.get('canais') if isinstance(js, dict) else js
                d0 = iso(js.get('atualizado_em')) if isinstance(js, dict) else None
                novos = [de_padrao(e, 'canais.json do projeto', d0 or data_arq, limpar) for e in lista or []]
            else:
                novos = de_markdown(texto, 'registro do CMO', data_arq, limpar, hoje)
        except Exception as ex:
            log.append(f'registro {rotulo} ilegível ({ex})'); continue
        if not novos: continue
        registros.append(rotulo)
        for n in novos:
            alvo = canais.get(n['id'])
            if not alvo and n.get('_bruto'):
                for cid in ordem:
                    c = canais[cid]
                    if c.get('_casado') or not c.get('palavras'): continue
                    if any(pw and pw in n['_bruto'] for pw in c['palavras']): alvo = c; break
            n.pop('_bruto', None)
            n['fonte'] = n.get('fonte') or rotulo
            if alvo and alvo.get('_so_anterior'):
                # canal que só existia no arquivo anterior e voltou no registro: o registro manda; números anteriores ficam se forem os únicos
                velho = alvo; n['registros'] = [rotulo]
                sobrepor(n, {'numeros': {k: m for k, m in velho['numeros'].items() if m.get('valor') is not None}, 'outros': velho.get('outros') or []}, forca_texto=False)
                canais[velho['id']] = n; continue
            if alvo:
                alvo['_casado'] = True
                if tipo == 'md':   # registro do CMO: status, hipótese, decisão; números só se vierem estruturados
                    for k in ('status', 'motivo', 'hipotese', 'metrica', 'decisao', 'inicio', 'prazo'):
                        if n.get(k): alvo[k] = n[k]
                    if n.get('status') and not n.get('motivo'): alvo['motivo'] = ''
                    alvo['registros'] = [r for r in alvo.get('registros') or [] if not r.endswith('(anterior)')] + [rotulo]
                else:
                    sobrepor(alvo, n); alvo['registros'] = [r for r in alvo.get('registros') or [] if not r.endswith('(anterior)')] + [rotulo]
            else:
                n['fonte'] = n.get('fonte') or rotulo
                n.setdefault('registros', []).append(rotulo)
                canais[n['id']] = n; ordem.append(n['id'])
    if not canais: return None, log
    # saída
    lista = []
    for cid in ordem:
        c = canais[cid]
        if c.pop('_so_anterior', False):
            c['canal_mantido'] = True; log.append(f'canais: "{c.get("canal")}" (ausente → anterior)')
        c.pop('_casado', None); c.pop('palavras', None)
        if c.get('status') not in STATUS: c['status'] = 'ativo'
        datas = [m.get('medido_em') for m in list(c['numeros'].values()) + c['outros'] if m.get('valor') is not None and m.get('medido_em')]
        c['medido_em'] = max(datas) if datas else c.get('medido_em')
        for m in list(c['numeros'].values()) + c['outros']:
            m['mantido'] = m.get('valor') is not None and m.get('origem') not in FRESCO
            if m['mantido'] and m.get('origem') == 'anterior': log.append(f'canais: "{c["canal"]}" {m.get("rotulo") or m.get("nota") or ""} (vazio → anterior)')
            m['medido_em'] = br(m['medido_em']) if m.get('medido_em') else None
        for k in ('inicio', 'prazo'):
            c[k] = br(c[k]) if c.get(k) else ''
        c['medido_em'] = br(c['medido_em']) if c.get('medido_em') else ''
        c['registros'] = sorted(set(c.get('registros') or []))
        lista.append(c)
    em_op = lambda c: c['status'] in ('ativo', 'em teste')
    grupos_aq = sorted({c['grupo'] for c in lista if em_op(c) and c['tipo'] == 'aquisição'})
    grupos_vd = sorted({c['grupo'] for c in lista if em_op(c) and c['tipo'] == 'venda'})
    cont = {s: len({c['grupo'] for c in lista if c['status'] == s}) for s in STATUS}
    alerta = None
    if len(grupos_aq) == 0: alerta = 'Nenhum canal de aquisição ativo.'
    elif len(grupos_aq) == 1: alerta = f'Só 1 canal de aquisição ativo ({grupos_aq[0]}): toda a aquisição depende dele.'
    return {'nome': nome, 'repo': repo, 'slug': slug_proj, 'registros_do_projeto': registros,
            'canais': lista, 'contagem': cont, 'aquisicao_ativos': len(grupos_aq), 'venda_ativos': len(grupos_vd),
            'canais_aquisicao_ativos': grupos_aq, 'alerta': alerta}, log
