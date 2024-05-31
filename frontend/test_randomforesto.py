import joblib
from pydantic import BaseModel
from flask import Flask, request, jsonify
import pandas as pd

model = joblib.load('random_forest_model.pkl')


class Dati_in_entrata(BaseModel):
    durationhours: float
    priceperStop: float
    durata_in_minuti: float
    num_scali: float
    emissioni_di_co2: float
    media_co2_per_percorso: float
    percentuale_co2: float
    mese_in_numero: int

app = Flask(__name__)


@app.route("/", methods=["GET"])
def accueil():
    return jsonify({"messaggio": "Benvenuto su l'API de predizione per il prezzo dei biglietti"})


@app.route("/predire", methods=["POST"])
def predire():
    if not request.json:
        return jsonify({"erreur": "Nessun JSON fornito"}), 400

    try:

        dati = Dati_in_entrata(**request.json)
        dati_df = pd.DataFrame([dati.dict()])

        predizioni = model.predict(dati_df)
        probabilita = model.predict_proba(dati_df)[:, 1]

        risultati = dati.dict()
        risultati['predizione'] = int(predizioni[0])
        risultati['probabilita_prezzo'] = probabilita[0]

        return jsonify({"risultati": risultati})
    except Exception as e:

        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
