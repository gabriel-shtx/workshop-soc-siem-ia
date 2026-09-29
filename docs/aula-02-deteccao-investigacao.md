# Aula 2 — Detecção e Investigação

O dia em que o participante **senta dos dois lados da mesa**: primeiro o atacante, depois o analista que investiga os próprios rastros.

## Conteúdo

- **Como o SIEM decide** — `log → decoder → regra → alerta`. Nada de mágica: alguém escreveu a regra. Decoder lê e separa; regra compara e julga.
- **A linguagem do analista** — severidade (e por que **não** é o mesmo que prioridade), IOC × TTP, e a **Pirâmide da Dor**: por que detectar comportamento vale mais que bloquear um IP.
- **Construir a detecção** — o participante escreve a própria regra no Wazuh, **antes** de atacar, e monta um dashboard. Assim o ataque vira o teste da detecção que ele criou.
- **Atacar o laboratório** — com o **Atomic Red Team** (Red Canary), encenando os TTPs de um grupo fictício ("Evil Art"): força bruta no sudo (`T1110.001`) seguida de criação de usuário backdoor (`T1136.001`).
- **Investigar** — o método das cinco perguntas (o quê, quando, onde, quem, e agora), aplicado numa **dinâmica de três cenários** em que a turma decide: falso positivo, verdadeiro positivo — ou "preciso de mais informação".
- **n8n** — introdução e instalação, preparando a automação da aula 3.

## Fio condutor

A regra `100210` — "Comportamento do Evil Art detectado!" — correlaciona a **sequência** (força bruta + criação de usuário na mesma janela), não um evento solto. É detecção de comportamento na prática. Veja [`wazuh/local_rules.xml`](../wazuh/local_rules.xml).

## Atomics executados

```powershell
Invoke-AtomicTest T1110.001-5
Invoke-AtomicTest T1136.001-1 -InputArgs @{username="evil-backdoor-user"}
```

> Rodam via `Invoke-AtomicRedTeam` (PowerShell / pwsh) em ambiente próprio e isolado.
