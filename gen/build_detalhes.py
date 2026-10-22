#!/usr/bin/env python3
"""Gera os dados dos painéis por projeto do Painel de Controle.

Lê  site/data/projetos.json (mantido pela rotina diária) e, para cada projeto
com repositório no GitHub, consulta a API (só leitura) e grava:
  site/data/detalhes/<repo>.json   painel completo do projeto
  site/data/detalhes/index.json    resumo para a Visão geral
Também regrava site/index.html (casca do app; os dados são carregados no navegador).

O site é PÚBLICO: tudo passa por limpar() (sem e-mails, links, caminhos, IPs,
CNPJ/CPF, telefones, tokens) e as pendências viram só títulos curtos.

Uso (de dentro do repositório):  python3 gen/build_detalhes.py
    --site   pasta do site (padrão: a pasta-mãe de gen/, ou seja, a raiz do repositório)
    --abriu  pasta local da Abriu Agora (padrão: $ABRIU_LOCAL ou /workspace/abriuagora)
Autenticação: variável GH_TOKEN/GITHUB_TOKEN ou `gh auth token`.

Rede de segurança: antes de gravar data/detalhes/<repo>.json o script lê o arquivo
anterior e mantém KPIs (bloco inteiro ou números/listas/tabelas individuais),
pendências e commits que vierem vazios/nulos nesta coleta (ver mesclar_anterior()).
"""
import argparse, datetime as dt, json, os, re, subprocess, sys, urllib.request, urllib.error, urllib.parse, csv, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import canais as CANAIS   # gen/canais.py: dashboard de canais de venda

OWNER = 'ratbragaia'
BRT = dt.timezone(dt.timedelta(hours=-3))
AGORA = dt.datetime.now(BRT)
ABRIU_LOCAL = os.environ.get('ABRIU_LOCAL') or '/workspace/abriuagora'   # --abriu sobrepõe
SITE_PADRAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo/gen/.. = repo

# ---------------------------------------------------------------- GitHub
def token():
    t = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if t: return t
    try:
        return subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        sys.exit('ERRO: sem token do GitHub (defina GH_TOKEN ou faça `gh auth login`).')

TOKEN = None
def api(path, raw=False, ok404=False):
    url = path if path.startswith('http') else 'https://api.github.com/' + path.lstrip('/')
    req = urllib.request.Request(url, headers={
        'Authorization': 'Bearer ' + TOKEN, 'User-Agent': 'painel-de-controle',
        'Accept': 'application/vnd.github.raw' if raw else 'application/vnd.github+json'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read()
            link = r.headers.get('Link', '')
    except urllib.error.HTTPError as e:
        if ok404 and e.code in (404, 409): return None
        raise
    if raw: return body.decode('utf-8', 'replace')
    data = json.loads(body or b'null')
    return (data, link) if path.endswith('#paged') else data

def paged(path, limite=500):
    out, url = [], 'https://api.github.com/' + path
    while url and len(out) < limite:
        req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + TOKEN, 'User-Agent': 'painel-de-controle', 'Accept': 'application/vnd.github+json'})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                out += json.loads(r.read()); link = r.headers.get('Link', '')
        except urllib.error.HTTPError as e:
            if e.code == 409: return []  # repositório vazio
            raise
        m = re.search(r'<([^>]+)>;\s*rel="next"', link)
        url = m.group(1) if m else None
    return out

def arquivo(repo, caminho):
    return api(f'repos/{OWNER}/{repo}/contents/' + urllib.parse.quote(caminho), raw=True, ok404=True)

# ---------------------------------------------------------------- limpeza (site público)
RX = [
    (re.compile(r'\[([^\]]+)\]\([^)]+\)'), r'\1'),                          # links markdown → texto
    (re.compile(r'[\w.+-]+@[\w-]+(\.[\w-]+)+'), '[e-mail]'),
    (re.compile(r'\b[\w.+-]+@(?=\W|$)'), '[e-mail]'),                       # "contato@"
    (re.compile(r'https?://\S+|www\.\S+'), '[link]'),
    (re.compile(r'[A-Za-z]:\\[^\s`]*'), '[caminho]'),
    (re.compile(r'(~|/home|/etc|/root|/var)/[^\s`]*'), '[caminho]'),
    (re.compile(r'\b\d{1,3}(\.\d{1,3}){3}\b'), '[IP]'),
    (re.compile(r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b'), '[CNPJ]'),
    (re.compile(r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b'), '[CPF]'),
    (re.compile(r'\b(\d{4}[ -]?){3}\d{4}\b'), '[número]'),
    (re.compile(r'(\(?\+?55\)?\s?)?\(?\d{2}\)?\s?9?\d{4}-?\d{4}\b'), '[telefone]'),
    (re.compile(r'\b(gh[pousr]_|sk-|xox[bp]-)[A-Za-z0-9_-]+'), '[segredo]'),
    (re.compile(r'\b[A-Za-z0-9_-]{32,}\b'), '[id]'),
]
def limpar(s, maximo=160):
    s = s or ''
    for rx, sub in RX: s = rx.sub(sub, s)
    s = re.sub(r'\*\*|__|~~|[*`]', '', s)          # marcação markdown
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\s+', ' ', s).strip(' -–:;,')
    if len(s) > maximo: s = s[:maximo - 1].rsplit(' ', 1)[0] + '…'
    return s

def titulo_curto(s, maximo=110):
    """Primeiro trecho em negrito, ou a primeira frase."""
    m = re.match(r'\s*(?:[^\w*]*\s*)?\*\*(.+?)\*\*', s)
    t = m.group(1) if m else re.split(r'(?<=[.!?])\s|\s—\s|;\s', s, maxsplit=1)[0]
    return limpar(t, maximo)

def sem_valores(s):
    return re.sub(r'R\$\s?[\d.,]+(\s?mil)?', 'R$ …', s)

PRAZO = re.compile(r'\b(até|vence|prazo|em|dia)?\s*(\d{1,2}/\d{1,2}(?:/\d{2,4})?)\b')
def prazo(s):
    m = re.search(r'\b(?:até|vence[mr]?|prazo:?|para o dia|no dia)\s+(\d{1,2}/\d{1,2}(?:/\d{2,4})?)', s, re.I)
    return m.group(1) if m else None

# ---------------------------------------------------------------- pendências
PARAR = re.compile(r'(decis|revis[aã]o mensal|datas travadas|radar|hist[oó]rico|feito|checagem|conclu|resolvid|arquiv)', re.I)
def pendencias_md(texto, fonte):
    itens, ativo, parar_no_hist = [], True, False
    for linha in texto.splitlines():
        h = re.match(r'^(#{1,4})\s+(.*)', linha)
        if h:
            if re.search(r'hist[oó]rico', h.group(2), re.I): break
            ativo = not PARAR.search(h.group(2)); continue
        l = linha.strip()
        m = re.match(r'^[-*]\s+\[( |x|X)\]\s+(.*)', l)
        if m:
            if m.group(1) == ' ': itens.append(m.group(2))
            continue
        if not ativo: continue
        if l.startswith('>') and '🔔' in l:
            itens.append(l.lstrip('> ').replace('🔔', '').strip()); continue
        m = re.match(r'^[-*]\s+\[( |x|X)\]\s+(.*)', l)
        if m:
            if m.group(1) == ' ': itens.append(m.group(2))
            continue
        m = re.match(r'^(?:\d+[.)]|[-*])\s+(.*)', linha)  # só itens de 1º nível
        if m:
            t = m.group(1).strip()
            if re.match(r'^(✅|❌|~~|\(resolvid|\*?\(resolvid)', t): continue
            if re.search(r'^\*?\*?(resolvid|feito|conclu)', t, re.I): continue
            itens.append(t)
    vistos, out = set(), []
    for t in itens:
        tit = sem_valores(titulo_curto(t))
        if not tit or tit.lower() in vistos: continue
        vistos.add(tit.lower())
        out.append({'titulo': tit, 'prazo': prazo(tit)})
    return out

def pendencias_secao(texto, rx_titulo):
    """Seção 'Pendências conhecidas' em CLAUDE.md/README.md (parágrafos ou bullets com negrito)."""
    linhas, dentro, nivel = [], False, 0
    for linha in texto.splitlines():
        h = re.match(r'^(#{1,4})\s+(.*)', linha)
        if h:
            if dentro and len(h.group(1)) <= nivel: break
            if re.search(rx_titulo, h.group(2), re.I) and 'ler no in' not in h.group(2):
                dentro, nivel = True, len(h.group(1)); continue
        if dentro: linhas.append(linha)
    if not linhas: return None
    out, par = [], ''
    for l in linhas + ['']:
        if not l.strip() or re.match(r'^\s*[-*]\s|^\s*\d+[.)]\s', l):
            if par.strip(): out.append(par.strip())
            par = re.sub(r'^\s*([-*]|\d+[.)])\s+', '', l)
        else: par += ' ' + l
    out = [p for p in out if p and p != '---']
    return [{'titulo': t, 'prazo': prazo(t)} for t in (sem_valores(titulo_curto(p)) for p in out)]

def handoff_checklist(texto):
    itens, total, feitos = [], 0, 0
    for l in texto.splitlines():
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        if len(c) >= 4 and c[0].isdigit():
            total += 1; st = c[-1]
            if st.startswith('✅'): feitos += 1
            elif st.startswith('⬜') or not st:
                itens.append({'titulo': limpar(re.split(r'\s\(|:', c[1])[0], 110), 'prazo': None})
    return itens, total, feitos

def buscar_pendencias(repo, caminhos):
    lower = {p.lower(): p for p in caminhos}
    cands = [lower[k] for k in ('pendencias.md', 'pendências.md') if k in lower]
    cands += sorted(p for p in caminhos if re.search(r'(^|/)pend[eê]ncias\.md$', p, re.I) and p not in cands)
    for c in cands:
        t = arquivo(repo, c)
        if t is not None:
            return {'fonte': c, 'itens': pendencias_md(t, c)}
    for c in ('CLAUDE.md', 'README.md'):
        if c in caminhos:
            t = arquivo(repo, c) or ''
            r = pendencias_secao(t, r'pend[eê]ncias (conhecidas|abertas|atuais)|^pend[eê]ncias$|^a fazer|^todo')
            if r is not None:
                return {'fonte': c + ' (seção de pendências)', 'itens': r}
    if 'docs/handoff-checklist.md' in caminhos:
        itens, tot, ok = handoff_checklist(arquivo(repo, 'docs/handoff-checklist.md') or '')
        return {'fonte': 'docs/handoff-checklist.md (itens do fundador)', 'itens': itens}
    return None

# ---------------------------------------------------------------- KPIs específicos
def num(rx, texto, grupo=1):
    m = re.search(rx, texto, re.I | re.S)
    return m.group(grupo) if m else None

def tabela_md(texto, depois_de=None):
    if depois_de:
        i = texto.find(depois_de)
        if i < 0: return None
        texto = texto[i:]
    linhas = [l for l in texto.splitlines() if l.strip().startswith('|')]
    bloco = []
    for l in texto.splitlines():
        if l.strip().startswith('|'): bloco.append(l)
        elif bloco: break
    if len(bloco) < 3: return None
    rows = [[limpar(c, 80) for c in l.strip().strip('|').split('|')] for l in bloco]
    return {'colunas': rows[0], 'linhas': [r for r in rows[2:]]}

SENSIVEL = re.compile(r'(cis[o]|seguran|webhook|token|senha|chave|permiss|vps|patch|backup|porta|cabe[cç]alho|servidor|\.env)', re.I)
def kpis_abriuagora(repo, caminhos):
    if not os.path.isdir(ABRIU_LOCAL): return None
    fontes, numeros, tabelas, listas = [], [], [], []
    obj = os.path.join(ABRIU_LOCAL, 'objetivos.md')
    if os.path.exists(obj):
        t = open(obj, encoding='utf-8').read(); fontes.append('objetivos.md')
        quando = num(r'Ponto de partida \(([^,)]+)', t)
        bloco = t[t.find('Ponto de partida'):][:1500] if 'Ponto de partida' in t else ''
        for rot, rx in [('Convites enviados', r'Convites[^:]*:\s*(\d+)'), ('Entregues', r'Entregues:\s*(\d+)'),
                        ('Falhas', r'Falhas:\s*(\d+)'), ('Spam', r'Spam\s*(\d+)'), ('Descadastros', r'Descadastros\s*(\d+)'),
                        ('Pedidos de amostra', r'Pedidos de amostra[^:]*:\s*(\d+)'), ('Pagantes', r'Pagantes:\s*(\d+)'),
                        ('Receita', r'Receita:\s*(R\$\s*[\d.,]+)')]:
            v = num(rx, bloco)
            if v is not None: v = v.rstrip('.,')
            if v is not None: numeros.append({'rotulo': rot, 'valor': v, 'detalhe': f'em {quando}' if quando else ''})
        conv = num(r'Convites[^:]*:\s*(\d+)', bloco); ent = num(r'Entregues:\s*(\d+)', bloco)
        if conv and ent and int(conv):
            numeros.append({'rotulo': 'Taxa de entrega', 'valor': f'{100*int(ent)/int(conv):.0f}%'.replace('.', ','), 'detalhe': f'{ent} de {conv}'})
        portao = num(r'## Norte até ([^\n]+)\n([^\n]+)', t, 2)
        if portao: listas.append({'titulo': 'Meta do Portão 1 (até 31/10)', 'itens': [limpar(portao, 200)]})
        empresa = re.search(r'## Objetivo da empresa\n(.*?)\n##', t, re.S)
        if empresa:
            itens = [titulo_curto(l[2:], 150) for l in empresa.group(1).splitlines() if l.startswith('- ')][:2]
            listas.append({'titulo': 'Objetivo da empresa', 'itens': itens})
    meta = os.path.join(ABRIU_LOCAL, 'meta-mensal.md')
    if os.path.exists(meta):
        t = open(meta, encoding='utf-8').read(); fontes.append('meta-mensal.md')
        tb = tabela_md(t)
        if tb:
            tb['titulo'] = 'Meta mensal de receita (pagantes, receita e lucro)'
            tabelas.append(tb)
            mes = AGORA.strftime('%m/%Y'); nomes = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
            rot = f"{nomes[AGORA.month-1]}/{AGORA.year}"
            for l in tb['linhas']:
                if l and l[0] == rot:
                    numeros.insert(0, {'rotulo': f'Meta de {rot}', 'valor': l[3] if len(l) > 3 else '', 'detalhe': f'pagantes: {l[1]} · {l[5] if len(l) > 5 else ""}'})
    reg = os.path.join(ABRIU_LOCAL, 'registro-ajustes.md')
    if os.path.exists(reg):
        fontes.append('registro-ajustes.md')
        cont, abertos = {}, []
        for l in open(reg, encoding='utf-8'):
            if not re.match(r'^- \*\*\d{8}-', l): continue
            f = [x.strip() for x in l.split(' | ')]
            PRIOS = {'urgente': 'URGENTE', 'alta': 'alta', 'média': 'média', 'media': 'média', 'baixa': 'baixa'}
            if len(f) >= 6 and f[1].lower() in PRIOS:
                # formato novo (C-levels, 21/10): id | PRIORIDADE | STATUS | data | cargo | texto
                idt = f[0].strip('-* '); prio = f[1]; st = f[2].upper(); cargo = f[4]; erro = ' | '.join(f[5:])
            elif len(f) >= 8:
                # formato antigo: id | cargo | erro | … | … | prioridade | … | status
                idt = f[0].strip('-* '); cargo = f[1]; erro = f[2]; prio = f[5]; st = f[7].upper()
            else:
                continue
            prio = PRIOS.get(prio.strip('* ').lower(), '—')       # nunca publica texto livre no campo de prioridade
            st = re.sub(r'[^A-ZÁÉÍÓÚÂÊÔÃÕÇ ]', '', st).strip()[:20] or 'ABERTO'
            idt = limpar(idt, 40)
            cont[st] = cont.get(st, 0) + 1
            if st != 'CONCLUÍDO':
                tit = 'Item técnico/segurança (detalhe só no registro interno)' if SENSIVEL.search(cargo + ' ' + erro) else sem_valores(limpar(re.split(r';|\s—\s', erro)[0], 110))
                abertos.append({'id': idt, 'cargo': limpar(cargo.split('/')[0], 20), 'prioridade': prio, 'status': st.capitalize(), 'titulo': tit})
        ordem = {'URGENTE': 0, 'alta': 1, 'média': 2, 'baixa': 3}
        abertos.sort(key=lambda a: ordem.get(a['prioridade'], 9))
        total = sum(cont.values())
        numeros.append({'rotulo': 'Ajustes dos C-levels em aberto', 'valor': str(len(abertos)), 'detalhe': f'de {total} registrados · ' + ', '.join(f'{v} {k.lower()}' for k, v in sorted(cont.items()))})
        listas.append({'titulo': 'Ajustes em aberto (C-levels → COO)', 'tipo': 'ajustes', 'itens': abertos})
    rc = os.path.join(ABRIU_LOCAL, 'resumos-clevels')
    if os.path.isdir(rc):
        arqs = sorted(f for f in os.listdir(rc) if re.match(r'\d{4}-\d{2}-\d{2}-\w+\.md$', f))
        if arqs:
            ult = arqs[-1][:10]
            cargos = sorted(f[11:-3].upper() for f in arqs if f.startswith(ult))
            fontes.append('resumos-clevels/')
            d = dt.date.fromisoformat(ult).strftime('%d/%m/%Y')
            numeros.append({'rotulo': 'Resumos de C-levels', 'valor': str(len(cargos)), 'detalhe': f'em {d}: ' + ', '.join(cargos)})
    if 'metricas.md' in caminhos:
        fontes.append('metricas.md (repo)')
    if not numeros and not tabelas: return None
    return {'titulo': 'Indicadores da Abriu Agora', 'fontes': fontes, 'numeros': numeros, 'tabelas': tabelas, 'listas': listas,
            'nota': 'Números copiados dos arquivos do CEO/COO; nada é estimado pelo painel.'}

def kpis_vagassjdr(repo, caminhos):
    numeros, fontes = [], []
    if 'registro-publicadas.csv' in caminhos:
        t = arquivo(repo, 'registro-publicadas.csv') or ''
        linhas = list(csv.DictReader(io.StringIO(t)))
        if linhas:
            fontes.append('registro-publicadas.csv')
            datas = sorted(l.get('data', '') for l in linhas if l.get('data'))
            numeros.append({'rotulo': 'Vagas publicadas', 'valor': str(len(linhas)), 'detalhe': f'de {fmt_data(datas[0])} a {fmt_data(datas[-1])}' if datas else ''})
            ult7 = sum(1 for d in datas if d >= (AGORA.date() - dt.timedelta(days=6)).isoformat())
            numeros.append({'rotulo': 'Publicadas nos últimos 7 dias', 'valor': str(ult7), 'detalhe': ''})
    pend = [p for p in caminhos if re.match(r'n8n/pendentes/[^/]+\.json$', p)]
    if pend:
        fontes.append('n8n/pendentes/')
        numeros.append({'rotulo': 'Vagas na fila (n8n/pendentes)', 'valor': str(len(pend)), 'detalhe': 'aguardando aprovação'})
    return {'titulo': 'Indicadores das Vagas SJDR', 'fontes': fontes, 'numeros': numeros, 'tabelas': [], 'listas': []} if numeros else None

def kpis_finbook(repo, caminhos):
    numeros, fontes, tabelas = [], [], []
    if 'ceo/financeiro.csv' in caminhos:
        t = arquivo(repo, 'ceo/financeiro.csv') or ''
        linhas = list(csv.DictReader(io.StringIO(t)))
        if linhas:
            fontes.append('ceo/financeiro.csv')
            def soma(campo, filtro=lambda l: True):
                s = 0.0
                for l in linhas:
                    try:
                        if filtro(l): s += float(l.get(campo) or 0)
                    except ValueError: pass
                return s
            brl = lambda v: 'R$ ' + f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
            ult = max(l['date'] for l in linhas if l.get('date'))
            numeros.append({'rotulo': 'Receita bruta registrada', 'valor': brl(soma('gross', lambda l: l.get('type') != 'custo')), 'detalhe': f'até {fmt_data(ult)}'})
            numeros.append({'rotulo': 'Resultado líquido registrado', 'valor': brl(soma('net')), 'detalhe': f'até {fmt_data(ult)}'})
    blog = [p for p in caminhos if re.match(r'site/blog/[^/]+/index\.html$', p)]
    if blog:
        fontes.append('site/blog/'); numeros.append({'rotulo': 'Artigos no blog', 'valor': str(len(blog)), 'detalhe': 'páginas em site/blog'})
    rot = [p for p in caminhos if re.match(r'social/shorts/roteiro-\d+.*\.md$', p)]
    if rot:
        fontes.append('social/shorts/'); numeros.append({'rotulo': 'Roteiros de Shorts', 'valor': str(len(rot)), 'detalhe': 'arquivos roteiro-*.md'})
    return {'titulo': 'Indicadores do Finbook', 'fontes': fontes, 'numeros': numeros, 'tabelas': [], 'listas': []} if numeros else None

def kpis_base(repo, caminhos):
    nomes = {'10-fontes': 'Fontes', '20-conhecimento': 'Notas de conhecimento', '30-conceitos': 'Conceitos', '50-ferramentas': 'Ferramentas', '70-topicos': 'Tópicos', '05-mensagens': 'Mensagens'}
    numeros = []
    for pasta, rot in nomes.items():
        n = sum(1 for p in caminhos if p.startswith(f'cerebro/{pasta}/') and p.endswith('.md'))
        if n: numeros.append({'rotulo': rot, 'valor': str(n), 'detalhe': f'cerebro/{pasta}'})
    return {'titulo': 'Tamanho do cérebro', 'fontes': ['cerebro/ (contagem de notas .md)'], 'numeros': numeros, 'tabelas': [], 'listas': []} if numeros else None

KPIS = {'abriuagora': kpis_abriuagora, 'vagassjdr': kpis_vagassjdr, 'finbook': kpis_finbook,
        'BaseDeConhecimento': kpis_base}

# ---------------------------------------------------------------- modo público mínimo
# gen/publico_minimo.json: projetos que aparecem no site público SÓ com nome + site (sem KPIs, canais,
# números, resumos, pendências, commits, prospects nem link do repositório). Ver aplicar_publico_minimo().
ARQ_MINIMO = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'publico_minimo.json')
def carregar_minimo():
    try:
        return [x for x in json.load(open(ARQ_MINIMO, encoding='utf-8')).get('projetos', []) if x.get('nome')]
    except FileNotFoundError:
        return []
    except Exception as ex:   # lista ilegível: não arrisca publicar dados → para tudo
        sys.exit(f'ERRO: gen/publico_minimo.json ilegível ({ex}); corrija antes de gerar o site público.')
MINIMO = carregar_minimo()
def minimo_de(p):
    for m in MINIMO:
        if p.get('nome') == m['nome'] or (p.get('repo') and p.get('repo') == m.get('repo')): return m
    return None
def entrada_minima(m):
    e = {'nome': m['nome'], 'publico_minimo': True}
    if m.get('site'): e['site'] = m['site']
    if m.get('nota'): e['nota'] = m['nota']
    return e
NOMES_MINIMO = [n for m in MINIMO for n in {m['nome'], m.get('repo') or m['nome']}]
RX_MINIMO = re.compile('|'.join(re.escape(n) for n in NOMES_MINIMO), re.I) if NOMES_MINIMO else None
def tirar_mencoes(v):
    """Em dados de OUTROS projetos, troca qualquer texto que cite um projeto em modo público mínimo."""
    if RX_MINIMO is None: return v
    if isinstance(v, str): return '[omitido no painel público]' if RX_MINIMO.search(v) else v
    if isinstance(v, list): return [tirar_mencoes(x) for x in v]
    if isinstance(v, dict): return {k: tirar_mencoes(x) for k, x in v.items()}
    return v
def limpar_scripts_update(gen_dir):
    """Remove dos gen/update_*.py (publicados no site) os blocos p = P["<projeto>"] dos projetos em modo mínimo."""
    if not MINIMO: return
    nomes = '|'.join(re.escape(m['nome']) for m in MINIMO)
    ini = re.compile(r'\s*p\s*=\s*P\[\s*[\'"](' + nomes + r')[\'"]\s*\]')
    cab = re.compile(r'\s*#\s*-+\s*(' + nomes + r')\b')
    fim = re.compile(r'\s*(p\s*=\s*P\[|#\s*-+|ordem\s*=)')
    for f in sorted(os.listdir(gen_dir)):
        if not re.match(r'update_.*\.py$', f): continue
        cam = os.path.join(gen_dir, f); L = open(cam, encoding='utf-8').read().split('\n'); out, i, n = [], 0, 0
        while i < len(L):
            nxt = L[i + 1] if i + 1 < len(L) else ''
            if ini.match(L[i]) or (cab.match(L[i]) and ini.match(nxt)):
                nome = (ini.match(L[i]) or ini.match(nxt)).group(1)
                i += 1 if ini.match(L[i]) else 2
                while i < len(L) and not fim.match(L[i]): i += 1
                out += [f'# {nome}: modo público mínimo (gen/publico_minimo.json) — bloco removido pelo gerador', '']; n += 1
                continue
            out.append(L[i]); i += 1
        if n:
            open(cam, 'w', encoding='utf-8').write('\n'.join(out))
            print(f'    público mínimo: {n} bloco(s) removido(s) de gen/{f}')

# ---------------------------------------------------------------- util
def fmt_data(iso):
    try: return dt.date.fromisoformat(iso[:10]).strftime('%d/%m/%Y')
    except Exception: return iso

def brt(iso):
    return dt.datetime.fromisoformat(iso.replace('Z', '+00:00')).astimezone(BRT)

def slug(p):
    base = p.get('repo') or p['nome']
    s = re.sub(r'[^a-z0-9]+', '-', base.lower().encode('ascii', 'ignore').decode()).strip('-')
    return s or 'projeto'

def detalhar(p):
    repo = p['repo']
    info = api(f'repos/{OWNER}/{repo}')
    since = (AGORA - dt.timedelta(days=30)).astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    commits = paged(f'repos/{OWNER}/{repo}/commits?per_page=100&since={since}', 1000)
    recentes = commits[:10] if len(commits) >= 10 else (paged(f'repos/{OWNER}/{repo}/commits?per_page=10', 10) or [])
    prs = paged(f'repos/{OWNER}/{repo}/pulls?state=open&per_page=100', 300)
    langs = api(f'repos/{OWNER}/{repo}/languages') or {}
    tree = api(f"repos/{OWNER}/{repo}/git/trees/{info['default_branch']}?recursive=1", ok404=True) or {'tree': []}
    caminhos = [t['path'] for t in tree.get('tree', []) if t.get('type') == 'blob']

    hoje = AGORA.date()
    dias = {(hoje - dt.timedelta(days=i)).isoformat(): 0 for i in range(29, -1, -1)}
    for c in commits:
        d = brt(c['commit']['committer']['date']).date().isoformat()
        if d in dias: dias[d] += 1
    c7 = sum(v for k, v in dias.items() if k >= (hoje - dt.timedelta(days=6)).isoformat())
    tot = sum(langs.values()) or 1
    ult = recentes[0]['commit']['committer']['date'] if recentes else None
    pend = buscar_pendencias(repo, caminhos)
    kp = KPIS.get(repo)
    kpis = kp(repo, caminhos) if kp else None
    try:
        canais = CANAIS.montar(repo, p['nome'], slug(p), caminhos, lambda c: arquivo(repo, c), limpar,
                               CANAIS_ANT.get(repo), AGORA.date().isoformat(), CANAIS_BASE)
    except Exception as ex:
        canais = (None, [f'canais: erro na coleta ({ex}); bloco anterior mantido']) if CANAIS_ANT.get(repo) else (None, [])
        if CANAIS_ANT.get(repo): canais = (CANAIS_ANT[repo], canais[1])
    return {
        '_canais': canais,
        'repo': repo, 'slug': slug(p),
        'estatisticas': {
            'linguagem': info.get('language'),
            'linguagens': [{'nome': k, 'pct': round(100 * v / tot, 1)} for k, v in sorted(langs.items(), key=lambda x: -x[1])[:4]],
            'ultimo_commit': brt(ult).strftime('%d/%m/%Y %H:%M') if ult else None,
            'commits_7d': c7, 'commits_30d': sum(dias.values()),
            'commits_30d_truncado': len(commits) >= 1000,
            'por_dia': [{'dia': k, 'n': v} for k, v in dias.items()],
            'issues_abertas': max(0, (info.get('open_issues_count') or 0) - len(prs)),
            'prs_abertos': len(prs),
            'arquivos': len(caminhos),
            'branch': info.get('default_branch'),
        },
        'commits': [{'quando': brt(c['commit']['committer']['date']).strftime('%d/%m %H:%M'),
                     'msg': limpar(c['commit']['message'].splitlines()[0], 140), 'sha': c['sha'][:7]} for c in recentes[:10]],
        'pendencias': pend,
        'kpis': kpis,
    }

# ---------------------------------------------------------------- rede de segurança
def _vazio(v):
    return v is None or v == '' or v == [] or v == {}

def _chave(rotulo):
    # 'Meta de Out/2026' e 'Meta de Nov/2026' são o mesmo indicador
    return re.sub(r'\b[A-Z][a-zç]{2}/\d{4}\b', '<mês>', rotulo or '').strip().lower()

def mesclar_kpis(novo, antigo, log):
    if _vazio(antigo): return novo
    if _vazio(novo) or (_vazio(novo.get('numeros')) and _vazio(novo.get('tabelas')) and _vazio(novo.get('listas'))):
        log.append('kpis (bloco inteiro mantido do arquivo anterior)')
        return antigo
    out = dict(novo)
    for campo, chave_item in (('numeros', 'rotulo'), ('tabelas', 'titulo'), ('listas', 'titulo')):
        atuais = list(out.get(campo) or [])
        idx = {_chave(x.get(chave_item)): i for i, x in enumerate(atuais)}
        for velho in antigo.get(campo) or []:
            k = _chave(velho.get(chave_item))
            if k in idx:
                i = idx[k]; atual = atuais[i]
                vazio = _vazio(atual.get('valor')) if campo == 'numeros' else \
                        _vazio(atual.get('linhas')) if campo == 'tabelas' else _vazio(atual.get('itens'))
                if vazio and not (_vazio(velho.get('valor')) if campo == 'numeros' else
                                  _vazio(velho.get('linhas')) if campo == 'tabelas' else _vazio(velho.get('itens'))):
                    atuais[i] = velho; log.append(f'kpis.{campo}: "{velho.get(chave_item)}" (valor vazio → anterior)')
            else:
                atuais.append(velho); idx[k] = len(atuais) - 1
                log.append(f'kpis.{campo}: "{velho.get(chave_item)}" (ausente → anterior)')
        out[campo] = atuais
    fontes = list(out.get('fontes') or [])
    for f in antigo.get('fontes') or []:
        if f not in fontes: fontes.append(f)
    out['fontes'] = fontes
    for k, v in antigo.items():
        if k not in out or _vazio(out.get(k)):
            if not _vazio(v) and k not in ('numeros', 'tabelas', 'listas'): out[k] = v
    return out

def mesclar_anterior(det, caminho):
    """Mantém do arquivo anterior o que veio nulo/vazio nesta coleta. Devolve a lista do que foi mantido."""
    log = []
    try:
        antigo = json.load(open(caminho, encoding='utf-8'))
    except Exception:
        return log
    det['kpis'] = mesclar_kpis(det.get('kpis'), antigo.get('kpis'), log)
    if det.get('pendencias') is None and antigo.get('pendencias'):
        det['pendencias'] = antigo['pendencias']; log.append('pendencias (fonte não encontrada → anterior)')
    if not det.get('commits') and antigo.get('commits'):
        det['commits'] = antigo['commits']; log.append('commits (lista vazia → anterior)')
    return log

CANAIS_ANT, CANAIS_BASE = {}, {}

INDEX_HTML = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index_template.html'), encoding='utf-8').read() \
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index_template.html')) else None

def main():
    global TOKEN
    ap = argparse.ArgumentParser()
    ap.add_argument('--site', default=SITE_PADRAO, help=f'pasta do site (padrão: {SITE_PADRAO})')
    ap.add_argument('--abriu', default=None, help='pasta local da Abriu Agora (padrão: $ABRIU_LOCAL ou /workspace/abriuagora)')
    ap.add_argument('--sem-index', action='store_true', help='não regravar index.html')
    a = ap.parse_args()
    global ABRIU_LOCAL
    if a.abriu: ABRIU_LOCAL = a.abriu
    CANAIS.LOCAIS_PADRAO['abriuagora'] = [ABRIU_LOCAL]
    if not os.path.isdir(ABRIU_LOCAL):
        print(f'aviso: pasta da Abriu Agora não encontrada ({ABRIU_LOCAL}); KPIs dela virão do arquivo anterior', file=sys.stderr)
    TOKEN = token()
    arq_proj = os.path.join(a.site, 'data/projetos.json')
    d = json.load(open(arq_proj, encoding='utf-8'))
    pasta = os.path.join(a.site, 'data/detalhes'); os.makedirs(pasta, exist_ok=True)
    # modo público mínimo: reescreve a entrada do projeto (só nome + site) e tira menções dele dos outros
    CANAIS.PUBLICO_MINIMO = set(NOMES_MINIMO)
    projs = []
    for p in d['projetos']:
        m = minimo_de(p)
        if m:
            projs.append(entrada_minima(m))
            for arq in {p.get('repo'), m.get('repo')} - {None}:
                cam = os.path.join(pasta, arq + '.json')
                if os.path.exists(cam): os.remove(cam); print(f'    público mínimo: {arq} → data/detalhes/{arq}.json removido')
        else:
            projs.append(tirar_mencoes(p))
    d['projetos'] = projs
    with open(arq_proj, 'w', encoding='utf-8') as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2); fh.write('\n')
    limpar_scripts_update(os.path.dirname(os.path.abspath(__file__)))
    resumo, falhas = [], []
    try:
        idx_antigo = {x.get('repo'): x for x in json.load(open(os.path.join(pasta, 'index.json'), encoding='utf-8')).get('projetos', []) if x.get('repo')}
    except Exception:
        idx_antigo = {}
    global CANAIS_ANT, CANAIS_BASE
    arq_canais = os.path.join(a.site, 'data/canais.json')
    try:
        CANAIS_ANT = {e['repo']: e for e in json.load(open(arq_canais, encoding='utf-8')).get('empresas', [])
                      if e.get('repo') and e['repo'] not in NOMES_MINIMO and e.get('nome') not in NOMES_MINIMO}
    except Exception:
        CANAIS_ANT = {}
    try:
        CANAIS_BASE = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'canais_base.json'), encoding='utf-8'))
        for n in NOMES_MINIMO: CANAIS_BASE.pop(n, None)
    except Exception as ex:
        print(f'aviso: gen/canais_base.json ilegível ({ex}); canais só dos registros dos projetos', file=sys.stderr); CANAIS_BASE = {}
    empresas = []
    for p in d['projetos']:
        if p.get('publico_minimo'):
            resumo.append(dict(p, slug=slug(p), arquivo=None)); print(f"ok  {p['nome']:<26} (público mínimo: só nome + site)")
            continue
        item = {'nome': p['nome'], 'slug': slug(p), 'repo': p.get('repo'), 'arquivo': None}
        if p.get('repo'):
            try:
                det = detalhar(p)
                emp, logc = det.pop('_canais', (None, []))
                for m in logc: print(f"    mantido em {p['repo']}: {m}")
                if emp:
                    empresas.append(emp)
                    item.update(canais_aquisicao_ativos=emp['aquisicao_ativos'], canais_total=len(emp['canais']), canais_alerta=emp['alerta'])
                det = tirar_mencoes(det)
                if emp: empresas[-1] = emp = tirar_mencoes(emp)
                det['gerado_em'] = AGORA.strftime('%d/%m/%Y %H:%M')
                destino = os.path.join(pasta, p['repo'] + '.json')
                for m in mesclar_anterior(det, destino):
                    print(f"    mantido em {p['repo']}: {m}")
                with open(destino, 'w', encoding='utf-8') as fh:
                    json.dump(det, fh, ensure_ascii=False, indent=1)
                e = det['estatisticas']
                item.update(arquivo=f"data/detalhes/{p['repo']}.json", commits_7d=e['commits_7d'], commits_30d=e['commits_30d'],
                            ultimo_commit=e['ultimo_commit'], linguagem=e['linguagem'], prs_abertos=e['prs_abertos'], issues_abertas=e['issues_abertas'],
                            pendencias=len(det['pendencias']['itens']) if det['pendencias'] else None, tem_kpis=bool(det['kpis']))
                print(f"ok  {p['repo']:<26} 7d={e['commits_7d']:<4} 30d={e['commits_30d']:<5} pend={item['pendencias']} kpis={item['tem_kpis']}")
            except Exception as ex:
                falhas.append(p['repo']); print(f"ERRO {p['repo']}: {ex}", file=sys.stderr)
                if p['repo'] in CANAIS_ANT:
                    empresas.append(CANAIS_ANT[p['repo']]); print(f"    mantido em {p['repo']}: canais (projeto falhou → anterior)")
                if p['repo'] in idx_antigo:   # mantém a entrada anterior (o .json antigo continua no lugar)
                    item = dict(idx_antigo[p['repo']], nome=p['nome'], slug=slug(p))
        resumo.append(item)
    empresas = [e for e in empresas if e.get('repo') not in NOMES_MINIMO and e.get('nome') not in NOMES_MINIMO]
    json.dump({'gerado_em': AGORA.strftime('%d/%m/%Y %H:%M') + ' (horário de Brasília)', 'projetos': resumo},
              open(os.path.join(pasta, 'index.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    with open(arq_canais, 'w', encoding='utf-8') as fh:
        json.dump({'titulo': 'Canais de venda e aquisição', 'gerado_em': AGORA.strftime('%d/%m/%Y %H:%M') + ' (horário de Brasília)',
                   'nota': 'Números copiados dos arquivos de cada empresa (registro do CMO, resumos dos C-levels, métricas); nada é estimado pelo painel. "sem dado" = não medido.',
                   'empresas': empresas}, fh, ensure_ascii=False, indent=1)
    print(f"canais: {len(empresas)} empresa(s) em data/canais.json: " + ', '.join(f"{e['nome']}={e['aquisicao_ativos']} ativo(s)" + (' ⚠' if e['alerta'] else '') for e in empresas))
    if INDEX_HTML and not a.sem_index:
        open(os.path.join(a.site, 'index.html'), 'w', encoding='utf-8').write(INDEX_HTML)
    if falhas: print('Falharam:', ', '.join(falhas), file=sys.stderr); sys.exit(1)

if __name__ == '__main__':
    main()
