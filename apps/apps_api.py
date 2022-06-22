'''
API for H2O Model
'''
from flask import Flask, jsonify, request
from flask_restful import Api,Resource

# H2O
import h2o
import pandas as pd
h2o.init()
## load saved model
model_path = '../models/StackedEnsemble_AllModels_3_AutoML_1_20220615_221514'
uploaded_model = h2o.load_model(model_path)


def prediction(model, json_obj=None):
    '''
    Provided an H2O model and a dataframe with predictors, 
    calculate predictions'''

    if json_obj is None:
        json_obj=[{'diagnosis': 'M',
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
    
    return uploaded_model.predict(to_predict).as_data_frame().to_json(orient='records')


app = Flask(__name__)
api = Api(app)




class Help(Resource):
    '''
    Implement the Help Resource'''
    def get(self):
        retJson = {
            "status": 200,
            "msg": "This API can be used to apply a ML"
        }
        return jsonify(retJson)

class Predict(Resource):
    '''
    Apply the model to the input parameters'''

    def post(self):

        postedData = request.get_json()

        ans=prediction(uploaded_model)
        retJson = {
            "status": 200,
            "msg": "Prediction is...",
            "params": postedData,
            "answer":ans

        }
        return jsonify(retJson)
    

api.add_resource(Help, '/help')
api.add_resource(Predict, '/predict')



if __name__=="__main__":
    app.run(host='0.0.0.0', port=5002)

