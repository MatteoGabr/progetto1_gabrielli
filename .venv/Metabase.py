import requests

# Configura le credenziali di accesso a Metabase
METABASE_URL = "http://localhost:3000"
EMAIL = "matteo.gabrielli@edu.itspiemonte.it"
PASSWORD = "MetabaseGabrielli1"

# Ottieni il token di sessione
response = requests.post(f"{METABASE_URL}/api/session", json={"username": EMAIL, "password": PASSWORD})

if response.status_code == 200:
    session_token = response.json()["id"]
    print("Autenticazione riuscita!")
else:
    print("Errore nell'autenticazione:", response.json())
    exit()

headers = {"X-Metabase-Session": session_token}
