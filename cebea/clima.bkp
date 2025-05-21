#!/bin/bash

IP="192.168.15.49"  # coloca o IP do ESP32 aqui

# Coletando dados
DADOS=$(curl -s http://$IP/)

# Pegando Temperatura
TEMP=$(echo "$DADOS" | grep -oP 'Temperatura:</strong> \K[0-9.]+')

# Pegando Umidade
HUM=$(echo "$DADOS" | grep -oP 'Umidade:</strong> \K[0-9.]+')

echo "     Dados do Ambiente"
echo "Temperatura: $TEMP °C"
echo "Umidade:     $HUM %"
