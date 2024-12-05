import random
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error
import time  # Per ritardare l'esecuzione tra un ciclo e l'altro

# Definizione delle tabelle di supporto
codes = ['P001', 'P002', 'P003', 'P004', 'P005']
operators = ['OP01', 'OP02', 'OP03', 'OP04', 'OP05']
machines = ['CNC01', 'CNC02', 'CNC03']
events = [
    'Fermo macchina: rottura inserto',
    'Fermo macchina: cambio turno',
    'Fermo macchina: pausa legale',
    'Fermo macchina: cambio commessa'
]

# Parametri di simulazione
start_time = datetime.now()  # Inizia al momento dell'esecuzione
duration_minutes = 250  # Durata della simulazione in minuti

try:
    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3307,
        user="ITS_2024",
        password="gabrielli",
        database="its_2024"
    )

    if connection.is_connected():
        print("Connessione a MySQL effettuata con successo")

        insert_query = """
        INSERT INTO DatiPezzi (Timestamp, PieceCode, WeightKg, TemperatureC, Event)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        cursor = connection.cursor()
        current_time = start_time

        # Esegui un ciclo per 10 minuti
        for _ in range(duration_minutes):
            for machine in machines:
                for code in codes:
                    operator = random.choice(operators)
                    weight = round(random.uniform(1.0, 5.0), 2)  # Peso casuale
                    temperature = round(random.uniform(800.0, 1200.0), 2)  # Temperatura casuale
                    event = random.choice(events) if random.random() < 0.3 else None

                    # Inserimento nel database
                    cursor.execute(insert_query, (
                        current_time.strftime('%Y-%m-%d %H:%M:%S'),
                        code,
                        weight,
                        temperature,
                        event
                    ))
            
            # Conferma delle modifiche dopo ogni minuto
            connection.commit()
            print(f"Inseriti record per il minuto: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Incrementa il tempo di un minuto e attende
            current_time += timedelta(minutes=45)
            time.sleep(0.5)  # Aspetta un minuto reale prima di ripetere il ciclo
        
except Error as e:
    print(f"Errore durante la connessione a MySQL: {e}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Connessione a MySQL chiusa")
