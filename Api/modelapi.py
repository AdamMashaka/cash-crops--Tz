from fastapi import FastAPI
from pydantic import BaseModel
import pickle as pk
import pandas as pd

Maize_model = pk.load(open('../Models/Maize/Maize_model_CatBoost Regressor.pkl', 'rb'))


app = FastAPI()

column_names = [
    "year",
    "month",
    "years_since_start",
    "past_three_months_mean_price",
    "past_six_months_mean_price",
    "past_twelve_months_mean_price",
    "yearly_average_price",
    "monthly_average_price",
    "market_average_price",
    "commodity_yearly_average_price",
    "commodity_monthly_average_price",
    "market_Arusha (urban)",
    "market_Babati",
    "market_Bukoba",
    "market_Dar es Salaam - Ilala",
    "market_Dar es Salaam - Kinondoni",
    "market_Dodoma (Kibaigwa)",
    "market_Dodoma (Majengo)",
    "market_Morogoro",
    "market_Mpanda",
    "market_Mtwara DC",
    "market_Musoma",
    "market_Tabora",
    "market_Tanga / Mgandini"
]


class Item(BaseModel):
    year: float
    month: int
    years_since_start: int
    past_three_months_mean_price: float
    past_six_months_mean_price: float
    past_twelve_months_mean_price: float
    yearly_average_price: float
    monthly_average_price: float
    market_average_price: float
    commodity_yearly_average_price: float
    commodity_monthly_average_price: float
    market_Arusha_urban: int
    market_Babati: int
    market_Bukoba: int
    market_Dar_es_Salaam_Ilala: int
    market_Dar_es_Salaam_Kinondoni: int
    market_Dodoma_Kibaigwa: int
    market_Dodoma_Majengo: int
    market_Morogoro: int
    market_Mpanda: int
    market_Mtwara_DC: int
    market_Musoma: int
    market_Tabora: int
    market_Tanga_Mgandini: int

@app.post('/predict-maize')
async def get_endpoint(inputValues:Item):
    data = pd.DataFrame([inputValues.model_dump().values()], columns=column_names)
    prediction = Maize_model.predict(data)
    return float(prediction)

@app.post('/predict-beans')
async def get_endpoint(inputValues:Item):
    return inputValues

@app.post('/predict-rice')
async def get_endpoint(inputValues:Item):
    return inputValues