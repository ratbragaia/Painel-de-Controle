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
