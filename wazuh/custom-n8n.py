#!/usr/bin/env python3
"""
Integração Wazuh -> n8n
Workshop SOC, SIEM e IA na Prática · Imperium Fox Academy

Instalação (no Wazuh Manager):
    sudo cp custom-n8n.py /var/ossec/integrations/custom-n8n
    sudo chmod 750 /var/ossec/integrations/custom-n8n
    sudo chown root:wazuh /var/ossec/integrations/custom-n8n
    sudo systemctl restart wazuh-manager

O Wazuh chama este script passando:
    argv[1] = caminho do arquivo de alerta (JSON)
    argv[2] = api_key definida na tag <api_key> da integração (não usada aqui)
    argv[3] = hook_url definida na tag <hook_url> da integração

Observação: a api_key é recebida mas não é utilizada nesta versão — o alerta
é enviado direto ao webhook. Se o seu webhook exigir autenticação, adicione o
cabeçalho aqui (e guarde o segredo fora do versionamento).
"""
import sys
import json
import requests


def main():
    alert_file = sys.argv[1]
    # api_key   = sys.argv[2]   # recebido do Wazuh; não usado nesta versão
    hook_url = sys.argv[3]

    with open(alert_file, "r") as f:
        alert = json.load(f)

    response = requests.post(hook_url, json=alert, timeout=10)
    print(f"n8n webhook response: {response.status_code}")


if __name__ == "__main__":
    main()
