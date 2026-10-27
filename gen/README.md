# gen/ — gerador dos painéis por projeto

`build_detalhes.py` lê `data/projetos.json`, consulta a API do GitHub (só leitura) para
cada projeto com repositório e grava:

- `data/detalhes/<repo>.json` — painel do projeto (`repo`, `slug`, `estatisticas`, `commits`,
  `pendencias`, `kpis`, `gerado_em`);
- `data/detalhes/index.json` — resumo leve para a Visão geral;
- `data/canais.json` — canais de venda e aquisição de cada empresa (aba "Canais de venda"; código em `gen/canais.py`,
  registro de reserva em `gen/canais_base.json`, formato padrão em `COMO-ATUALIZAR.md`);
- `index.html` — regravado a partir de `gen/index_template.html` (use `--sem-index` para não mexer).

## Como rodar

De dentro do repositório (a pasta do site é, por padrão, a pasta-mãe de `gen/`):

```bash
cd /workspace/painel/site
python3 gen/build_detalhes.py
```

Rotina diária completa (uma linha):

```bash
cd /workspace/painel/site && git pull && python3 gen/build_detalhes.py && git add -A && git commit -m "Atualização diária DD/MM/AAAA" && git push origin main
```

`data/projetos.json` continua sendo editado pela rotina diária (à mão ou com um
`gen/update_AAAA-MM-DD.py`) **antes** de rodar o gerador. Os `update_2026-10-1x.py` são
históricos e usam caminhos absolutos de `/workspace/painel/site`.

## Opções

| Opção / variável | Padrão | Para quê |
|---|---|---|
| `--site PASTA` | pasta-mãe de `gen/` | onde estão `data/` e `index.html` |
| `--abriu PASTA` ou `ABRIU_LOCAL=PASTA` | `/workspace/abriuagora` | arquivos locais da Abriu Agora (`objetivos.md`, `meta-mensal.md`, `registro-ajustes.md`, `resumos-clevels/`) — não estão no repositório do GitHub |
| `--sem-index` | — | não regravar `index.html` |
| `PATENT_LOCAL=PASTA` | `/workspace/patentsonar/clevels` | registro de canais, `meta-mensal.md` e resumos locais do PatentSonar |
| `FINBOOK_LOCAL=PASTA` | `/workspace/kit-mei-em-dia` | cópia local do Finbook (`ceo/canais.md`) |
| `GH_TOKEN` / `GITHUB_TOKEN` | `gh auth token` | autenticação no GitHub |

## Rede de segurança (nada some do painel)

Antes de gravar cada `data/detalhes/<repo>.json`, o script lê o arquivo anterior e mantém:

- o bloco `kpis` inteiro, se a coleta nova vier nula/vazia (ex.: pasta da Abriu Agora ausente);
- cada número (`numeros[].rotulo`), tabela ou lista de KPI que sumiu ou veio vazio
  (ex.: "Ajustes dos C-levels em aberto", "Resumos de C-levels", "Ajustes em aberto");
  "Meta de Out/2026" e "Meta de Nov/2026" contam como o mesmo indicador;
- `pendencias`, se a fonte não for encontrada (`null`), e `commits`, se a lista vier vazia;
- em `data/canais.json`, cada número de canal que não veio na coleta (nota "mantido · medido em …"), o status lido
  do registro do CMO quando o registro some, e canais inteiros que sumiram do registro.

Tudo o que for mantido aparece no terminal como `mantido em <repo>: …`. Se um projeto falhar,
o `.json` anterior fica no lugar e a entrada antiga do `index.json` é reaproveitada (o script sai com código 1).

Atenção: uma lista que fica vazia de verdade (ex.: zero ajustes em aberto) também volta do
arquivo anterior. Nesse caso, apague o item do JSON anterior antes de rodar.

## Modo público mínimo (`gen/publico_minimo.json`)

A lista está **vazia** desde 26/10/2026 (Rodrigo liberou tudo, inclusive o PatentSonar). O mecanismo continua disponível:
projetos listados aparecem no site **só com nome + site**; o gerador reescreve a entrada em `data/projetos.json`, não consulta o
GitHub, apaga `data/detalhes/<repo>.json`, não gera canais, troca por "[omitido no painel público]" textos de outros projetos que citem
o nome e (se a lista voltar a ter itens) remove de `gen/update_*.py` os blocos `p = P["<projeto>"]`.

## Dashboard resumido (`gen/resumo.py`)

Gera `data/resumo.json` (abas meta x resultado + histórico dos C-levels) a partir de `gen/resumo_base.json` e das fontes locais/GitHub.
Variáveis: `VAGAS_CLEVELS` (padrão `/workspace/clevels/vagas-sjdr`), `PATENT_LOCAL` (padrão `/workspace/patentsonar/clevels`), `ABRIU_LOCAL`.
Detalhes e regras de privacidade em `gen/COMO-ATUALIZAR.md`.

## Segurança (site público)

`limpar()` remove e-mails, links, caminhos, IPs, CNPJ/CPF, telefones e tokens; pendências
viram só títulos curtos; itens técnicos/de segurança da Abriu Agora aparecem genéricos.
Não publique corpos de e-mail, senhas, dados de cartão nem detalhes da VPS.
Veja também `COMO-ATUALIZAR.md`.
