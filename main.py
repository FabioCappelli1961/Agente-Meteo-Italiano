#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Entry Point - Agente Meteo Italiano
Avvia l'agente autonomo che raccoglie previsioni meteo italiane ogni mercoledì
"""

import os
import logging
import sys
from pathlib import Path
from dotenv import load_dotenv
from weather_agent import ItalyWeatherAgent

# Carica le variabili di ambiente dal file .env
load_dotenv()

# Configura logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.getenv('LOG_FILE', 'weather_agent.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    """
    Funzione principale - Avvia l'Agente Meteo Italiano
    """
    logger.info("="*70)
    logger.info("🌤️ Agente Meteo Italiano - Avvio")
    logger.info("="*70)
    
    try:
        # Verifica configurazione email
        sender_email = os.getenv('SENDER_EMAIL')
        sender_password = os.getenv('SENDER_PASSWORD')
        
        if not sender_email or not sender_password:
            logger.error(
                "❌ Errore: SENDER_EMAIL e SENDER_PASSWORD non configurati.\n"
                "   Copia .env.example a .env e configura le credenziali Gmail."
            )
            sys.exit(1)
        
        # Configurazione email
        email_config = {
            'sender_email': sender_email,
            'sender_password': sender_password,
            'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
            'smtp_port': int(os.getenv('SMTP_PORT', 465))
        }
        
        # Crea l'agente
        agent = ItalyWeatherAgent(email_config)
        logger.info("✅ Agente inizializzato correttamente")
        
        # Avvia lo scheduler
        agent.schedule_weekly()
        logger.info("✅ Scheduler avviato")
        
        # Informazioni di avvio
        logger.info("🌜 Configurazione attiva:")
        logger.info(f"   - Email destinatario: {agent.email_recipient}")
        logger.info(f"   - Giorno di esecuzione: Mercoledì")
        logger.info(f"   - Ora di esecuzione: {os.getenv('SCHEDULE_HOUR', 9)}:00")
        logger.info("📋 Per interrompere l'agente: premere CTRL+C")
        logger.info("="*70)
        
        # Mantieni l'agente in esecuzione
        import time
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("""
            \n⚠️  Interruzione richiesta...
            """)
            agent.stop_scheduler()
            logger.info("✅ Agente fermato correttamente")
    
    except Exception as e:
        logger.error(f"❌ Errore critico: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
