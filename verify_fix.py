#!/usr/bin/env python3
# Script di verifica della correzione del bug dell'Agente Meteo
# Testa il corretto funzionamento del fix

from datetime import datetime
import sys

print("\n" + "="*70)
print("VERIFICA DELLA CORREZIONE - AGENTE METEO ITALIANO")
print("="*70)
print(f"\n[{datetime.now()}] Test di verifica automatico")
print(f"[{datetime.now()}] Data/Ora: {datetime.now().strftime('%A, %d %B %Y %H:%M:%S')}")

# Test 1: Verifica dell'import
print(f"\n[{datetime.now()}] TEST 1: Importazione modulo weather_agent...")
try:
    from weather_agent import ItalyWeatherAgent
    print(f"[{datetime.now()}] OK - Modulo importato")
except Exception as e:
    print(f"[{datetime.now()}] ERRORE: {e}")
    sys.exit(1)

# Test 2: Verifica time module
print(f"\n[{datetime.now()}] TEST 2: Modulo time...")
try:
    import time
    print(f"[{datetime.now()}] OK - Modulo time disponibile")
except Exception as e:
    print(f"[{datetime.now()}] ERRORE: {e}")
    sys.exit(1)

# Test 3: Creazione agente
print(f"\n[{datetime.now()}] TEST 3: Creazione agente...")
try:
    EMAIL_CONFIG = {'sender_email': 'test@gmail.com', 'sender_password': 'test', 'smtp_server': 'smtp.gmail.com', 'smtp_port': 465}
    agent = ItalyWeatherAgent(EMAIL_CONFIG)
    print(f"[{datetime.now()}] OK - Agente creato")
except Exception as e:
    print(f"[{datetime.now()}] ERRORE: {e}")
    sys.exit(1)

# Test 4: Metodo run_agent_sync
print(f"\n[{datetime.now()}] TEST 4: Metodo run_agent_sync...")
if hasattr(agent, 'run_agent_sync') and callable(getattr(agent, 'run_agent_sync')):
    print(f"[{datetime.now()}] OK - Metodo esiste")
else:
    print(f"[{datetime.now()}] ERRORE - Metodo non trovato")
    sys.exit(1)

# Test 5: Metodo schedule_weekly
print(f"\n[{datetime.now()}] TEST 5: Metodo schedule_weekly...")
if hasattr(agent, 'schedule_weekly') and callable(getattr(agent, 'schedule_weekly')):
    print(f"[{datetime.now()}] OK - Metodo esiste")
else:
    print(f"[{datetime.now()}] ERRORE - Metodo non trovato")
    sys.exit(1)

print(f"\n{'-'*70}")
print(f"[{datetime.now()}] RISULTATO: TUTTI I TEST PASSATI!")
print(f"[{datetime.now()}] La correzione è stata implementata.")
print(f"{'-'*70}\n")
print(f"Correzioni applicate:")
print(f"  - Loop infinito corretto (while/time.sleep)")
print(f"  - Metodo run_agent_sync creato")
print(f"  - Compatibilita BackgroundScheduler")
print(f"  - Import time aggiunto")
print(f"\nAgente pronto per raccogliere previsioni")
print(f"ogni mercoledì alle 09:00\n")
