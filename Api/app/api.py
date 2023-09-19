from fastapi import FastAPI
from pydantic import BaseModel
import pickle as pk
import pandas as pd

Maize_model = pk.load(open('Maize_model_XGBoost Regressor.pkl', 'rb'))
Beans_model = pk.load(open('Beans_model_XGBoost Regressor.pkl', 'rb'))
Rice_model = pk.load(open('Rice_model_XGBoost Regressor.pkl', 'rb'))


app = FastAPI()

columns_name = [
    'market',
    'year',
    'month',
    'years_since_start',
    'past_1_months_mean_price',
    'past_2_months_mean_price',
    'past_3_months_mean_price',
    'past_4_months_mean_price',
    'past_5_months_mean_price',
    'past_6_months_mean_price',
    'past_7_months_mean_price',
    'past_8_months_mean_price',
    'past_9_months_mean_price',
    'past_10_months_mean_price',
    'past_11_months_mean_price',
    'past_1_years_mean_price',
    'past_2_years_mean_price',
    'past_3_years_mean_price',
    'past_4_years_mean_price',
    'past_5_years_mean_price',
    'past_6_years_mean_price',
    'past_7_years_mean_price',
    'past_8_years_mean_price',
    'past_9_years_mean_price',
    'past_10_years_mean_price',
    'past_11_years_mean_price',
    'past_12_years_mean_price',
    'past_13_years_mean_price',
    'past_14_years_mean_price',
    'past_15_years_mean_price',
    'past_16_years_mean_price',
    'past_17_years_mean_price',
    'yearly_average_price',
    'monthly_average_price',
    'market_average_price',
    'commodity_yearly_average_price',
    'commodity_monthly_average_price'
]


class Item(BaseModel):
    market: int
    year: int
    month: int
    years_since_start: int
    past_1_months_mean_price: float
    past_2_months_mean_price: float
    past_3_months_mean_price: float
    past_4_months_mean_price: float
    past_5_months_mean_price: float
    past_6_months_mean_price: float
    past_7_months_mean_price: float
    past_8_months_mean_price: float
    past_9_months_mean_price: float
    past_10_months_mean_price: float
    past_11_months_mean_price: float
    past_1_years_mean_price: float
    past_2_years_mean_price: float
    past_3_years_mean_price: float
    past_4_years_mean_price: float
    past_5_years_mean_price: float
    past_6_years_mean_price: float
    past_7_years_mean_price: float
    past_8_years_mean_price: float
    past_9_years_mean_price: float
    past_10_years_mean_price: float
    past_11_years_mean_price: float
    past_12_years_mean_price: float
    past_13_years_mean_price: float
    past_14_years_mean_price: float
    past_15_years_mean_price: float
    past_16_years_mean_price: float
    past_17_years_mean_price: float
    yearly_average_price: float
    monthly_average_price: float
    market_average_price: float
    commodity_yearly_average_price: float
    commodity_monthly_average_price: float


@app.get('/')
async def get_home():
    return {"Do you know where you are going?":"NO!, you don't 😂"}

@app.post('/predict-maize')
async def predict_maize_price(inputValues: Item):
    data = pd.DataFrame(
        [inputValues.model_dump().values()], columns=columns_name)
    prediction = Maize_model.predict(data)
    return float(prediction)


@app.post('/predict-beans')
async def predict_beans_price(inputValues: Item):
    data = pd.DataFrame(
        [inputValues.model_dump().values()], columns=columns_name)
    prediction = Beans_model.predict(data)
    return float(prediction)


@app.post('/predict-rice')
async def predict_rice_price(inputValues: Item):
    data = pd.DataFrame(
        [inputValues.model_dump().values()], columns=columns_name)
    prediction = Rice_model.predict(data)
    return float(prediction)
