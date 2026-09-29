# Workflow do n8n

A orquestração que liga a detecção do Wazuh à entrega do e-mail. Seis nodes, cada um com uma responsabilidade.

```
Webhook Wazuh → NORMALIZAR → ABUSE-IPDB → MISTRAL NEMOTRON → Code (Parse JSON) → RESEND
```

> **Credenciais:** todas as chaves (AbuseIPDB, NVIDIA, Resend) ficam em **credenciais do n8n**, nunca em texto dentro dos nodes. Veja [`.env.example`](../.env.example).

## Como importar / exportar

- **Importar:** no n8n, `Workflows → ⋮ → Import from File` e selecione o seu `workflow.json`.
- **Exportar (para versionar aqui):** `Workflows → ⋮ → Download` e salve como `n8n/workflow.json`. Antes de comitar, **remova credenciais** do export.

---

## 1. Webhook Wazuh
Recebe o `POST` do script `custom-n8n`. Método `POST`, path `wazuh-alert`. Coloque o webhook em **modo de produção** — em teste ele só aceita uma chamada por vez.

## 2. NORMALIZAR
Reduz o alerta cru do Wazuh a campos previsíveis, que o resto do fluxo consome:

```json
{
  "nome-alerta": "SSH_BruteForce_Seguido_Sucesso",
  "level-alerta": 15,
  "nome-agente": "COLABORADOR",
  "agent": { "ip": "127.0.0.1" },
  "data": { "srcip": "202.82.20.241" },
  "srcport": "4444",
  "usuario": "admin",
  "full_log": "... Accepted password for admin from 202.82.20.241 port 4444 ssh2"
}
```

Expressões usadas adiante: `{{ $('NORMALIZAR').item.json.data.srcip }}`, `{{ $('NORMALIZAR').item.json.usuario }}`, etc.

## 3. ABUSE-IPDB
Consulta a reputação do IP de origem (node HTTP Request):

| Campo | Valor |
|---|---|
| Method | `GET` |
| URL | `https://api.abuseipdb.com/api/v2/check` |
| Query `ipAddress` | `{{ $('NORMALIZAR').item.json.data.srcip }}` |
| Query `maxAgeInDays` | `90` |
| Query `verbose` | `true` |
| Header `Key` | *(credencial — sua API key)* |
| Header `Accept` | `application/json` |

Campos usados pela IA: `abuseConfidenceScore`, `totalReports`, `countryCode`, `isp`, `usageType`, `lastReportedAt`.

## 4. MISTRAL NEMOTRON
Análise contextual via API da NVIDIA (compatível com OpenAI).

- **Endpoint:** `POST https://integrate.api.nvidia.com/v1/chat/completions`
- **Modelo:** `mistralai/mistral-nemotron`
- **Auth:** `Authorization: Bearer <SUA_NVIDIA_API_KEY>` *(credencial)*
- **Parâmetros:** `temperature: 0`, `top_p: 0.7`, `max_tokens: 400`

**System prompt (resumo):**
> Você é um analista SOC experiente. Analise o alerta considerando usuário, ativo, IP de origem, regra do Wazuh e reputação. Determine o risco e dê recomendações práticas. **Não invente** informações. Diferencie ações imediatas de ações de investigação. Responda **SOMENTE com JSON válido**, sem markdown.

O **User** carrega o contexto (dados do Wazuh + AbuseIPDB) e pede o formato de saída abaixo.

**Saída esperada da IA:**
```json
{
  "veredito": "MALICIOUS | SUSPICIOUS | BENIGN | UNKNOWN",
  "confidence": 0,
  "severity": "LOW | MEDIUM | HIGH | CRITICAL",
  "reason": "explicação objetiva baseada nos dados fornecidos",
  "immediate_actions": ["ação imediata 1", "ação imediata 2"],
  "investigation_steps": ["investigação 1", "investigação 2"],
  "recommendation": "recomendação final específica para este cenário"
}
```

## 5. Code — Parse JSON
O modelo às vezes embrulha o JSON num bloco markdown. Este código remove as marcações e converte para um objeto real do n8n:

```javascript
const content = $json.choices[0].message.content;
const clean = content
  .replace(/```json/g, '')
  .replace(/```/g, '')
  .trim();
const verdict = JSON.parse(clean);
return [{ json: verdict }];
```

Depois disto, os campos ficam disponíveis direto: `$json.veredito`, `$json.severity`, `$json.immediate_actions`, etc.

## 6. RESEND
Entrega o e-mail final. O corpo é o [`email-template.html`](email-template.html), preenchido com as expressões do fluxo.

**Assunto sugerido:**
```
[WAZUH] {{ $('NORMALIZAR').item.json['nome-alerta'] }} | {{ $json.severity }} | {{ $('NORMALIZAR').item.json.data.srcip }}
```

> O Resend exige remetente/domínio autorizado. Se o e-mail não chega, quase sempre é isso.
