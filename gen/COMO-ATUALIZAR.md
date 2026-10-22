# Como atualizar o Painel de Controle

O site em https://ratbragaia.github.io/Painel-de-Controle/ é estático (GitHub Pages).
Os dados dos repositórios privados são coletados **no momento da geração** e
publicados em JSON; o navegador **não** chama a API do GitHub.

## Arquivos

| Caminho | Papel |
|---|---|
| `site/data/projetos.json` | Resumo diário (status, recente, próximos). Editado pela rotina diária. |
| `site/data/detalhes/<repo>.json` | Painel completo de cada projeto (commits, pendências, KPIs). |
| `site/data/detalhes/index.json` | Índice leve para a Visão geral. |
| `site/data/canais.json` | Canais de venda/aquisição de cada empresa (gerado; ver "Canais de venda" abaixo). |
| `gen/canais.py` + `gen/canais_base.json` | Coleta dos canais e registro de reserva do painel. |
| `site/index.html` + `site/assets/` | Casca do app (dropdown + cards). |
| `gen/update_YYYY-MM-DD.py` (históricos) | Atualiza `projetos.json` (e, no script antigo, regravava o HTML estático). |
| `gen/build_detalhes.py` | Coleta dados do GitHub e gera `data/detalhes/`. Também regrava `index.html` a partir de `gen/index_template.html`. |

O schema de `projetos.json` é estável: só **adicione** campos novos; não renomeie nem remova os existentes (`titulo`, `gerado_em`, `projetos[].nome/repo/objetivo/status/recente/proximos/atualizado/url/categoria`).

## Comando da rotina diária

Depois de editar `projetos.json` (via `update_YYYY-MM-DD.py` ou à mão):

O gerador agora fica versionado dentro do repositório, em `gen/` (ver `gen/README.md`):

```bash
cd /workspace/painel/site && git pull && python3 gen/build_detalhes.py && git add -A && git commit -m "Atualização diária DD/MM/AAAA" && git push origin main
```

Isso atualiza `data/detalhes/` e `index.html`, mantendo KPIs/pendências/commits do
arquivo anterior quando a coleta nova vier vazia.

Autenticação: o script usa `gh auth token` (ou `GH_TOKEN` / `GITHUB_TOKEN`).
Os KPIs da Abriu Agora leem `/workspace/abriuagora/` (objetivos.md, meta-mensal.md,
registro-ajustes.md, resumos-clevels/), configurável com `--abriu` ou `ABRIU_LOCAL`.
Se essa pasta não existir no ambiente, o card de indicadores é mantido do JSON anterior.

## Segurança (site público)

`build_detalhes.py` limpa e-mails, URLs, caminhos, IPs, CNPJ/CPF, telefones e
tokens antes de gravar o JSON. Pendências viram só títulos curtos. Não publique
corpos de e-mail, senhas, dados de cartão nem detalhes de segurança da VPS.

## Canais de venda (aba "Canais de venda")

O gerador também grava `data/canais.json` (todas as empresas) e acrescenta ao `index.json`
`canais_aquisicao_ativos`, `canais_total` e `canais_alerta` de cada projeto. O site mostra:

- no painel de cada projeto, o card **Canais de venda** (tabela: canal, tipo, status + motivo,
  alcance/visitas, cliques, leads, vendas, receita, período/medição e fonte);
- no seletor, a opção **Canais de venda (todas as empresas)** (`#canais`): comparação das empresas,
  contagem de canais ativos e **alerta quando a empresa tem só 1 canal de aquisição ativo**.

Ativo = status `ativo` ou `em teste`; canais do mesmo `grupo` (ex.: ondas do e-mail frio) contam uma vez.
O código fica em `gen/canais.py`; o registro de reserva do painel em `gen/canais_base.json`.

### De onde vêm os canais (o mais forte vence)

1. `gen/canais_base.json` — registro de reserva mantido no painel (números com data e fonte).
2. `data/canais.json` anterior — rede de segurança: número que não veio hoje continua, com a nota
   **"mantido · medido em DD/MM/AAAA"**; canal que sumiu do registro continua como "mantido do registro anterior"
   (apague-o do `data/canais.json` se foi tirado de propósito).
3. Extração automática (todo dia): Abriu Agora `resumos-clevels/*-ceo.md` (pasta local);
   Finbook `ceo/diario.md` (placar do CEO), `ceo/financeiro.csv`, `ceo/envios/convite_parceiros.jsonl` (só a contagem);
   Vagas SJDR `registro-publicadas.csv` e `PLANO-VagasSJDR.md`.
4. Registro do CMO em Markdown (`CANAIS.md`, `canais.md` ou `canais-aquisicao.md`): status, motivo, hipótese, métrica e decisão.
5. `canais.json` do projeto (formato padrão abaixo): o mais forte, inclusive para os números.

Para cada número vale o de **data de medição mais recente**; empate → a fonte mais forte. Sem valor = **"sem dado"**.
Nada é estimado pelo painel. Textos passam por `limpar()`; parênteses sem número (em geral nomes de contatos) são retirados.

Onde o gerador procura o registro de cada projeto: primeiro na pasta local (preferida, é a cópia de trabalho),
depois no repositório (qualquer pasta). Pastas locais: Abriu Agora `$ABRIU_LOCAL` (padrão `/workspace/abriuagora`),
Finbook `$FINBOOK_LOCAL` (padrão `/workspace/kit-mei-em-dia`).
Qualquer outro projeto com `canais.json` ou `CANAIS.md` no repositório entra sozinho na aba.

### Formato padrão do registro de canais (cada CMO mantém no repositório do projeto)

Arquivo `canais.json` na raiz (ou em `ceo/`, `cmo/`, `docs/`). Uma entrada por canal; campos sem valor podem ficar de fora ou `null`:

```json
{
  "atualizado_em": "2026-10-21",
  "canais": [
    {
      "canal": "E-mail frio a escritórios contábeis",
      "grupo": "E-mail frio",
      "tipo": "aquisição",
      "status": "ativo",
      "motivo": "",
      "inicio": "2026-10-13",
      "hipotese": "Contador sem cliente novo por indicação pede a amostra grátis.",
      "metrica": "pedidos de amostra ÷ e-mails entregues",
      "numeros": {
        "alcance":  {"valor": 86, "nota": "e-mails entregues"},
        "cliques":  {"valor": 0,  "nota": "visitas com origem de prospecção"},
        "leads":    {"valor": 0,  "nota": "pedidos de amostra"},
        "vendas":   0,
        "receita":  "R$ 0",
        "outros":   {"Descadastros": 1, "Spam": 0}
      },
      "periodo": "13/10 a 21/10/2026",
      "medido_em": "2026-10-21",
      "fonte": "metricas.md",
      "decisao": "manter até 31/10; veredito em 04/11 (manter / ampliar / encerrar)"
    }
  ]
}
```

- `tipo`: `aquisição` ou `venda`. `status`: `ativo`, `em teste`, `planejado`, `parado` ou `encerrado` (com `motivo`).
- `numeros`: as 5 colunas fixas (`alcance` = alcance/visitas/enviados, `cliques`, `leads`, `vendas`, `receita`) e `outros` livres.
  Cada número pode ser só o valor ou `{"valor", "nota", "medido_em"}`. Não medido = `null` (o site mostra "sem dado").
- Datas em `AAAA-MM-DD` ou `DD/MM/AAAA`. `id` (opcional) fixa o canal entre versões; sem ele, o nome do canal é a chave.

Alternativa em Markdown (`CANAIS.md`), para quem prefere tabela — o gerador lê qualquer tabela com coluna
**Canal** e uma de **Status/Estado/Situação/Veredito/Resultado**:

```markdown
| Canal | Tipo | Status | Início | Hipótese | Métrica | Resultado | Prazo | Veredito |
|---|---|---|---|---|---|---|---|---|
| E-mail frio a contadores | aquisição | ativo | 13/10/2026 | Contador pede a amostra grátis | amostras ÷ entregues | 86 entregues, 0 cliques, 0 amostras (21/10) | 31/10/2026 | — |
| Reddit | aquisição | encerrado: conta banida | 12/10/2026 | … | visitas UTM | 0 visitas | — | encerrar |
```

No Markdown os números das 5 colunas não são lidos da coluna Resultado (texto livre): eles vêm do `canais.json`,
da extração automática ou do registro do painel; o texto aparece como "Resultado (registro do CMO)" só nos canais
que não têm números estruturados. Para números confiáveis no painel, use o `canais.json`.

**Projetos em modo público mínimo** (`gen/publico_minimo.json`, hoje: PatentSonar) não entram na aba de canais
nem têm painel: no site aparecem só nome + site. Não escreva status, números, prospects nem resumos deles no
`data/projetos.json`, nos `gen/update_*.py` ou em qualquer arquivo deste repositório (veja `gen/README.md`).

**Não publicar** no registro: e-mails, telefones, nomes de contatos/prospects, tokens, caminhos do Windows, CNPJ/CPF
nem corpo de e-mail. O painel limpa o que reconhece, mas o site é público.
