#!/usr/bin/env python3
"""Atualização diária 16/10/2026 — só data/projetos.json (build_detalhes regenera o resto)."""
import json

path = "/workspace/painel/site/data/projetos.json"
d = json.load(open(path, encoding="utf-8"))
P = {p["nome"]: p for p in d["projetos"]}
d["gerado_em"] = "16/10/2026 08:10 (horário de Brasília)"

# --- Abriu Agora ---
p = P["Abriu Agora"]
p["status"] = (
    "Em operação ativa: prospecção por e-mail e /para-contadores passam a falar pela dor "
    "(produto depois); teto fixo de 20 convites/dia; Portão 1 ~170 convites até 30/10; "
    "pendência da importação Receita 2026-09 resolvida (PENDENCIAS vazia)."
)
p["recente"] = [
    "16/10 06:10 – prospecção e /para-contadores pela dor (produto depois); assuntos A/B e D+3/D+7 alinhados",
    "15/10 18:12 – importação Receita 2026-09 resolvida; PENDENCIAS.md sem itens abertos",
    "15/10 – CISO (permissões, security.txt), política de privacidade, docs de CS/onboarding; Portão 1 (~170 convites até 30/10)",
] + p["recente"][:2]
p["proximos"] = [
    "Disparar a onda 2 com o assunto B e medir pedidos de amostra",
    "Atualização/reinício da VPS planejado para 17/10 de madrugada",
    "Seguir o checklist e a RPI mensal",
]
p["atualizado"] = "16/10/2026 06:10"

# --- PatentSonar ---
p = P["PatentSonar"]
p["status"] = (
    "Em operação: C-levels no Grok com prospecção contínua; fila COO→Claude (docs/coo/fila.md) "
    "ativa após o merge do PR #5; crítico de e-mail com barra 10/12; checkout Paddle e segurança VPS ainda em plano."
)
p["recente"] = [
    "16/10 05:09 – pesquisa 15: 7 contatos FR preparados para a semana 43 (importação só em 19/10; semana 42 em 50/50)",
    "16/10 04:11 – crítico: caixas genéricas reprovam antes da nota; barra sobe para 10/12 (0 respostas humanas em 36 envios 01–08/10)",
    "15/10 23:23 – PR #5 mergeado: fila docs/coo/fila.md (pedidos do COO chegam ao Claude sem repasse do Rodrigo)",
] + p["recente"][:2]
p["proximos"] = [
    "Medir respostas dos contatos já enviados",
    "Importar a pesquisa 15 em 19/10 (semana 43)",
    "Executar os planos de checkout (Paddle) e de segurança da VPS",
]
p["atualizado"] = "16/10/2026 05:09"

# --- Finbook ---
p = P["Finbook"]
p["status"] = (
    "finbook.com.br no ar; 0 vendas até 16/10 de manhã; modelo C-level desde 15/10 à noite "
    "(meta: 1ª venda até 31/10, 10 até 30/11); Kit R$37 / Pacote Profissões R$17 / Combo R$47 na Kiwify; "
    "site atualizado após aprovação do PLP 186 no Senado (falta sanção)."
)
p["recente"] = [
    "15/10 ~23:30 – modelo C-level (organograma, metas, fila-coo); Pacote Profissões confirmado a R$17 na Kiwify",
    "15/10 ~20:45 – Senado aprovou PLP 186 (78 a 0); site, FB post-07 e Short 06 passam a 'falta a sanção'",
    "15/10 – Short 06 v5 (voz nativa pt-BR) pronto para publicar; artigo do limite R$110 mil no ar; 1ª resposta de parceiro (recusa)",
] + p["recente"][:2]
p["proximos"] = [
    "Publicar Short 06 e FB post-07 em 16/10 (diurno)",
    "Short 07 em 17/10; Reddit em 17/10",
    "Pin 4 do Pinterest depende do Rodrigo; convites a parceiros só como rascunho",
]
p["atualizado"] = "16/10/2026 08:10"

# --- Vagas SJDR ---
p = P["Vagas SJDR"]
p["status"] = (
    "Coleta ativa; PENDENCIAS revisadas em 16/10 (Afya publicada em 15/10; 5 stories de 13/10 publicados; "
    "chave da fila do Chrome/POST pago fora do git). Sem README."
)
p["recente"] = [
    "16/10 – limpeza aprovada pelo Rodrigo; PENDENCIAS atualizado (Afya 15/10, stories 13/10, chave da fila fora do git)",
    "16/10 – conferir mensagem a contatos antigos (número do dia); arquivar 2 fluxos TEMP no n8n (aguardando ok escrito)",
] + p["recente"][:2]
p["proximos"] = [
    "Conferir envio a contatos antigos (frase do número do dia)",
    "Arquivar os 2 fluxos TEMP do n8n após ok escrito",
    "Criar README",
]
p["atualizado"] = "16/10/2026 02:40"

# Espelhamentos sem mudança de conteúdo — só atualizado se quiser refletir o mirror.
# Assistente Pessoal / Redes Sociais / ytkit / editallido: só espelhamento automático — sem nova recente.

# Hub Rockfort permanece sem painel detalhado (fora do GitHub).
assert P["Hub Rockfort"].get("categoria", "").startswith("Fora")

ordem = [
    "Abriu Agora",
    "PatentSonar",
    "Finbook",
    "Vagas SJDR",
    "BlueBed",
    "Base de Conhecimento",
    "Editallido",
    "Milhas e Cartões",
    "Assistente Pessoal",
    "ytkit",
    "Redes Sociais",
    "Curso de IA",
    "Juventude Empreendedora",
    "Lígia Daher – site",
    "Carteira de Locação",
    "InfluNet",
    "Agente de Saúde",
    "Hub Rockfort",
]
assert set(ordem) == set(P), set(P) ^ set(ordem)
d["projetos"] = [P[n] for n in ordem]
json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok", d["gerado_em"], len(d["projetos"]))
