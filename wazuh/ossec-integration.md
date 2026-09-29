# Integração Wazuh → n8n

Como fazer o Wazuh Manager enviar cada alerta relevante para o webhook do n8n.

## 1. Bloco de integração

No `/var/ossec/etc/ossec.conf`, dentro de `<ossec_config>`:

```xml
<integration>
  <name>custom-n8n</name>
  <hook_url>http://127.0.0.1:5678/webhook/wazuh-alert</hook_url>
  <level>9</level>
  <alert_format>json</alert_format>
</integration>
```

- **`name`** → precisa bater com o nome do script em `/var/ossec/integrations/`.
- **`hook_url`** → o endereço do webhook do n8n. Ajuste host/porta ao seu ambiente.
- **`level`** → só alertas de nível **≥ 9** disparam a integração. Suba ou desça conforme o ruído.
- **`alert_format`** → `json`, para o n8n receber estruturado.

## 2. Script de envio

O arquivo [`custom-n8n.py`](custom-n8n.py) faz o `POST` do alerta ao webhook. Instale com a permissão certa — **este passo é o que mais dá errado**:

```bash
sudo cp custom-n8n.py /var/ossec/integrations/custom-n8n
sudo chmod 750 /var/ossec/integrations/custom-n8n
sudo chown root:wazuh /var/ossec/integrations/custom-n8n
```

Sem `chmod 750` e `chown root:wazuh`, o manager se recusa a executar o script e o alerta nunca sai.

## 3. Aplicar

```bash
sudo /var/ossec/bin/wazuh-analysisd -t     # valida a config
sudo systemctl restart wazuh-manager
```

## Troubleshooting

| Sintoma | Verificação |
|---|---|
| Webhook não recebe nada | URL, porta `5678`, e se o **webhook do n8n está em modo de produção** (não só teste). |
| Manager não reinicia | Rode `wazuh-analysisd -t` e cheque a sintaxe do XML. |
| Integração não executa | Permissão do script: `chmod 750` + `chown root:wazuh`. |
