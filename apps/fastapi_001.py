'''
API for H2O Model

    fastapi version
    Documentation at: https://fastapi.tiangolo.com/
'''

'''
To start: uvicorn __name__:app --reload 
'''

from typing import Union

from pyrsistent import s

from fastapi import FastAPI
from pydantic import BaseModel


# H2O
import h2o
import pandas as pd
import json
h2o.init()
## load saved model
model_path = '../models/StackedEnsemble_AllModels_3_AutoML_1_20220615_221514'
uploaded_model = h2o.load_model(model_path)

def prediction(model, json_obj=None):
    '''
    Provided an H2O model and a dataframe with predictors, 
    calculate predictions'''

    if json_obj is None:
        json_obj=[{
        'diagnosis': 'M',
        'radius_mean': 11.34,
        'texture_mean': 15.26,
        'perimeter_mean': 10.5,
        'area_mean': 920.4,
        'smoothness_mean': 0.1073,
        'compactness_mean': 0.2135,
        'concavity_mean': 0.2077,
        'concave points_mean': 0.09756,
        'symmetry_mean': 0.2521,
        'fractal_dimension_mean': 0.27032,

        'radius_se': 0.4388,
        'texture_se': 0.7096,
        'perimeter_se': 4.384,
        'area_se': 44.91,
        'smoothness_se': 0.006789,
        'compactness_se': 0.05328,
        'concavity_se': 0.01446,
        'concave points_se': 0.02252,
        'symmetry_se': 0.03672,
        'fractal_dimension_se': 0.004394,

        'radius_worst': 14.07,
        'texture_worst': 12.08,
        'perimeter_worst': 125.1,
        'area_worst': 980.9,
        'smoothness_worst': 0.139,
        'compactness_worst': 0.5954,
        'concavity_worst': 0.6305,
        'concave points_worst': 0.2393,
        'symmetry_worst': 0.4667,
        'fractal_dimension_worst': 0.09946}]
    
    # Upload model
    df = pd.DataFrame(data = json_obj)
    to_predict = h2o.H2OFrame(df)
    uploaded_model = model
    
    return json.loads(uploaded_model.predict(to_predict).as_data_frame().to_json(orient='records'))


# Define the Model  
class Model_01_Payload(BaseModel):
    diagnosis: str

    radius_mean: float
    texture_mean: float
    perimeter_mean: float
    area_mean: float
    smoothness_mean: float
    compactness_mean: float
    concavity_mean: float
    concave_points_mean: float
    symmetry_mean: float
    fractal_dimension_mean: float

    radius_se: float
    texture_se: float
    perimeter_se: float
    area_se: float
    smoothness_se: float
    compactness_se:float
    concavity_se: float
    concave_points_se:float
    symmetry_se:float
    fractal_dimension_se: float

    radius_worst:float
    texture_worst: float
    perimeter_worst: float
    area_worst: float
    smoothness_worst: float
    compactness_worst: float
    concavity_worst: float
    concave_points_worst: float
    symmetry_worst: float
    fractal_dimension_worst: float



app = FastAPI()


# Entry point

@app.post("/model_01/")
async def create_item(plModel_01: Model_01_Payload):
    response = prediction(uploaded_model)
    plModel_01.diagnosis = response
    return plModel_01