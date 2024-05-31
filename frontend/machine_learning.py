import pandas as pd
import numpy as np

from sklearn.impute import SimpleImputer

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
import time
import joblib

df = pd.read_csv('../csv_puliti/flight data.csv')
#Cancelliamo le colonne irrelevanti
df.drop(columns=['scan_date', 'currency', 'aircraft_type'], inplace=True)
#Splittiamo le colonne flight_number e aircraft_type per ottenere solo il nome della prima compagnia e tipo
df['flight_number'] = df['flight_number'].apply(lambda x : x.split("|")[0])
#Trasformiamo i valori della colonnna airline_number in due categorie
def f(x):
    if x != "multi":
        x = "singolo"
    return x
df['airline_number'] = df['airline_number'].apply(f)
# Imputazione per la mediana
imputer_median = SimpleImputer(strategy='median')
df['price'] = imputer_median.fit_transform(df[['price']])
df['avg_co2_emission_for_this_route'] = imputer_median.fit_transform(df[['avg_co2_emission_for_this_route']])
#df['co2_percentage'] = imputer_median.fit_transform(df[['co2_percentage']])
df['co2_emissions'] = imputer_median.fit_transform(df[['co2_emissions']])

# Verifica dei valori mancanti dopo imputazione
missing_values_after = df.isnull().mean()
print("\nMissing Values After Treatment:\n", missing_values_after)
#Trasformazione sulla colonna co2_percentage
df['co2_percentage'] = df['co2_percentage'].str[:-1]
df['co2_percentage'] = df['co2_percentage'].replace(['', 'None', '-'], np.nan)
mean_column = df['co2_percentage'].astype(float).mean()
df['co2_percentage'] = df['co2_percentage'].fillna(mean_column).astype(int)
#Casting del tipo delle variabili
df['departure_time'] = pd.to_datetime(df['departure_time'])
df['arrival_time'] = pd.to_datetime(df['arrival_time'])
#creazione di nuove colonne calcolate
df['duration'] = df['arrival_time'] - df['departure_time']
df['duration_in_minutes'] = df['duration'].dt.total_seconds() / 60
df['month_in_number'] = df['departure_time'].dt.month
df['month'] = df['departure_time'].dt.month_name()
#Rinominare le colonne
df = df.set_axis(['codice_aereoporto_di_partenza', 'paese_di_partenza', 'codice_aereoporto_di_arrivo', 'paese_di_arrivo', \
            'numero_di_compagnie', 'nome_compagnia', 'codice_volo', 'ora_partenza', 'ora_arrivo', 'durata', \
            'num_scali', 'prezzo', 'emissioni_di_co2', 'media_co2_per_percorso', 'percentuale_co2', 'durata_in_minuti', \
             'mese_in_numero', 'mese'], axis = "columns")
# Create new features (if applicable)
df['price_per_stop'] = df['prezzo'] / (df['num_scali'] + 1)
df['duration_hours'] = df['durata_in_minuti'] / 60
# Select relevant features for the model
X = df[['duration_hours','price_per_stop','durata_in_minuti', 'num_scali', 'emissioni_di_co2', 'media_co2_per_percorso', 'percentuale_co2', 'mese_in_numero']]
y = df['prezzo']
# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Training the Random Forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

start_time = time.time()
rf_model.fit(X_train, y_train)
end_time = time.time()
# Model training time
training_time = end_time - start_time
# Making predictions on the training and testing sets
y_train_pred = rf_model.predict(X_train)
y_test_pred = rf_model.predict(X_test)
# Calculating performance metrics for training set
r2_train = r2_score(y_train, y_train_pred)
rmse_train = np.sqrt(mean_squared_error(y_train, y_train_pred))
mae_train = mean_absolute_error(y_train, y_train_pred)
# Calculating performance metrics for testing set
r2_test = r2_score(y_test, y_test_pred)
rmse_test = np.sqrt(mean_squared_error(y_test, y_test_pred))
mae_test = mean_absolute_error(y_test, y_test_pred)
# Displaying the results
performance_summary = {
    'Metric': ['R² Score', 'RMSE', 'MAE'],
    'Training': [r2_train, rmse_train, mae_train],
    'Testing': [r2_test, rmse_test, mae_test]
}
performance_df = pd.DataFrame(performance_summary)
# Model training time
print(f"Model Training Time: {training_time:.2f} seconds")
#Save the model
joblib.dump(rf_model, 'random_forest_model.pkl')