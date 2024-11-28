#importo le dipendenze, jsonify serve per avere ritorno in json
from flask import Flask, request, jsonify

import mysql.connector

#creazione di un applicativo Flask
app = Flask(__name__)

#endpoint della api dove raccolgo dati
#importante che "app" sia il nome del Flask server creato sopra, tra virgolette ho il path
@app.route("/")
def home():
    mydb = mysql.connector.connect(
    host="127.0.0.1",      # Indirizzo IP
    port=3307,             # Porta
    user="ITS_2024",       # Nome utente
    password="gabrielli",           # Inserisci la password corretta
    database="its_2024"            # Specifica il nome del database, se necessario
    )

    # Esegui una query per recuperare i dati
    #cursor sarebbe un'interfaccia per eseguire comandi SQL e vederne i risultati
    cursor = mydb.cursor(dictionary=True)  # dictionary=True per ottenere i risultati come dizionari altrimenti con =False diventano delle tuple
    cursor.execute("SELECT * FROM favourite_data")  # Cambia "utenti" con il nome della tua tabella
    result = cursor.fetchall()  # Ottieni tutti i risultati
        
    # Chiudi la connessione
    cursor.close()
    mydb.close()
        
    # Ritorna i dati come JSON
    return jsonify(result)



#creazione metodo HTTP get
#tra <> passo un dato tramite url tipo il numero di user da raggiungere nel db
@app.route("/get-user/<user_id>")
def get_user(user_id):
    
    user_data = {
        "user_id": user_id,
        "name": "John Doe",
        "email": "aaaa@libero.it"
    }

    #"get-user/123?extra=hello world" 
    #con il punto di domanda passo piu' cose nell'url, sia 123 che extra equivalga a hello world 

    
    #va a prendere nell'url ossia la richiesta l'argomento assegnato alla variabile extra
    extra = request.args.get("extra")

    #se extra non esiste nell'url nel json finale non avro' il campo extra 
    if extra:
        user_data["extra"] = extra
    
    #il ritorno dati da un api per il dizionario user_data va fatto in json
    return jsonify(user_data), 200


#siccome non sto usando il metodo standard get ma un post devo specificarlo
@app.route("/create-user", methods=["POST"])
def create_user():
    #se il metodo della richiesta e' post
    if request.method == "POST":
        #per creare un utente deve essere passato un json con i dati relativi nel body della richiesta, tipo con postman
        data = request.get_json()

        #ritorno i dati ricevuti cosi' faccio veder che sono stati ricevuti
        return jsonify(data), 201

#run del server Flask
if __name__ == "__main__":
    app.run(debug=True)