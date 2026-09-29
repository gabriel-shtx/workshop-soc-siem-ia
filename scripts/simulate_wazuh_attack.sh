#!/bin/bash
# ============================================================================
# Simula o cenário de força bruta SSH + login com sucesso — SEM atacar nada.
# Workshop SOC, SIEM e IA na Prática · Imperium Fox Academy
#
# O logger injeta linhas no syslog com a "cara" de eventos de SSH; o Wazuh lê
# essas linhas e a regra 100501 dispara. É ensaio de detecção, não ataque real.
#
# Uso:
#   chmod +x simulate_wazuh_attack.sh
#   sudo ./simulate_wazuh_attack.sh 185.220.101.1
#
# O IP é apenas ilustrativo (faixa conhecida por reputação ruim, útil para ver
# o AbuseIPDB responder). Rode SOMENTE no seu laboratório.
# ============================================================================

ATTACKER_IP="${1:-185.220.101.1}"

# 5 falhas seguidas...
for i in {1..5}; do
    logger -t sshd "Failed password for invalid user admin from $ATTACKER_IP port 4444 ssh2"
    sleep 1
done

# ...e então um sucesso (é isto que fecha a sequência da regra 100501)
logger -t sshd "Accepted password for admin from $ATTACKER_IP port 4444 ssh2"

echo "Cenário simulado a partir do IP $ATTACKER_IP. Confira o alerta no dashboard do Wazuh."
