"""Dashboard resumido do topo do Painel de Controle (data/resumo.json).

Chamado por build_detalhes.py depois dos painéis por projeto. Monta:
  * uma aba por empresa (ordem em gen/resumo_base.json) só com META x RESULTADO;
  * o "Histórico dos C-levels": quando cada rotina de C-level/CEO/COO rodou (mais recente primeiro).

De onde vêm os números (para cada resultado vale o de medição mais recente; empate → o extraído):
  1. gen/resumo_base.json      registro mantido no painel (meta e resultado com fonte e data);
  2. data/resumo.json anterior rede de segurança (se o registro e a extração vierem vazios);
  3. extração automática       arquivos do CEO/COO de cada empresa (ver extrair_*).
De onde vem o histórico (só evidência real de execução):
  * Abriu Agora:  $ABRIU_LOCAL/resumos-clevels/AAAA-MM-DD-<cargo>.md (cada "Rodada" do COO conta uma vez);
  * Finbook:      commits do repositório finbook cuja mensagem começa pelo cargo (CEO, COO, CCO, CISO…);
  * Vagas SJDR:   $VAGAS_CLEVELS/diario.md (cabeçalhos "### DD/MM HH:MM — <rotina>");
  * Edital Lido:  commits de decisões (ADR) em qualquer branch do repositório editallido cujo texto diz que o CEO decidiu;
  * o histórico anterior (data/resumo.json) é mantido quando a fonte some (janela de DIAS_HIST dias).
Projetos que voltarem a gen/publico_minimo.json aparecem só com nome + site: sem indicadores nem histórico (lista vazia desde 26/10/2026).
Site público: textos passam por limpar(); a frase de resultado só sai se não tiver nome próprio desconhecido
(prospect/cliente), contato, caminho ou tema de segurança — na dúvida, a frase é omitida.
"""
import csv, datetime as dt, io, json, os, re, unicodedata

DIAS_HIST = 30
MAX_HIST = 400
PATENT_LOCAL = os.environ.get('PATENT_LOCAL') or '/workspace/patentsonar/clevels'
VAGAS_CLEVELS = os.environ.get('VAGAS_CLEVELS') or '/workspace/clevels/vagas-sjdr'
MESES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
MESES_LONGOS = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
CARGOS = ('CEO', 'COO', 'CCO', 'CISO', 'CSO', 'CMO', 'CFO', 'CLO', 'CTO', 'CS')

# ------------------------------------------------------------------ privacidade da frase de resultado
# Palavras com maiúscula que podem aparecer (cargos, produtos e plataformas próprias ou públicas, termos comuns).
# Qualquer outra palavra com maiúscula (em geral nome de prospect, cliente ou pessoa) derruba o trecho.
PERMITIDAS = set('''
CEO COO CCO CISO CSO CMO CFO CLO CTO CS C-levels C-level Diretoria Rodrigo Claude Grok Bot Assistente Pessoal
Abriu Agora Finbook Vagas SJDR Edital Lido Kit MEI Dia Pacote Profissões Combo Controle Limite Calculadora
Instagram Facebook TikTok YouTube LinkedIn Shorts Short Kiwify Hotmart Asaas Resend Gmail Google Search Console GSC
Cloudflare Pix Dependabot Outlook Paddle DMARC PECR SBIR OPS BigQuery Hunter G2 Capterra PatentSonar Supabase GitHub Postgres RLS CI SMS Pull Request PR
Cloudflare Pix POST STORY STORYs Fixado Direct Telegram Meta Business Suite Insights WhatsApp Chrome
LC PGFN DAS DASN SIMEI FAQ PDF CTA SEO GEO UTM KV API IA URL HTML CSV ADR OK BRT FB SMS LGPD CDC CNAE PNCP MRR OTIF NFS-e
Portão Out Nov Dez Jan Fev Mar Abr Mai Jun Jul Ago Set Brasília Minas Gerais MG São João Rei Tiradentes
Feito Fazendo Novo Nova Travou Atrasado Aguardando Placar Estratégia Rascunhos Rascunho Resumo Resultado Resultados
Varredura Rodada Fila Decisão Decisões Sem Site Página Home Capa Lote Nota Número Status Tarefa Tarefas Itens Item
Consolidado Ciclo Manhã Noite Fechamento Semana Semanal Parecer Auditoria Canais Canal Envio Envios Prospecção
Parceria Parcerias Amostra Amostras Pagantes Receita Lucro Vendas Venda Visitas Leads Funil Oferta Ofertas Plano
Mensagem Mensagens Prévia Leitura Leituras Ajuste Ajustes Checklist Política Privacidade Termos Blog Artigo Artigos
Vídeo Vídeos Post Posts Newsletter Página Páginas Projeção Anual Objetivo Objetivos Metas Meta Hoje Ontem Amanhã
Objetivos Área Áreas Prioridade Prioridades Pendências Pendência Erros Erro Achados Achado Nenhum Nenhuma Nada Todos Tudo
Seguimento Teste Testes Grátis Gatilho Regra Regras Sessão Extra Extraordinária Pedido Pedidos Lista Listas
R O A Os As E Em No Na Nos Nas Do Da De Um Uma Com Para Por Até Se Só Já Mais Menos Não Sim Sobre Entre Desde Após
'''.split())
SENSIVEL = re.compile(r'(segur|webhook|token|senha|chave|segredo|permiss|vps|servidor|hostinger|ssh|patch|backup|porta|\.env|'
                      r'telefone|celular|chip|n[uú]mero|whats|sms|cpf|cnpj|\[|@|\\|/home|/workspace|cart[aã]o|'
                      r'\d{4,5}-\d{4}|\(\d{2}\)|\b(?=[0-9a-f]*\d)(?=[0-9a-f]*[a-f])[0-9a-f]{7,8}\b)', re.I)
RX_PALAVRA = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ][\w'’&.-]*")

def _trecho_ok(t):
    if SENSIVEL.search(t): return False
    for w in RX_PALAVRA.findall(t):
        w = w.strip(".-'’")
        if not w or not w[0].isupper(): continue
        if re.match(r'^[A-Z]{1,3}-\d', w): continue          # T-061, D-020, C-004, V-01, E-013
        if w in PERMITIDAS or w.capitalize() in PERMITIDAS: continue
        REJEITADAS[w] = REJEITADAS.get(w, 0) + 1
        return False
    return True

def _partes(t):
    """Divide em orações por '; ', '. ', ' — ' e quebra de linha, só fora de parênteses."""
    out, buf, prof, i = [], '', 0, 0
    while i < len(t):
        ch = t[i]
        if ch == '(': prof += 1
        elif ch == ')': prof = max(0, prof - 1)
        if prof == 0 and (ch == '\n' or (ch in ';.' and t[i + 1:i + 2] == ' ') or t.startswith(' — ', i) or t.startswith(' | ', i)):
            out.append(buf); buf = ''; i += 3 if t.startswith((' — ', ' | '), i) else 1; continue
        buf += ch; i += 1
    out.append(buf)
    return [p.strip(' -–:;,.') for p in out]

REJEITADAS = {}
def frase(texto, limpar, maximo=120):
    """Primeira(s) oração(ões) publicáveis do texto; '' se nada passar no filtro de privacidade."""
    t = re.sub(r'\*\*|__|`', '', texto or '')
    t = re.sub(r'\s*\((?![^)]*\d)[^)]*\)', '', t)            # parênteses sem número (em geral nomes)
    out = []
    for p in _partes(t):
        if not p or p.count('(') != p.count(')') or len(re.findall(r'[A-Za-zÀ-ÿ]{2,}', p)) < 2: continue
        if not _trecho_ok(p):
            if out: break
            continue
        out.append(p)
        if len('; '.join(out)) >= maximo * 0.6: break
    s = limpar('; '.join(out), maximo) if out else ''
    return s if s and _trecho_ok(s) else ''

# ------------------------------------------------------------------ util
def _ler(c):
    try: return open(c, encoding='utf-8').read()
    except Exception: return None

def _quando(dia, hora=None):
    return dia.isoformat() + (' ' + hora if hora else '')

def _br(q):
    """'2026-10-26 08:40' → '26/10/2026 08:40'."""
    if not q: return ''
    try:
        d = dt.date.fromisoformat(q[:10]).strftime('%d/%m/%Y')
        return d + (' ' + q[11:16] if len(q) > 11 else '')
    except Exception:
        return q

def _num(s):
    s = (s or '').replace('−', '-').replace('R$', '').replace(' ', '')
    m = re.search(r'-?\d[\d.]*(,\d+)?', s)
    if not m: return None
    v = m.group(0).replace('.', '').replace(',', '.')
    try: return float(v) if '.' in v else int(v)
    except ValueError: return None

def _dia(ddmm, ano, ref):
    try:
        d, m = [int(x) for x in ddmm.split('/')[:2]]
        x = dt.date(ano, m, d)
        if x > ref + dt.timedelta(days=1): x = dt.date(ano - 1, m, d)
        return x
    except Exception:
        return None

def _hora(s):
    m = re.search(r'~\s*(\d{1,2})[:h](\d{2})', s) or re.search(r'\b(\d{1,2}):(\d{2})\b', s)
    return f'{int(m.group(1)):02d}:{m.group(2)}' if m else None

def _cargo_arquivo(suf):
    base = suf.split('-')[0].upper()
    rot = {'CS': 'CS/CCO'}.get(base, base)
    resto = suf[len(base):].strip('-')
    return rot + (f' ({resto})' if resto else '')

# ------------------------------------------------------------------ extração automática de indicadores
def extrair_abriu(local, agora):
    """Do consolidado mais recente do CEO (resumos-clevels/*-ceo.md)."""
    out = {}
    rc = os.path.join(local, 'resumos-clevels')
    if not os.path.isdir(rc): return out
    arqs = sorted(f for f in os.listdir(rc) if re.match(r'\d{4}-\d{2}-\d{2}-ceo\.md$', f))
    if not arqs: return out
    f = arqs[-1]; t = _ler(os.path.join(rc, f)) or ''
    dia = dt.date.fromisoformat(f[:10]); hora = _hora(t.splitlines()[0] if t else '')
    q = _quando(dia, hora); fonte = f'resumo do CEO de {dia.strftime("%d/%m")} (resumos-clevels)'
    m = re.search(r'Amostras \(Port[aã]o 1\):\s*(\d+)\s*÷\s*(\d+)', t)
    if m:
        out['amostras'] = {'resultado': {'texto': m.group(1), 'num': int(m.group(1)), 'medido_em': q, 'fonte': fonte},
                           'meta_num': int(m.group(2))}
    m = re.search(r'Pagantes\s+(\d+),\s*receita\s+(R\$\s?[\d.,]+)', t)
    if m:
        out['pagantes'] = {'resultado': {'texto': m.group(1), 'num': int(m.group(1)), 'medido_em': q, 'fonte': fonte}}
    m = re.search(r'Lucro do m[eê]s vs R\$\s?[\d.,]+:\s*([−-]?\s?R\$\s?[\d.,]+?)\s*\((\w+)\s+(\d{1,2}/\d{1,2})\s*(\d{1,2}:\d{2})?', t)
    if m:
        d2 = _dia(m.group(3), dia.year, dia) or dia
        out['lucro'] = {'resultado': {'texto': m.group(1).replace('-', '−').replace(' ', '') .replace('R$', 'R$ '),
                                      'num': _num(m.group(1)), 'medido_em': _quando(d2, m.group(4)),
                                      'fonte': f'{m.group(2)} {m.group(3)}, citado no resumo do CEO de {dia.strftime("%d/%m")}'}}
    return out

def extrair_finbook(arquivo, agora):
    """Da última linha 'CEO resumo DD/MM enviado (~HH:MM BRT…): N venda; M visitas…' em ceo/diario.md."""
    out = {}
    t = arquivo('ceo/diario.md') or ''
    ult = None
    for m in re.finditer(r'CEO resumo (\d{1,2}/\d{1,2}) enviado \(~(\d{1,2}:\d{2}) BRT[^)]*\):\s*(\d+) vendas?;\s*(\d+) visitas[^;]*?7d(?: \(visitas\.py (\d{1,2}:\d{2})\))?', t):
        ult = m
    if ult:
        dia = _dia(ult.group(1), agora.year, agora.date())
        if dia:
            q = _quando(dia, ult.group(2)); fonte = f'resumo do CEO de {dia.strftime("%d/%m")} (ceo/diario.md)'
            v = int(ult.group(3))
            out['vendas-out'] = {'resultado': {'texto': str(v), 'num': v, 'medido_em': q, 'fonte': fonte}}
            out['vendas-nov'] = {'resultado': {'texto': str(v), 'num': v, 'medido_em': q, 'fonte': fonte}}
            vis = int(ult.group(4))
            out['visitas-7d'] = {'resultado': {'texto': str(vis), 'num': vis, 'medido_em': _quando(dia, ult.group(5) or ult.group(2)),
                                               'fonte': f'resumo do CEO de {dia.strftime("%d/%m")} (visitas.py)'}}
    return out

def extrair_patentsonar(local, agora):
    """Indicadores do PatentSonar na tabela de KPIs do meta-mensal.md (pasta local dos C-levels)."""
    out = {}
    t = _ler(os.path.join(local, 'meta-mensal.md')) or ''
    snaps = re.findall(r'^###\s+Snapshot\s+(\d{1,2}/\d{1,2})/(\d{4})', t, re.M)
    dia_snap = None
    if snaps:
        try: dia_snap = dt.date(int(snaps[-1][1]), int(snaps[-1][0].split('/')[1]), int(snaps[-1][0].split('/')[0]))
        except Exception: dia_snap = None
    m = re.search(r'\|\s*E-mails de 1º contato[^|]*\|[^|]*\|[^|]*?\*\*(\d+)\s+em\s+(\d{1,2}/\d{1,2})\*\*', t)
    if m:
        d = _dia(m.group(2), agora.year, agora.date())
        if d: out['contatos'] = {'resultado': {'texto': m.group(1), 'num': int(m.group(1)), 'medido_em': _quando(d), 'fonte': f'contagem do COO de {d.strftime("%d/%m")} (meta-mensal.md)'}}
    m = re.search(r'\|\s*Taxa de resposta[^|]*\|[^|]*\|\s*(\d+)\s*/\s*(\d+)\s*\(([\d,]+)\s*%\)', t)
    if m and dia_snap:
        out['resposta'] = {'resultado': {'texto': f'{m.group(1)} de {m.group(2)} ({m.group(3)} %)', 'num': _num(m.group(3)),
                                         'medido_em': _quando(dia_snap), 'fonte': f'meta-mensal.md do CEO, snapshot de {dia_snap.strftime("%d/%m")}'}}
    m = re.search(r'\|\s*Clientes pagantes[^|]*\|[^|]*\|\s*(\d+)\s*/\s*(US\$\s*[\d.,]+)', t)
    if m and dia_snap:
        out['pagantes'] = {'resultado': {'texto': m.group(1), 'num': int(m.group(1)), 'medido_em': _quando(dia_snap),
                                         'fonte': f'meta-mensal.md do CEO, snapshot de {dia_snap.strftime("%d/%m")} (MRR {m.group(2)})'}}
    return out

def extrair_vagas(arquivo, local, agora):
    out = {}
    hoje = agora.date()
    t = arquivo('registro-publicadas.csv')
    if t:
        datas = [l.get('data', '') for l in csv.DictReader(io.StringIO(t)) if l.get('data')]
        seg = hoje - dt.timedelta(days=hoje.weekday())
        n_sem = sum(1 for d in datas if d >= seg.isoformat())
        out['vagas-semana'] = {'resultado': {'texto': str(n_sem), 'num': n_sem, 'medido_em': agora.strftime('%Y-%m-%d %H:%M'),
                                             'fonte': f'registro-publicadas.csv (desde seg {seg.strftime("%d/%m")})'}}
        mes = hoje.strftime('%Y-%m')
        n_mes = sum(1 for d in datas if d.startswith(mes))
        out['vagas-mes'] = {'rotulo': f'Vagas publicadas em {MESES[hoje.month-1]}/{hoje.year}',
                            'resultado': {'texto': str(n_mes), 'num': n_mes, 'medido_em': agora.strftime('%Y-%m-%d %H:%M'),
                                          'fonte': 'registro-publicadas.csv'}}
    me = _ler(os.path.join(local, 'metricas.md')) or ''
    for l in me.splitlines():   # tabela com a linha mais recente primeiro
        m = re.match(r'\|\s*(\d{2}/\d{2}/\d{4})\s*\|\s*Instagram[^|]*\|\s*([\d.]+) visualiza[çc][õo]es[^|]*\|\s*(\d+) dias \(([^)]*)\)', l)
        if m:
            d = dt.datetime.strptime(m.group(1), '%d/%m/%Y').date()
            out['views-28d'] = {'rotulo': f'Visualizações no Instagram ({m.group(3)} dias)',
                                'resultado': {'texto': m.group(2), 'num': _num(m.group(2)), 'medido_em': d.isoformat(),
                                              'fonte': f'metricas.md (Meta Business Suite, {m.group(4)})'}}
            break
    di = _ler(os.path.join(local, 'diario.md')) or ''
    for m in re.finditer(r'^### (\d{1,2}/\d{1,2}) (\d{1,2}:\d{2}) — CEO[^\n]*\n(.*?)(?=^### |\Z)', di, re.M | re.S):
        r = re.search(r'receita (' + '|'.join(MESES_LONGOS) + r') R\$ ?([\d.,]+)', m.group(3))
        if r and MESES_LONGOS.index(r.group(1)) == hoje.month - 1:
            dia = _dia(m.group(1), hoje.year, hoje)
            out['receita-mes'] = {'resultado': {'texto': 'R$ ' + r.group(2), 'num': _num(r.group(2)), 'medido_em': _quando(dia, m.group(2)),
                                                'fonte': f'resumo do CEO de {dia.strftime("%d/%m")} (diario.md)'}}
            break   # diário: mais recente primeiro
    return out

# ------------------------------------------------------------------ histórico
def hist_abriu(local, limpar, desde):
    rc = os.path.join(local, 'resumos-clevels'); out = []
    if not os.path.isdir(rc): return None
    for f in sorted(os.listdir(rc)):
        m = re.match(r'(\d{4}-\d{2}-\d{2})-([\w-]+)\.md$', f)
        if not m: continue
        dia = dt.date.fromisoformat(m.group(1))
        if dia < desde - dt.timedelta(days=1): continue
        cargo = _cargo_arquivo(m.group(2)); t = _ler(os.path.join(rc, f)) or ''
        linhas = t.splitlines(); fonte = f'resumos-clevels/{f}'
        rodadas = [i for i, l in enumerate(linhas) if re.match(r'^## Rodada', l)]
        def corpo(i0, i1):
            for l in linhas[i0:i1]:
                s = l.strip()
                if not s or s.startswith('#') or re.match(r'^(Fontes?|Fonte)\b', s) or re.match(r'^\d\)\s*\w+$', s): continue
                s = re.sub(r'^[-*]\s*|^\d+[.)]\s*', '', s)
                s = re.sub(r'^(Feito|Status|Resumo|Resultado)\s*:\s*', '', s)
                r = frase(s, limpar)
                if r: return r
            return ''
        cab = linhas[0] if linhas else ''
        if not rodadas or _hora(cab):   # arquivo de uma rodada só, ou cabeçalho com hora antes das "Rodada"
            fim = rodadas[0] if rodadas else len(linhas)
            out.append({'dia': dia, 'hora': _hora(cab), 'cargo': cargo, 'resultado': corpo(1, fim), 'fonte': fonte})
        for k, i in enumerate(rodadas):
            h = linhas[i]; hora = _hora(h); d = dia
            m2 = re.search(r'\((\d{1,2})→\d{1,2}/\d{1,2}', h)
            if m2 or (hora and hora >= '23:00' and re.search(r'Rodada 00:00', h)): d = dia - dt.timedelta(days=1)
            fim = rodadas[k + 1] if k + 1 < len(rodadas) else len(linhas)
            out.append({'dia': d, 'hora': hora, 'cargo': cargo, 'resultado': corpo(i + 1, fim), 'fonte': fonte})
    return out

RX_CARGO_COMMIT = re.compile(r'^\s*(?:Diretoria\s+)?(CEO|COO|CCO|CISO|CSO|CMO|CFO|CLO|CTO)\b\s*', re.I)
def hist_finbook(paged, owner, limpar, desde, brt):
    out = []
    since = dt.datetime.combine(desde, dt.time(), brt).astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    for c in paged(f'repos/{owner}/finbook/commits?per_page=100&since={since}', 1000):
        msg = c['commit']['message'].splitlines()[0]
        m = RX_CARGO_COMMIT.match(msg)
        if not m: continue
        quando = dt.datetime.fromisoformat(c['commit']['committer']['date'].replace('Z', '+00:00')).astimezone(brt)
        resto = msg[m.end():]
        resto = re.sub(r'^[:\s]*((\d{1,2}/\d{1,2}|\d{1,2}:\d{2})[\s:,]*)*', '', resto)
        out.append({'dia': quando.date(), 'hora': quando.strftime('%H:%M'), 'cargo': m.group(1).upper(),
                    'resultado': frase(resto, limpar), 'fonte': f'commit {c["sha"][:7]} (finbook)'})
    return out

RX_ITEM_FILA = re.compile(r'^###\s+(COO-\d{4}-\d{2}-\d{2}-\d+)\s+—\s+(.+)$')
def hist_patentsonar(arquivo, local, limpar, desde, agora):
    """COO: cada item de docs/coo/fila.md (repo) vira uma linha na data/hora do pedido; CEO/CMO/CS/CSO/CTO: arquivos de resumos/ e snapshots do meta-mensal.md (pasta local)."""
    out = []
    t = arquivo('docs/coo/fila.md')
    if t is None: return None
    itens = re.split(r'(?m)^(?=### COO-)', t)[1:]
    runs = {}   # (dia, hora) → contagem por status: um registro por rodada do COO
    for it in itens:
        m = RX_ITEM_FILA.match(it.split('\n')[0])
        da = re.search(r'^- Data:\s*(\d{1,2})/(\d{1,2})/(\d{4})(?:\s+(\d{1,2}):(\d{2}))?', it, re.M)
        if not m or not da: continue
        st = re.search(r'^- Status:\s*([^\n]+)', it, re.M)
        st = (st.group(1).strip().lower() if st else '')
        k = 'feito' if st.startswith('feito') else 'em andamento' if st.startswith('em andamento') else 'travado' if st.startswith('travado') else 'aberto'
        dia = dt.date(int(da.group(3)), int(da.group(2)), int(da.group(1)))
        hora = f'{int(da.group(4)):02d}:{da.group(5)}' if da.group(4) else None
        c = runs.setdefault((dia, hora), {'feito': 0, 'em andamento': 0, 'travado': 0, 'aberto': 0}); c[k] += 1
    for (dia, hora), c in runs.items():
        n = sum(c.values())
        pl = {'feito': ('feito', 'feitos'), 'em andamento': ('em andamento', 'em andamento'), 'travado': ('travado', 'travados'), 'aberto': ('aberto', 'abertos')}
        det = ', '.join(f'{v} {pl[k][0 if v == 1 else 1]}' for k, v in c.items() if v)
        out.append({'dia': dia, 'hora': hora, 'cargo': 'COO',
                    'resultado': f'{n} pedido{'s' if n != 1 else ''} na fila do Claude (situação atual: {det})', 'fonte': 'docs/coo/fila.md (PatentSonar)'})
    # resumos dos demais C-levels (pasta local); só dos últimos dias
    rdir = os.path.join(local, 'resumos')
    if os.path.isdir(rdir):
        for f in sorted(os.listdir(rdir)):
            mm = re.match(r'^(ceo|cmo|cso|cto|cfo|clo|ciso|cs|cco)-(\d{4})-(\d{2})-(\d{2})(.*)\.md$', f)
            if not mm: continue
            dia = dt.date(int(mm.group(2)), int(mm.group(3)), int(mm.group(4)))
            txt = _ler(os.path.join(rdir, f)) or ''
            cab = txt.split('\n', 1)[0]
            corpo = ''
            for ln in txt.split('\n')[1:]:
                ln = ln.strip()
                if not ln or ln.startswith(('#', '-', '|', '>', '*', '`')): continue
                corpo = ln; break
            out.append({'dia': dia, 'hora': _hora(cab), 'cargo': _cargo_arquivo(mm.group(1) + mm.group(5)),
                        'resultado': frase(corpo, limpar), 'fonte': 'clevels/resumos (pasta local do PatentSonar)'})
    return out

def hist_vagas(local, limpar, hoje):
    t = _ler(os.path.join(local, 'diario.md'))
    if t is None: return None
    out = []
    for m in re.finditer(r'^### (\d{1,2}/\d{1,2}) (\d{1,2}:\d{2}) — ([^\n]+)\n(.*?)(?=^### |\Z)', t, re.M | re.S):
        rot = m.group(3).strip()
        c = re.match(r'(CEO|COO|CCO|CISO|CSO|CMO|CFO|CLO|CTO)\b\s*(.*)', rot)
        if c:
            extra = re.sub(r'\([^)]*\)|\d{1,2}/\d{1,2}', '', c.group(2)).strip(' ()')
            cargo = c.group(1) + (f' ({extra})' if extra and _trecho_ok(extra) else '')
        elif re.match(r'Sess[aã]o', rot):
            cargo = 'C-levels (sessão extraordinária)'
        else:
            continue   # decisões/mensagens do Rodrigo e notas da pasta não são rodadas de C-level
        dia = _dia(m.group(1), hoje.year, hoje)
        if not dia: continue
        corpo = re.sub(r'^(CEO|COO|CCO|CISO|CSO|CMO|CFO|CLO|CTO)\b[^\n]{0,25}?:\s+', '', m.group(4).strip())
        corpo = re.sub(r'^(Placar|Estratégia|Feito)\s*:\s*', '', corpo)
        out.append({'dia': dia, 'hora': m.group(2).zfill(5), 'cargo': cargo, 'resultado': frase(corpo, limpar),
                    'fonte': 'diario.md dos C-levels do Vagas SJDR'})
    return out

def hist_editallido(api, paged, owner, limpar, desde, brt):
    out, vistos = [], set()
    since = dt.datetime.combine(desde, dt.time(), brt).astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    for b in api(f'repos/{owner}/editallido/branches?per_page=100') or []:
        for c in paged(f'repos/{owner}/editallido/commits?sha={b["name"]}&path=decisoes&per_page=100&since={since}', 300):
            if c['sha'] in vistos: continue
            vistos.add(c['sha'])
            msg = c['commit']['message'].splitlines()[0]
            m = re.match(r'ADR (\d{4}):\s*(.*)', msg)
            if not m: continue
            det = api(f'repos/{owner}/editallido/commits/{c["sha"]}') or {}
            texto = ''
            for f in det.get('files', []):
                if f['filename'].startswith('decisoes/') and f['filename'][9:13] == m.group(1):
                    texto = '\n'.join(l[1:] for l in (f.get('patch') or '').splitlines() if l.startswith('+'))
            if not re.search(r'\bCEO\b', texto): continue   # só decisões tomadas pelo CEO
            quando = dt.datetime.fromisoformat(c['commit']['committer']['date'].replace('Z', '+00:00')).astimezone(brt)
            out.append({'dia': quando.date(), 'hora': quando.strftime('%H:%M'), 'cargo': 'CEO',
                        'resultado': frase(f'Decisão {m.group(1)}: ' + m.group(2), limpar),
                        'fonte': f'commit {c["sha"][:7]} (editallido, decisoes/{m.group(1)})'})
    return out

# ------------------------------------------------------------------ montagem
def _mais_novo(a, b):
    """Resultado com medido_em mais recente (b = extraído vence empate)."""
    if not a or a.get('texto') is None: return b or a
    if not b or b.get('texto') is None: return a
    return b if (b.get('medido_em') or '') >= (a.get('medido_em') or '') else a

def _pct(meta, res):
    try:
        if meta and meta.get('num') and res and res.get('num') is not None and meta['num'] > 0:
            return max(0, min(100, round(100 * res['num'] / meta['num'])))
    except Exception: pass
    return None

def montar(site, base_path, api, paged, arquivo_de, limpar, tirar_mencoes, minimo, agora, abriu_local, owner, log):
    brt = agora.tzinfo; hoje = agora.date(); desde = hoje - dt.timedelta(days=DIAS_HIST)
    base = json.load(open(base_path, encoding='utf-8'))
    try: ant = json.load(open(os.path.join(site, 'data/resumo.json'), encoding='utf-8'))
    except Exception: ant = {}
    nomes_min = {m['nome'].lower() for m in minimo} | {(m.get('repo') or '').lower() for m in minimo} - {''}
    ant_ind = {(e.get('nome'), i.get('id')): i for e in ant.get('empresas', []) for i in e.get('indicadores', [])}

    extr = {}
    for nome, f in (('abriuagora', lambda: extrair_abriu(abriu_local, agora)),
                    ('finbook', lambda: extrair_finbook(arquivo_de('finbook'), agora)),
                    ('PatentSonar', lambda: extrair_patentsonar(PATENT_LOCAL, agora)),
                    ('vagassjdr', lambda: extrair_vagas(arquivo_de('vagassjdr'), VAGAS_CLEVELS, agora))):
        try: extr[nome] = f()
        except Exception as ex: extr[nome] = {}; log.append(f'resumo: extração de {nome} falhou ({ex}); usando registro/anterior')

    por_nome = {e['nome']: e for e in base.get('empresas', [])}
    empresas = []
    for nome in base.get('ordem') or list(por_nome):
        m = next((x for x in minimo if x['nome'].lower() == nome.lower()), None)
        if m or nome.lower() in nomes_min:
            m = m or {'nome': nome}
            empresas.append({'nome': m['nome'], 'publico_minimo': True, 'site': m.get('site'),
                             'nota': 'Dados internos não publicados (modo público mínimo).'})
            continue
        e = por_nome.get(nome)
        if not e: continue
        ex = extr.get(e.get('repo'), {})
        inds = []
        for i in e.get('indicadores', []):
            i = json.loads(json.dumps(i)); x = ex.get(i['id'], {})
            if x.get('rotulo'): i['rotulo'] = x['rotulo']
            if x.get('meta_num') is not None and i.get('meta'): i['meta']['num'] = x['meta_num']
            i['resultado'] = _mais_novo(i.get('resultado'), x.get('resultado'))
            if not i['resultado'] or i['resultado'].get('texto') is None:
                velho = ant_ind.get((nome, i['id']), {}).get('resultado')
                if velho and velho.get('texto') is not None:
                    i['resultado'] = dict(velho, mantido=True); log.append(f'resumo: {nome}/{i["id"]} mantido do anterior')
            r = i.get('resultado') or {}
            r['medido_br'] = _br(r.get('medido_em'))
            i['pct'] = _pct(i.get('meta'), r)
            inds.append(i)
        emp = {'nome': nome, 'repo': e.get('repo'), 'slug': e.get('repo'), 'indicadores': inds}
        if e.get('site'): emp['site'] = e['site']
        empresas.append(tirar_mencoes(emp))

    # histórico
    novos, fontes = [], []
    for emp, f, desc in (
            ('Abriu Agora', lambda: hist_abriu(abriu_local, limpar, desde), 'Abriu Agora: resumos-clevels/ (pasta local da Abriu Agora)'),
            ('Finbook', lambda: hist_finbook(paged, owner, limpar, desde, brt), 'Finbook: commits das rotinas no repositório finbook'),
            ('Vagas SJDR', lambda: hist_vagas(VAGAS_CLEVELS, limpar, hoje), 'Vagas SJDR: diario.md dos C-levels (pasta local)'),
            ('PatentSonar', lambda: hist_patentsonar(arquivo_de('PatentSonar'), PATENT_LOCAL, limpar, desde, agora), 'PatentSonar: docs/coo/fila.md do repositório (itens do COO) + resumos dos C-levels em clevels/resumos (pasta local)'),
            ('Edital Lido', lambda: hist_editallido(api, paged, owner, limpar, desde, brt), 'Edital Lido: commits de decisões do CEO no repositório editallido')):
        if emp.lower() in nomes_min: continue
        try:
            r = f()
        except Exception as ex:
            r = None; log.append(f'resumo: histórico de {emp} falhou ({ex}); mantido do anterior')
        if r is None:
            log.append(f'resumo: fonte do histórico de {emp} ausente; mantido do anterior'); continue
        fontes.append(desc)
        for x in r:
            if x['dia'] < desde: continue
            novos.append({'quando': _quando(x['dia'], x.get('hora')), 'quando_br': _br(_quando(x['dia'], x.get('hora'))),
                          'empresa': emp, 'cargo': limpar(x['cargo'], 40), 'resultado': x.get('resultado') or '', 'fonte': x['fonte']})
    chave = lambda h: (h['empresa'], h['cargo'], h['quando'])
    tem = {chave(h) for h in novos}
    emps_novas = {h['empresa'] for h in novos}
    for h in ant.get('historico', []):
        if chave(h) in tem or h.get('empresa', '').lower() in nomes_min: continue
        if h['empresa'] in emps_novas and h['quando'][:10] >= desde.isoformat() and h.get('fonte', '').startswith(('resumos-clevels', 'diario.md', 'docs/coo', 'clevels/resumos')):
            continue   # fonte lida hoje: o que não veio foi apagado/renomeado na fonte
        if (h.get('quando') or '')[:10] >= desde.isoformat():
            novos.append(h)
    novos.sort(key=lambda h: h['quando'], reverse=True)
    novos = tirar_mencoes(novos[:MAX_HIST])
    novos = [h for h in novos if h.get('empresa') != '[omitido no painel público]']
    return {'titulo': 'Resumo das empresas', 'gerado_em': agora.strftime('%d/%m/%Y %H:%M') + ' (horário de Brasília)',
            'nota': 'Só meta x resultado, copiados dos arquivos de cada empresa; nada é estimado. "sem dado" = não medido; "meta não definida" = sem meta escrita.',
            'empresas': empresas, 'historico': novos, 'fontes_historico': fontes,
            'janela_historico_dias': DIAS_HIST}
