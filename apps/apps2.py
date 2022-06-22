from flask import Flask,jsonify
from flask_restful import Resource, Api, reqparse
app = Flask(__name__)
api = Api(app)
# argument parsing
parser = reqparse.RequestParser()
parser.add_argument('num1')
class HelloWorld(Resource):
    def get(self):
        return jsonify({'hello': 'world'})
        
class PrintSquare(Resource):
    def get(self):
        # use parser and find the user's input
        args = parser.parse_args()
        
        user_query = float(args['num1'])
        return jsonify({'ans': user_query * user_query})

api.add_resource(HelloWorld, '/hello')
api.add_resource(PrintSquare, '/sq')
if __name__ == '__main__':
    app.run(debug=True, port = 12345)