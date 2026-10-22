#!/usr/bin/env python3
"""Atualização diária 20/10/2026 — só data/projetos.json (build_detalhes regenera o resto)."""
import json

path = "/workspace/painel/site/data/projetos.json"
d = json.load(open(path, encoding="utf-8"))
P = {p["nome"]: p for p in d["projetos"]}
d["gerado_em"] = "20/10/2026 08:10 (horário de Brasília)"

# --- Abriu Agora ---
p = P["Abriu Agora"]
p["status"] = (
    "Em operação ativa: envio voltou em 19/10 (20 e-mails, 19 entregues, 1 devolvido por caixa cheia, sem PAUSA); "
    "onda 2 pronta para hoje 20/10 09:30 com o assunto B (10 convites + 10 seguimentos, abrindo pela dor). "
    "Relatório semanal 12–18/10: 60 convites, 0 aberturas registradas, 0 pedidos de amostra, 0 assinantes. "
    "Em 20/10 a home e /para-contadores foram redesenhadas (amostra grátis no topo, faixa com o número do mês, print da planilha, menu no celular). "
    "Conta bancária no Asaas ainda pendente (cadastro pelo Rodrigo)."
)
p["recente"] = [
    "20/10 00:08 – home e /para-contadores redesenhadas: formulário de amostra no topo, faixa com 6.573 empresas abertas em agosto nas 19 cidades, print da planilha, menu no celular",
    "19/10 18:12 – métricas com visitas por origem; teste do espelho corrigido (CI voltou a passar)",
    "19/10 12:17 – servidor atualizado, teste de amostra entregue em 4,6 min (meta até 10); onda 2 pronta para 20/10",
    "19/10 09:36 – relatório semanal 12–18/10 (60 convites, 0 pedidos de amostra) e envio de 19/10: 19 de 20 entregues",
    "19/10 00:06 – cobrança: troca de data (recorte até o dia 5) e alerta de assinatura pendente há mais de 7 dias",
    "18/10 18:07 – páginas por cidade, índice de /conteudo e posts da semana abrem pela dor; preço de fundador até 31/12",
]
p["proximos"] = [
    "Ligar a onda 2 hoje 20/10 09:30 (assunto B) e conferir a onda 3 pela regra (≥ 1 pedido de lead e sem PAUSA)",
    "Medir devolução e pedidos de amostra com a home nova",
    "Rodrigo cadastrar a conta bancária no Asaas; Portão 1: ~170 convites até 30/10",
]
p["atualizado"] = "20/10/2026 00:08"

# PatentSonar: modo público mínimo (gen/publico_minimo.json) — bloco removido em 22/10/2026

# --- Finbook ---
p = P["Finbook"]
p["status"] = (
    "finbook.com.br no ar (site 200 em todas as checagens do COO de 19/10); 0 vendas (meta: 1ª até 31/10), 110 visualizações em 7 dias, 0 clique em comprar, 0 lead (CEO 19/10). "
    "Home redesenhada em 19/10 pelo CMO (dor no topo, calculadora como destaque, Kit só depois do resultado); rastreio UTM provado ponta a ponta; "
    "post 08 publicado no Facebook; Short 08 aprovado para 21/10; Reddit pausado até o CMO decidir. PLP 186 ainda sem sanção (prazo 06/11). "
    "Decisões pendentes do Rodrigo: preço do Pacote Profissões (T-011) e T-009."
)
p["recente"] = [
    "19/10 22:55 – COO: site 200, fila sem itens executáveis",
    "19/10 20:21 – CEO resumo: 0 vendas, 110 visualizações/7d, 0 clique em comprar, 0 lead",
    "19/10 19:21 – CMO/COO: home nova com a dor no topo e a calculadora como destaque (~470 palavras); CMO dono do design",
    "19/10 14:58 – página GEO estourou o limite do deploy (T-019); bio do TikTok conferida",
    "19/10 11:35 – rastreio UTM ok ponta a ponta, post 08 no Facebook, Short 08 aprovado (publica 21/10)",
    "19/10 08:44 – CEO: Reddit pausado até o CMO; CISO: varredura sem achados novos",
]
p["proximos"] = [
    "Publicar o Short 08 em 21/10 e soltar o lote 5 (T-008)",
    "Rodrigo decidir o preço do Pacote Profissões (T-011) e a T-009",
    "Resolver a página GEO acima do limite (T-019); acompanhar a sanção do PLP 186 (prazo 06/11)",
]
p["atualizado"] = "19/10/2026 22:55"

# --- Vagas SJDR ---
p = P["Vagas SJDR"]
p["status"] = (
    "Coleta ativa: em 19/10 oito vagas novas por stories (SJDR e Tiradentes), sete publicadas sozinhas e uma aguardando aprovação; "
    "script para religar o Chrome versionado. Pendente: arquivar 2 fluxos temporários no n8n (aguardando ok escrito). Sem README."
)
p["recente"] = [
    "19/10 17:35 – 8 vagas de 19/10 (SJDR e Tiradentes): 7 publicadas automaticamente, 1 aguardando aprovação",
    "19/10 – script para religar o Chrome adicionado ao repositório",
] + p["recente"][:3]
p["atualizado"] = "19/10/2026 17:35"

# --- Milhas e Cartões ---
p = P["Milhas e Cartões"]
p["status"] = (
    "Em operação: radar de 19/10 sem promoção aplicável (bônus Azul de Inter/BV/C6 e Qatar Avios +60% descartados com a conta feita). "
    "Vigiando bônus Nubank Ultravioleta → Azul/Smiles de 20 a 24/10, ainda sem anúncio em 2026. Saldos na planilha seguem desatualizados."
)
p["recente"] = [
    "19/10 – radar diário: nada aplicável; Livelo sem transferência bonificada, Qatar Avios +60% acima do teto",
] + p["recente"][:3]
p["atualizado"] = "19/10/2026 10:35"

# --- Assistente Pessoal ---
p = P["Assistente Pessoal"]
p["status"] = (
    "Versionado no GitHub e espelhado de hora em hora. Em 19/10 o modelo de funções C-Level foi atualizado: o CMO passou a cuidar também do design "
    "e da conversão das páginas públicas."
)
p["recente"] = [
    "19/10 20:36 – Funcoes-C-Level: CMO dono do design e da conversão das páginas públicas",
] + p["recente"][:2]
p["atualizado"] = "19/10/2026 20:36"

json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok")
