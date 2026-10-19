#!/usr/bin/env python3
"""Atualização diária 19/10/2026 — só data/projetos.json (build_detalhes regenera o resto)."""
import json

path = "/workspace/painel/site/data/projetos.json"
d = json.load(open(path, encoding="utf-8"))
P = {p["nome"]: p for p in d["projetos"]}
d["gerado_em"] = "19/10/2026 08:10 (horário de Brasília)"

# --- Abriu Agora ---
p = P["Abriu Agora"]
p["status"] = (
    "Em operação ativa: envio volta hoje (seg 19/10) às 09:30 com 20/dia (10 convites + 10 seguimentos), com a regra nova da pausa "
    "(conta só devolução definitiva). Em 18/10 páginas por cidade, índice de conteúdo e posts da semana passaram a abrir pela dor do cliente; "
    "cobrança ganhou troca de data (recorte até o dia 5) e alerta de assinatura pendente há mais de 7 dias. Conta bancária no Asaas ainda pendente "
    "(cadastro pelo Rodrigo)."
)
p["recente"] = [
    "19/10 00:06 – cobrança: troca de data (recorte até o dia 5) e alerta de assinatura pendente há mais de 7 dias",
    "18/10 18:07 – páginas por cidade, índice de /conteudo e posts da semana abrem pela dor; preço de fundador até 31/12",
    "18/10 06:05 – página de obrigado e 'Sobre' do LinkedIn abrem pela dor; status do Asaas: tudo aprovado menos a conta bancária",
    "18/10 00:02 – gastos de Resend e Asaas lidos pela API; lucro negativo aparece como −R$",
] + p["recente"][2:4]
p["proximos"] = [
    "Retomar o envio hoje 19/10 09:30 (20/dia) e medir devolução e pedidos de amostra",
    "Rodrigo cadastrar a conta bancária no Asaas",
    "Atualizar pacotes do servidor (precisa de root); Portão 1: ~170 convites até 30/10",
]
p["atualizado"] = "19/10/2026 00:06"

# --- PatentSonar ---
p = P["PatentSonar"]
p["status"] = (
    "Em operação: em 19/10 a abordagem pela dor do cliente entrou em todo o funil (e-mails, home, 6 páginas de tecnologia, relatório de agosto) "
    "e a maior parte da fila do COO de 16/10 foi marcada feita; site com nota 12/12 no crítico, 300 impressões e 1 clique na busca (problema é tráfego, "
    "não conversão); 7 contatos FR importados para a semana 43 e 3 primeiros contatos novos na fila; resumos de uma página preparados para um 'sim' recebido em 19/10."
)
p["recente"] = [
    "19/10 07:15 – resumos de uma página para o 'sim' do primeiro contato v2 (19, 49 e 31 famílias de patentes; gancho corrigido antes do envio)",
    "19/10 05:25 – crescimento: site 12/12, e-mails pela dor (templates 8→11), semana 43 com 7 contatos FR e 3 primeiros contatos na fila; pedidos do COO -01 a -05, -07, -08, -10, -11 feitos",
    "19/10 05:09 – e-mails de amostra/teste, home e 6 páginas de tecnologia abrem pela dor; modelos v1 aposentados com trava no envio",
    "19/10 05:06 – documentos de dor e voz do cliente (citações checadas na fonte), críticos pontuam a dor, first_touch_v2/follow_up_v2",
    "19/10 04:12 – ingestão do BigQuery passa a seguir a atualização real da base pública",
    "16/10 16:10 – relatório semanal: MRR US$ 0, 52 e-mails frios desde 01/10 com 0 respostas humanas",
]
p["proximos"] = [
    "Enviar os 3 primeiros contatos novos da semana 43 e responder o 'sim' com os resumos",
    "Medir o lote de e-mails v2 em 22/10",
    "Atacar a falta de tráfego (300 impressões, 1 clique); pedidos restantes da fila do COO",
]
p["atualizado"] = "19/10/2026 07:15"

# --- Finbook ---
p = P["Finbook"]
p["status"] = (
    "finbook.com.br no ar (site 200 em todas as checagens do COO de 18/10); 0 vendas, 75 visitas em 7 dias (CEO 18/10). "
    "Short 07 público no YouTube e no TikTok em 18/10; Reddit travou (sem pergunta adequada em 7 dias e 2 comentários antigos removidos pelo filtro) "
    "e aguarda decisão do CMO; PLP 186 ainda sem sanção (prazo 06/11); decisões pendentes do Rodrigo: preço do Pacote Profissões (T-011) e T-009."
)
p["recente"] = [
    "18/10 22:52 – COO: site 200, rodada noturna, fila sem itens executáveis",
    "18/10 20:24 – CEO resumo: 0 vendas, 75 visitas/7d, 0 inscritos; feito Short 07; travou Reddit",
    "18/10 12:57 – Short 07 público no TikTok (YouTube já estava desde 17/10)",
    "18/10 10:50 – COO: Reddit travou (sem post adequado e 2 comentários removidos); CMO decide se segue ou pausa",
    "18/10 – CISO: varredura sem achados novos; CCO: 0 venda, cliente ou parceiro",
] + p["recente"][:1]
p["proximos"] = [
    "CMO decidir se o Reddit segue ou pausa (T-004)",
    "Rodrigo decidir o preço do Pacote Profissões (T-011) e a T-009",
    "CTO atualizar as dependências do deploy (T-013); acompanhar a sanção do PLP 186 (prazo 06/11)",
]
p["atualizado"] = "18/10/2026 22:52"

# --- Vagas SJDR ---
p = P["Vagas SJDR"]
p["status"] = (
    "Coleta ativa: em 18/10 quatro vagas novas por stories (SJDR e Tiradentes), todas publicadas sozinhas; a rotina ganhou um passo para religar "
    "o Chrome depois de uma falha às 17h. Pendente: arquivar 2 fluxos temporários no n8n (aguardando ok escrito). Sem README."
)
p["recente"] = [
    "18/10 18:36 – 4 vagas de 18/10 (SJDR e Tiradentes) publicadas automaticamente",
    "18/10 – rotina diária: passo novo para religar o Chrome e esperar até 5 min antes de avisar",
] + p["recente"][:3]
p["atualizado"] = "18/10/2026 18:36"

# --- Milhas e Cartões ---
p = P["Milhas e Cartões"]
p["status"] = (
    "Em operação: radar de 18/10 sem promoção aplicável (aniversário da Smiles sem campanha de transferência); auditoria mensal dos cartões feita em 18/10 "
    "(fim do seguro grátis do Ultravioleta, versão paga não recomendada; rendimento do OKX corrigido para ~3,5% a.a.). Vigiando bônus Nubank → Azul/Smiles de 20 a 24/10."
)
p["recente"] = [
    "18/10 – auditoria mensal dos cartões: fim do seguro grátis do Ultravioleta, teto de cashback do OKX confirmado, prévia do XP Legacy",
    "18/10 – radar diário: nada aplicável; aniversário da Smiles sem campanha de transferência",
] + p["recente"][:2]
p["proximos"] = [
    "Vigiar bônus Nubank Ultravioleta → Azul/Smiles de 20 a 24/10",
] + [x for x in p["proximos"] if "saldos" in x or "Revisão mensal" in x]
p["atualizado"] = "18/10/2026 10:35"

json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok")
