#!/usr/bin/env python3
# Test manuale per l'Agente Meteo Italiano
# Questo script testa manualmente l'invio di una email meteo

import sys
import os
from datetime import datetime

# Aggiungi il percorso al modulo weather_agent
sys.path.insert(0, os.path.dirname(__file__))

from weather_agent import ItalyWeatherAgent
import asyncio

def test_manual_email_send():
    """
    Test manuale di invio email
    """
    print(f"[{datetime.now()}] INIZIO TEST DI INVIO EMAIL")
    print(f"[{datetime.now()}] =========================================")
    
    # Configurazione email (ATTENZIONE: inserire credenziali reali)
    EMAIL_CONFIG = {
        'sender_email': 'your-email@gmail.com',
        'sender_password': 'your-app-password',  # Password app Gmail
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 465
    }
    
    # Inizializza l'agente
    agent = ItalyWeatherAgent(EMAIL_CONFIG)
    
    # Esegui il ciclo completo una volta (test immediato)
    print(f"[{datetime.now()}] Esecuzione test agente...")
    result = agent.run_agent_sync()
    
    print(f"[{datetime.now()}] =========================================")
    print(f"[{datetime.now()}] Risultato del test:")
    print(f"  - Status: {result['status']}")
    print(f"  - Email inviata: {result.get('email_sent', False)}")
    print(f"  - Regioni elaborate: {result.get('regions_processed', 0)}")
    print(f"[{datetime.now()}] FINE TEST")
    
    return result['status'] == 'completed' and result.get('email_sent', False)

if __name__ == "__main__":
    print("\nTEST MANUALE - AGENTE METEO ITALIANO")
    print("=====================================")
    print("Questo script invia un riepilogo meteo a drcappelli1961@gmail.com")
    print("\nASSICURATI DI AVER CONFIGURATO LE CREDENZIALI EMAIL NEL FILE!\n")
    
    success = test_manual_email_send()
    
    if success:
        print("\n✅ TEST RIUSCITO!")
        sys.exit(0)
    else:
        print("\n❌ TEST FALLITO!")
        sys.exit(1)
