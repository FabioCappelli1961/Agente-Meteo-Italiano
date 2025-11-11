# Agente Meteo Italiano 🌤️

> **Agente autonomo che raccoglie automaticamente le previsioni meteo italiane ogni mercoledì e invia un riepilogo via email**

## Descrizione

**Agente Meteo Italiano** è un'applicazione Python autonoma che si esegue settimanalmente per:

1. 🔍 **Raccogliere dati meteo**: Ricerca automaticamente le migliori previsioni per le principali regioni italiane
2. 📋 **Elaborare informazioni**: Crea un riepilogo formattato e professionale
3. 📧 **Inviare via email**: Spedisce il riepilogo a `drcappelli1961@gmail.com` ogni mercoledì alle 09:00

## Funzionalità

- ✅ **Scheduling automatico**: Si esegue ogni mercoledì mattina senza intervento manuale
- 🌟 **Monitoring di 10 regioni**: Lombardia, Lazio, Campania, Sicilia, Piemonte, Veneto, Emilia-Romagna, Toscana, Puglia, Basilicata
- 📐 **Report professionale**: Genera riepiloghi chiari e ben formattati
- 🔐 **Sicuro**: Utilizza credenziali Gmail con autenticazione a 2 fattori (App Password)
- 📊 **Logging completo**: Traccia di tutte le operazioni in file log
- 🛠 **Configurazione flessibile**: Personalizzabile via file `.env`

## Installazione

### 1. Prerequisiti

- Python 3.8 o superiore
- pip (gestore pacchetti Python)
- Un account Gmail (per l'invio email)
- Git

### 2. Clonare il repository

```bash
git clone https://github.com/FabioCappelli1961/Agente-Meteo-Italiano.git
cd Agente-Meteo-Italiano
```

### 3. Installare le dipendenze

```bash
pip install -r requirements.txt
```

### 4. Configurare Gmail

1. Accedi al tuo account Google: https://myaccount.google.com
2. Abilita la **Verifica in due passaggi** (se non lo hai già fatto)
3. Genera una **Password per le app**: https://myaccount.google.com/apppasswords
4. Seleziona "Mail" e "Windows Computer" (o il tuo dispositivo)
5. Copia la password generata (16 caratteri)

### 5. Configurare variabili di ambiente

Copia il file di esempio e modifica le credenziali:

```bash
cp .env.example .env
```

Modifica `.env` con le tue credenziali:

```env
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-16-char-app-password
```

## Utilizzo

### Avviare l'agente

```bash
python main.py
```

L'output sarà simile a:

```
======================================================================
🌤️ Agente Meteo Italiano - Avvio
======================================================================
✅ Agente inizializzato correttamente
✅ Scheduler avviato
🌜 Configurazione attiva:
   - Email destinatario: drcappelli1961@gmail.com
   - Giorno di esecuzione: Mercoledì
   - Ora di esecuzione: 9:00
📋 Per interrompere l'agente: premere CTRL+C
======================================================================
```

### Testare manualmente

Per eseguire l'agente immediatamente senza aspettare il mercoledì:

```python
from weather_agent import ItalyWeatherAgent
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

email_config = {
    'sender_email': os.getenv('SENDER_EMAIL'),
    'sender_password': os.getenv('SENDER_PASSWORD'),
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 465
}

agent = ItalyWeatherAgent(email_config)
await agent.run_agent()
```

## Struttura del Progetto

```
Agente-Meteo-Italiano/
├── weather_agent.py       # Classe principale dell'agente
├── main.py               # Entry point - avvia l'agente
├── requirements.txt      # Dipendenze Python
├── .env.example         # Template configurazione
├── README.md            # Questo file
├── LICENSE              # MIT License
└── weather_agent.log    # Log di esecuzione (creato automaticamente)
```

## Configurazione Avanzata

Modifica `.env` per personalizzare il comportamento:

```env
# Giorno della settimana per l'esecuzione (0=Monday, ..., 2=Wednesday, ...)
SCHEDULE_DAY_OF_WEEK=2
SCHEDULE_HOUR=9
SCHEDULE_MINUTE=0

# Level di logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO
LOG_FILE=weather_agent.log
```

## Email Ricevute

Ogni mercoledì alle 09:00 riceverai un'email simile a:

```
Oggetto: 🌤️ Riepilogo Previsioni Meteo Italia - 15/11/2025

RIEPILOGO PREVISIONI METEO ITALIA
============================================================
Data: 15/11/2025 09:00
============================================================

REGIONI MONITORATE:
1. ✅ Lombardia: fetched
2. ✅ Lazio: fetched
...

FONTI UTILIZZATE:
meteo.it, ilmeteo.it, 3bmeteo.com, weather.com

RACCOMANDAZIONI:
- Consulta quotidianamente i bollettini della Protezione Civile
- Verifica i dati su: meteo.it, ilmeteo.it, weather.com
- Segui gli avvisi meteo ufficiali regionali
- In caso di allerte, consulta le autorità locali
============================================================
```

## Risoluzione dei Problemi

### Errore: SENDER_EMAIL e SENDER_PASSWORD non configurati

**Soluzione**: Assicurati di aver copiato `.env.example` a `.env` e di aver inserito le credenziali corrette.

### Errore: Authentication failed

**Soluzione**: 
1. Verifica che l'account Gmail abbia la 2FA abilitata
2. Genera una nuova App Password su https://myaccount.google.com/apppasswords
3. Aggiorna il valore di `SENDER_PASSWORD` in `.env`

### L'agente non invia email

**Soluzione**: Controlla il file `weather_agent.log` per eventuali errori. Verifica che:
- Le credenziali Gmail siano corrette
- La connessione internet sia attiva
- SMTP_SERVER e SMTP_PORT siano corretti

## Deployment su Server

Per eseguire l'agente su un server Linux/Ubuntu 24/7:

```bash
# Installare screen o tmux
sudo apt-get install screen

# Avviare l'agente in background
screen -S weather-agent python /path/to/main.py

# Detach da screen: Ctrl+A, poi D
# Riattach: screen -r weather-agent
```

Per l'avvio automatico al riavvio, crea un servizio systemd:

```bash
sudo nano /etc/systemd/system/weather-agent.service
```

```ini
[Unit]
Description=Italian Weather Agent
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/Agente-Meteo-Italiano
ExecStart=/usr/bin/python3 /path/to/Agente-Meteo-Italiano/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Poi:

```bash
sudo systemctl daemon-reload
sudo systemctl enable weather-agent
sudo systemctl start weather-agent
```

## Contribuire

Sei invitato a contribuire al progetto! Puoi:

1. Forkare il repository
2. Creare un branch per la tua feature (`git checkout -b feature/amazing-feature`)
3. Fare commit dei tuoi cambiamenti (`git commit -m 'Add amazing feature'`)
4. Pushare al branch (`git push origin feature/amazing-feature`)
5. Aprire una Pull Request

## Licenza

Questo progetto è distribuito sotto la licenza MIT. Vedi il file [LICENSE](LICENSE) per i dettagli.

## Support

Per problemi o domande:
- Apri una [GitHub Issue](https://github.com/FabioCappelli1961/Agente-Meteo-Italiano/issues)
- Contatta: drcappelli1961@gmail.com

## Crediti

Progetto creato da [Fabio Cappelli](https://github.com/FabioCappelli1961)

---

<div align="center">

Made with ❤️ in Italy 🇮🇹

**Agente Meteo Italiano** - Previsioni meteo nella tua casella di posta ogni mercoledì

</div>
