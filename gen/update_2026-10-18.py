#!/usr/bin/env python3
"""Atualização diária 18/10/2026 — só data/projetos.json (build_detalhes regenera o resto)."""
import json

path = "/workspace/painel/site/data/projetos.json"
d = json.load(open(path, encoding="utf-8"))
P = {p["nome"]: p for p in d["projetos"]}
d["gerado_em"] = "18/10/2026 08:10 (horário de Brasília)"

# --- Abriu Agora ---
p = P["Abriu Agora"]
p["status"] = (
    "Em operação ativa: regra nova da pausa instalada (conta só devolução definitiva) e pausa retirada em 17/10; "
    "envio volta seg 19/10 09:30 com 20/dia (10 convites + 10 seguimentos). Home, página de obrigado e kit das redes "
    "abrem pela dor do cliente; métricas ganharam gastos por serviço e lucro do mês. Conta bancária no Asaas ainda pendente "
    "(cadastro pelo Rodrigo)."
)
p["recente"] = [
    "18/10 06:05 – página de obrigado e 'Sobre' do LinkedIn abrem pela dor; status do Asaas: tudo aprovado menos a conta bancária",
    "18/10 00:02 – gastos de Resend e Asaas lidos pela API; lucro negativo aparece como −R$",
    "17/10 18:03 – home abre pela dor (título e 'Para quem é'); gastos por serviço e seção Lucro do mês; ganchos e legendas dos 5 posts do Instagram",
    "17/10 12:05 – regra da pausa instalada e pausa retirada; atualização do servidor depende de acesso root",
] + p["recente"][:2]
p["proximos"] = [
    "Retomar o envio seg 19/10 09:30 (20/dia) e medir devolução e pedidos de amostra",
    "Rodrigo cadastrar a conta bancária no Asaas",
    "Atualizar pacotes do servidor (precisa de root); Portão 1: ~170 convites até 30/10",
]
p["atualizado"] = "18/10/2026 06:05"

# --- Finbook ---
p = P["Finbook"]
p["status"] = (
    "finbook.com.br no ar (site 200 nas checagens do COO); 0 vendas até 17/10 à noite, 81 visitas em 7 dias; "
    "Short 07 e Reddit não rodaram em 17/10 e passaram para 18/10; CISO achou 1 fragilidade sem vazamento "
    "(dependências da ferramenta de deploy); preço do Pacote Profissões (site R$ 17, Kiwify R$ 10) segue aguardando o Rodrigo; "
    "sanção do PLP 186 pendente."
)
p["recente"] = [
    "17/10 22:55 – COO: site 200, 0 venda; Short 07 (T-003) e Reddit (T-004) atrasaram, novo prazo na 1ª rodada de 18/10",
    "17/10 20:23 – CEO resumo: 0 vendas, 81 visitas/7d, 0 inscritos, nada aguardando aprovação",
    "17/10 – CCO (09:40 e 15:48): 0 venda, cliente ou parceiro novo",
    "17/10 09:04 – CISO: varredura sem segredos expostos; 6 avisos altos nas dependências do deploy local (tarefa T-013)",
] + p["recente"][:2]
p["proximos"] = [
    "Publicar Short 07 e retomar o Reddit (1 por dia, sem links) em 18/10",
    "Rodrigo decidir o preço do Pacote Profissões (T-011)",
    "CTO atualizar as dependências do deploy (T-013); acompanhar a sanção do PLP 186 (prazo 06/11)",
]
p["atualizado"] = "17/10/2026 22:55"

# --- Vagas SJDR ---
p = P["Vagas SJDR"]
p["status"] = (
    "Coleta ativa: em 17/10 três vagas novas por stories (2 publicadas sozinhas, 1 enviada para aprovação). "
    "Pendente: arquivar 2 fluxos temporários no n8n (aguardando ok escrito). Sem README."
)
p["recente"] = [
    "17/10 17:35 – 3 vagas de 17/10 (SJDR e Tiradentes): 2 publicadas automaticamente, 1 aguardando aprovação",
] + p["recente"][:3]
p["atualizado"] = "17/10/2026 17:35"

# --- Milhas e Cartões ---
p = P["Milhas e Cartões"]
p["status"] = (
    "Em operação: radar diário de 17/10 sem promoção aplicável (nenhuma transferência bonificada Livelo para "
    "Azul, Smiles ou Latam); vigiando o aniversário da Smiles em 18/10 e o bônus Nubank Ultravioleta."
)
p["recente"] = [
    "17/10 08:17 – radar diário: nada aplicável; Smiles 315% só para assinante do clube; cartões de adesão reprovados pela anuidade",
] + p["recente"][:2]
p["proximos"] = [
    "Conferir campanha do aniversário da Smiles (18/10) e bônus Nubank Ultravioleta → Azul/Smiles",
] + [x for x in p["proximos"] if "Revisão mensal" in x or "saldos" in x]
p["atualizado"] = "17/10/2026 08:17"

json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok")
