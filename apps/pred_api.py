from flask import Flask
from flask_restful import Resource, Api, reqparse
app = Flask(__name__)
api = Api(app)
import h2o
import pandas as pd
h2o.init()
## load saved model
model_path = 'StackedEnsemble_AllModels_AutoML_20200619_******'
uploaded_model = h2o.load_model(model_path)
# argument parsing
parser = reqparse.RequestParser(bundle_errors=True) #if there are 2 errors, both's msg will be printed
parser.add_argument('age_group', choices = ('Young', 'Older', 'Middle-Aged'), help = 'Bad Choice: {error_msg}. Valid choices are Young, Older, Middle-Aged')
parser.add_argument('car_type', choices = ('SUV', 'Saloon', 'Convertible'), help = 'Bad Choice: {error_msg}. Valid choices are SUV, Saloon, Convertible')
parser.add_argument('loanamount')
parser.add_argument('deposit')
parser.add_argument('area', choices = ('urban', 'rural'), help = 'Bad Choice: {error_msg}. Valid choices are urban, rural')
#Categorical Columns - enum
#Numerical Columns - real
col_dict = {'age_group' : 'enum', 
            'car_type' : 'enum', 
            'loanamount' : 'real', 
            'deposit' : 'real', 
            'area' : 'enum',
           'application_outcome': 'enum'}
#prepare empty test data frame to be fed to the model
data = {}
# results dict
item_dict = {}
class LoanPred(Resource):
    def get(self):
         args = parser.parse_args()
         age = args['age_group']
         car_type = args['car_type']
         loanamount = float(args['loanamount'])
         deposit = float(args['deposit'])
         area = args['area']
         application_outcome = 'declined' 
         
         # put key:value pairs in empty dict called data
         data['age_group'] = age
         data['car_type'] = car_type
         data['loanamount'] = [loanamount]
         data['deposit'] = [deposit]
         data['area'] = area
         data['application_outcome'] = application_outcome
         
         # creating dataframe from dict
         testing = pd.DataFrame(data)
         
         # converting pandas to h2o dataframe
         test = h2o.H2OFrame(testing, column_types = col_dict)
        
         # making predictions
         pred_ans = uploaded_model.predict(test).as_data_frame()
         
         # put key:value pairs in empty dict called item_dict
         item_dict['Prediction'] = pred_ans.predict.values[0]
         item_dict['Approved'] = pred_ans.approved.values[0]
         item_dict['Declined'] = pred_ans.declined.values[0]
         
         return{'ans': item_dict}
         
api.add_resource(LoanPred, '/')
if __name__ == '__main__':
    app.run(debug=True, port= 1234)