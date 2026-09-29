# Aula 1 — Fundamentos

**SOC, SIEM e Wazuh.** O objetivo do dia é sair da teoria com um SIEM de verdade rodando e o primeiro evento coletado.

## Conteúdo

- **O que é um SOC** — pessoas, processos e tecnologia. A missão: detectar, analisar e responder antes que vire prejuízo.
- **O ecossistema** — SIEM, EDR, SOAR e Threat Intelligence, e onde o analista entra (N1/N2/N3).
- **Ativos críticos** — o primeiro passo de qualquer SOC é saber o que proteger. Não se protege o que não se conhece.
- **A cadeia da detecção** — `log → evento → alerta → incidente`. E o conceito que falta na maioria dos cursos: **nem todo alerta é um incidente**.
- **Ruído e tuning** — fadiga de alerta (99 de 100 alertas são ruído) e o trabalho de ajuste fino que separa um bom analista de um fraco.
- **MITRE ATT&CK** — tática × técnica: o mapa do comportamento do atacante.
- **Mão na massa** — instalação do Wazuh (server + agente) e o primeiro evento chegando ao dashboard.

## Resultado

Um SIEM funcional, um endpoint monitorado, e o ciclo completo visto ao vivo: um login falho gerou um log, que virou evento, que virou alerta.

## Prática

O laboratório completo (Wazuh server + agente no WSL) está descrito no roteiro do workshop. As regras personalizadas estão em [`wazuh/local_rules.xml`](../wazuh/local_rules.xml).
