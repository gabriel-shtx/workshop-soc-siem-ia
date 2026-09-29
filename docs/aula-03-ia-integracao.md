# Aula 3 — IA e Integração

O dia em que o participante deixa de ser quem investiga e passa a ser **quem constrói o robô que faz a primeira triagem**. Fecha o arco: ver (aula 1) → investigar (aula 2) → automatizar (aula 3).

## Conteúdo

- **IA em segurança** — onde ela ajuda (resumir contexto, cruzar reputação, redigir recomendação) e onde **não** (detectar é o Wazuh; decidir ação irreversível é humano). A analogia: a IA é um estagiário brilhante — você confere antes de assinar.
- **O pipeline completo** — Wazuh → n8n → AbuseIPDB → Mistral Nemotron → Resend.
- **O gatilho** — a regra `100501` (força bruta SSH + login com sucesso), a integração no `ossec.conf` e a simulação com `logger`.
- **Enriquecer e analisar** — NORMALIZAR, consulta ao AbuseIPDB, a análise da IA (com prompt de saída em JSON estrito) e o Code node de parse.
- **Entregar** — o e-mail acionável via Resend.
- **Publicar** — transformar o laboratório em portfólio (GitHub + LinkedIn). Este repositório é o resultado.

## O que foi construído

Um **SOAR** funcional: um alerta entra numa ponta, um e-mail investigado sai na outra — com veredito, reputação do IP, ações imediatas e passos de investigação. Do zero, com ferramentas gratuitas.

## Artefatos

- Regra: [`wazuh/local_rules.xml`](../wazuh/local_rules.xml)
- Integração: [`wazuh/ossec-integration.md`](../wazuh/ossec-integration.md) · [`wazuh/custom-n8n.py`](../wazuh/custom-n8n.py)
- Simulação: [`scripts/simulate_wazuh_attack.sh`](../scripts/simulate_wazuh_attack.sh)
- Workflow, prompt e e-mail: [`n8n/`](../n8n/)
