# ==========================================================
# TREINAMENTO E SALVAMENTO DO MODELO
# RANDOM FOREST - PREVISÃO DE PREÇOS DE IMÓVEIS
# ==========================================================


# ==========================================================
# 1. IMPORTAÇÃO DAS BIBLIOTECAS
# ==========================================================

from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score
)



# ==========================================================
# 2. DEFINIÇÃO DOS CAMINHOS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[1]

CAMINHO_DADOS = BASE_DIR / "dados" / "train.csv"

CAMINHO_MODELO = (
    Path(__file__).resolve().parent
    / "modelo_random_forest.pkl"
)

# ==========================================================
# 3. CARREGAMENTO DA BASE DE DADOS
# ==========================================================

dados = pd.read_csv(CAMINHO_DADOS)

print("Base de dados carregada com sucesso!")

print("\nDimensão da base:")
print(dados.shape)


# ==========================================================
# 4. DEFINIÇÃO DAS VARIÁVEIS DO MODELO
# ==========================================================

features = [
    "GrLivArea",
    "OverallQual",
    "GarageCars",
    "BedroomAbvGr",
    "LotArea",
    "YearBuilt",
    "FullBath"
]

X = dados[features]

y = dados["SalePrice"]

# ==========================================================
# 5. DIVISÃO DA BASE EM TREINO E TESTE
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# ==========================================================
# 6. TREINAMENTO DO MODELO DE VALIDAÇÃO
# ==========================================================

modelo_validacao = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

modelo_validacao.fit(
    X_train,
    y_train
)

# ==========================================================
# 7. AVALIAÇÃO DO MODELO
# ==========================================================

y_pred = modelo_validacao.predict(X_test)

rmse = mean_squared_error(
    y_test,
    y_pred
) ** 0.5

mae = mean_absolute_error(
    y_test,
    y_pred
)

r2 = r2_score(
    y_test,
    y_pred
)

print("\n====================================")
print("DESEMPENHO DO MODELO")
print("====================================")

print(f"RMSE: {rmse:.2f}")
print(f"MAE: {mae:.2f}")
print(f"R²: {r2:.4f}")

# ==========================================================
# 8. TREINAMENTO DO MODELO FINAL
# ==========================================================

modelo_final = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

modelo_final.fit(
    X,
    y
)


# ==========================================================
# 9. CRIAÇÃO DO ARTEFATO
# ==========================================================

artefato = {
    "model": modelo_final,
    "scaler": None,
    "features": features,
    "metrics": {
        "rmse": rmse,
        "mae": mae,
        "r2": r2
    }
}


# ==========================================================
# 10. SALVAMENTO DO MODELO
# ==========================================================

joblib.dump(
    artefato,
    CAMINHO_MODELO
)

print("\n====================================")
print("MODELO SALVO COM SUCESSO")
print("====================================")

print(f"\nArquivo criado em:\n{CAMINHO_MODELO}")

print("\nVariáveis utilizadas pelo modelo:")

for feature in features:
    print(f"- {feature}")

