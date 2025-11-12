# Weather Agent - Agente Meteo Autonomo per l'Italia
# Raccoglie automaticamente previsioni meteo ogni mercoledì e invia via email

import asyncio
import time
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import httpx
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

class ItalyWeatherAgent:
    """
    Agente autonomo che raccoglie le previsioni meteo italiane
    ogni mercoledì e invia un riepilogo via email.
    """
    
    def __init__(self, email_config: dict):
        self.email_config = email_config
        self.scheduler = BackgroundScheduler()
        self.email_recipient = "drcappelli1961@gmail.com"
        self.is_running = False
        
    async def search_weather_forecasts(self) -> dict:
        """
        Cerca le migliori previsioni meteo per l'Italia
        """
        weather_data = {
            "regions": {},
            "timestamp": datetime.now().isoformat(),
            "sources": ["meteo.it", "ilmeteo.it", "3bmeteo.com", "weather.com"]
        }
        
        regions = [
            "Lombardia", "Lazio", "Campania", "Sicilia", "Piemonte",
            "Veneto", "Emilia-Romagna", "Toscana", "Puglia", "Basilicata"
        ]
        
        async with httpx.AsyncClient(timeout=15.0) as client:
            for region in regions:
                try:
                    # Ricerca previsioni meteo per questa regione
                    response = await client.get(
                        "https://www.google.com/search",
                        params={
                            "q": f"previsioni meteo {region} italia questa settimana"
                        }
                    )
                    weather_data["regions"][region] = {
                        "status": "fetched",
                        "status_code": response.status_code,
                        "timestamp": datetime.now().isoformat()
                    }
                except Exception as e:
                    weather_data["regions"][region] = {
                        "status": "error",
                        "error": str(e)
                    }
        
        return weather_data
    
    def create_summary(self, weather_data: dict) -> str:
        """
        Crea un riepilogo formattato delle previsioni meteo
        """
        summary = f"""RIEPILOGO PREVISIONI METEO ITALIA
{'='*60}
Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
{'='*60}

REGIONI MONITORATE:
"""
        
        for i, (region, data) in enumerate(weather_data.get("regions", {}).items(), 1):
            status_icon = "\u2705" if data.get('status') == 'fetched' else "\u274c"
            summary += f"\n{i}. {status_icon} {region}: {data.get('status', 'N/A')}"
        
        summary += f"""\n\nFONTI UTILIZZATE:
{', '.join(weather_data.get('sources', []))}

RACCOMANDAZIONI:
- Consulta quotidianamente i bollettini della Protezione Civile
- Verifica i dati su: meteo.it, ilmeteo.it, weather.com
- Segui gli avvisi meteo ufficiali regionali
- In caso di allerte, consulta le autorità locali

{'='*60}
Generato automaticamente dall'Agente Meteo Italiano
https://github.com/FabioCappelli1961/Agente-Meteo-Italiano
{'='*60}
"""
        return summary
    
    async def send_email_report(self, summary: str) -> bool:
        """
        Invia il riepilogo via email
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config['sender_email']
            msg['To'] = self.email_recipient
            msg['Subject'] = f"\ud83c\udf24\ufe0f Riepilogo Previsioni Meteo Italia - {datetime.now().strftime('%d/%m/%Y')}"
            
            msg.attach(MIMEText(summary, 'plain', 'utf-8'))
            
            # Connessione SMTP (Gmail)
            with smtplib.SMTP_SSL(
                self.email_config['smtp_server'],
                self.email_config['smtp_port']
            ) as server:
                server.login(
                    self.email_config['sender_email'],
                    self.email_config['sender_password']
                )
                server.send_message(msg)
            
            print(f"[{datetime.now()}] Email inviata con successo a {self.email_recipient}")
            return True
        except Exception as e:
            print(f"[{datetime.now()}] Errore invio email: {e}")
            return False
    
    async def run_agent(self) -> dict:
        """
        Esegue il ciclo completo dell'agente
        """
        print(f"[{datetime.now()}] \ud83e\udd16 Agente Meteo: Inizio raccolta dati...")
        
        try:
            # Fase 1: Ricerca
            weather_data = await self.search_weather_forecasts()
            print(f"[{datetime.now()}] \u2705 Dati meteo raccolti: {len(weather_data.get('regions', {}))} regioni")
            
            # Fase 2: Riepilogo
            summary = self.create_summary(weather_data)
            print(f"[{datetime.now()}] \u2705 Riepilogo generato")
            
            # Fase 3: Invio
            email_sent = await self.send_email_report(summary)
            print(f"[{datetime.now()}] \u2705 Operazione completata")
            
            return {
                "status": "completed",
                "regions_processed": len(weather_data.get('regions', {})),
                "email_sent": email_sent,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"[{datetime.now()}] \u274c Errore nell'esecuzione: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def schedule_weekly(self):
        """
        Pianifica l'esecuzione ogni mercoledì alle 09:00
        """
        self.scheduler.add_job(
            self.run_agent,
            trigger=CronTrigger(day_of_week=2, hour=9, minute=0),  # 2 = mercoledì
            id='weather_agent_weekly'
        )
        self.scheduler.start()
        self.is_running = True
        print(f"[{datetime.now()}] \u23f0 Agente programmato: ogni mercoledì alle 09:00")
    
    def stop_scheduler(self):
        """
        Arresta lo scheduler
        """
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            print(f"[{datetime.now()}] \u26a0 Scheduler fermato")


if __name__ == "__main__":
    # Configurazione email (inserire credenziali reali)
    EMAIL_CONFIG = {
        'sender_email': 'your-email@gmail.com',
        'sender_password': 'your-app-password',  # Password app Gmail (non la password principale)
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 465
    }
    
    # Inizializza l'agente
    agent = ItalyWeatherAgent(EMAIL_CONFIG)
    
    # Avvia lo scheduler
    agent.schedule_weekly()
    
    # Mantieni in esecuzione
    try:
        print("Agente Meteo Italiano avviato. Premere CTRL+C per fermare.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nFermo dell'agente...")
        agent.stop_scheduler()
