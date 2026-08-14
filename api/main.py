# ==========================================================
# API DE PREVISÃO DE PREÇOS DE IMÓVEIS
# FASTAPI + RANDOM FOREST
# ==========================================================


# ==========================================================
# 1. IMPORTAÇÃO DAS BIBLIOTECAS
# ==========================================================

from __future__ import annotations

import os

from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# ==========================================================
# 2. CONFIGURAÇÃO DO CAMINHO DO MODELO
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

DEFAULT_MODEL_PATH = (
    BASE_DIR / "modelo_random_forest.pkl"
).resolve()

MODEL_PATH = Path(
    os.getenv(
        "MODEL_PATH",
        str(DEFAULT_MODEL_PATH)
    )
).resolve()

# ==========================================================
# 3. INICIALIZAÇÃO DA APLICAÇÃO FASTAPI
# ==========================================================

app = FastAPI(
    title="API de Previsão de Preços de Imóveis",
    description=(
        "API para estimativa do preço de venda de imóveis "
        "utilizando modelo Random Forest."
    ),
    version="1.0.0"
)

# ==========================================================
# 4. MODELOS DE ENTRADA - PYDANTIC
# ==========================================================

class ImovelInput(BaseModel):

    GrLivArea: float = Field(
        ...,
        gt=0,
        description="Área construída acima do nível do solo, em pés².",
        examples=[1800]
    )

    OverallQual: int = Field(
        ...,
        ge=1,
        le=10,
        description="Qualidade geral da construção e acabamento.",
        examples=[8]
    )

    GarageCars: int = Field(
        ...,
        ge=0,
        description="Número de vagas na garagem.",
        examples=[2]
    )

    BedroomAbvGr: int = Field(
        ...,
        ge=0,
        description="Número de quartos acima do nível do solo.",
        examples=[3]
    )

    LotArea: float = Field(
        ...,
        gt=0,
        description="Área total do terreno, em pés².",
        examples=[9000]
    )

    YearBuilt: int = Field(
        ...,
        ge=1800,
        le=2100,
        description="Ano de construção do imóvel.",
        examples=[2015]
    )

    FullBath: int = Field(
        ...,
        ge=0,
        description="Número de banheiros completos.",
        examples=[2]
    )


class PredictRequest(BaseModel):

    data: ImovelInput


class PredictBatchRequest(BaseModel):

    data: list[ImovelInput] = Field(
        ...,
        min_length=1,
        description="Lista de imóveis para previsão em lote."
    )

# ==========================================================
# 5. VARIÁVEIS GLOBAIS DO MODELO
# ==========================================================

MODEL_ARTIFACT: Any = None
MODEL = None
SCALER = None
FEATURES: list[str] | None = None
METRICS: dict[str, Any] | None = None

# ==========================================================
# 6. CARREGAMENTO DO MODELO NO STARTUP
# ==========================================================

@app.on_event("startup")
def load_artifact() -> None:

    global MODEL_ARTIFACT, MODEL, SCALER, FEATURES, METRICS

    if not MODEL_PATH.exists():
        raise RuntimeError(
            f"Modelo não encontrado em: {MODEL_PATH}"
        )

    MODEL_ARTIFACT = joblib.load(MODEL_PATH)

    if isinstance(MODEL_ARTIFACT, dict):
        MODEL = MODEL_ARTIFACT.get("model")
        SCALER = MODEL_ARTIFACT.get("scaler")
        FEATURES = MODEL_ARTIFACT.get("features")
        METRICS = MODEL_ARTIFACT.get("metrics")

    else:
        MODEL = MODEL_ARTIFACT
        SCALER = None
        FEATURES = None
        METRICS = None

    if MODEL is None:
        raise RuntimeError(
            "Artefato carregado, mas sem objeto de modelo válido."
        )

    if FEATURES is None and hasattr(
        MODEL,
        "feature_names_in_"
    ):
        FEATURES = list(MODEL.feature_names_in_)
        
# ==========================================================
# 7. ENDPOINT DE SAÚDE DA API
# ==========================================================

@app.get("/health")
def health() -> dict[str, Any]:

    return {
        "status": "ok",
        "model_path": str(MODEL_PATH),
        "has_scaler": SCALER is not None,
        "n_features": (
            len(FEATURES)
            if FEATURES is not None
            else None
        )
    }

# ==========================================================
# 8. ENDPOINT DE INFORMAÇÕES DO MODELO
# ==========================================================

@app.get("/model-info")
def model_info() -> dict[str, Any]:

    return {
        "model_type": type(MODEL).__name__,
        "has_scaler": SCALER is not None,
        "features": FEATURES,
        "model_path": str(MODEL_PATH)
    }

# ==========================================================
# 9. ENDPOINT DE MÉTRICAS DO MODELO
# ==========================================================

@app.get("/metrics")
def metrics() -> dict[str, Any]:

    if METRICS is None:
        raise HTTPException(
            status_code=404,
            detail="Métricas do modelo não disponíveis."
        )

    return METRICS

# ==========================================================
# 10. PREPARAÇÃO E VALIDAÇÃO DOS DADOS DE ENTRADA
# ==========================================================

def _prepare_input(
    records: list[dict[str, Any]]
) -> pd.DataFrame:

    if not records:
        raise HTTPException(
            status_code=422,
            detail="Entrada vazia."
        )

    df = pd.DataFrame(records)

    if FEATURES is not None:

        missing = [
            feature
            for feature in FEATURES
            if feature not in df.columns
        ]

        if missing:
            raise HTTPException(
                status_code=422,
                detail={
                    "error": "Colunas ausentes para o modelo.",
                    "missing_features": missing
                }
            )

        df = df.reindex(
            columns=FEATURES
        )

    for col in df.columns:

        converted = pd.to_numeric(
            df[col],
            errors="coerce"
        )

        invalid_mask = (
            converted.isna()
            & df[col].notna()
        )

        if invalid_mask.any():

            bad_rows = (
                invalid_mask[
                    invalid_mask
                ]
                .index
                .tolist()
            )

            raise HTTPException(
                status_code=422,
                detail={
                    "error": (
                        f"Valores inválidos "
                        f"na coluna '{col}'."
                    ),
                    "rows": bad_rows
                }
            )

        df[col] = converted

    if df.isna().any().any():

        missing_info = {}

        for col in df.columns:

            rows = (
                df.index[
                    df[col].isna()
                ]
                .tolist()
            )

            if rows:
                missing_info[col] = rows

        raise HTTPException(
            status_code=422,
            detail={
                "error": (
                    "Existem valores nulos "
                    "após a validação."
                ),
                "null_positions": missing_info
            }
        )

    if SCALER is not None:

        scaled = SCALER.transform(df)

        df = pd.DataFrame(
            scaled,
            columns=df.columns,
            index=df.index
        )

    return df

# ==========================================================
# 11. FUNÇÃO DE PREDIÇÃO
# ==========================================================

def _predict(
    records: list[dict[str, Any]]
) -> dict[str, Any]:

    x = _prepare_input(records)

    predictions = MODEL.predict(x)

    return {
        "n_records": len(records),
        "predictions": predictions.tolist()
    }

# ==========================================================
# 12. ENDPOINT DE PREDIÇÃO UNITÁRIA
# ==========================================================

@app.post("/predict")
def predict_single(
    payload: PredictRequest
) -> dict[str, Any]:

    out = _predict(
        [payload.data.model_dump()]
    )

    return {
        "prediction": out["predictions"][0]
    }

# ==========================================================
# 13. ENDPOINT DE PREDIÇÃO EM LOTE
# ==========================================================

@app.post("/predict-batch")
def predict_batch(
    payload: PredictBatchRequest
) -> dict[str, Any]:

    return _predict(
        [
            imovel.model_dump()
            for imovel in payload.data
        ]
    )
