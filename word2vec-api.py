'''
Simple web service wrapping a Word2Vec as implemented in Gensim
Example call: curl http://127.0.0.1:5000/wor2vec/n_similarity/ws1=Sushi&ws1=Shop&ws2=Japanese&ws2=Restaurant
@TODO: Add more methods
@TODO: Add command line parameter: path to the trained model
@TODO: Add command line parameters: host and port
'''

from flask import Flask, request, jsonify
from flask.ext.restful import Resource, Api, reqparse
from gensim.models.word2vec import Word2Vec as w
from gensim import utils, matutils
from numpy import exp, dot, zeros, outer, random, dtype, get_include, float32 as REAL,\
    uint32, seterr, array, uint8, vstack, argsort, fromstring, sqrt, newaxis, ndarray, empty, sum as np_sum

model = w.load_word2vec_format('/var/data/GoogleNews-vectors-negative300.bin.gz',binary=True)

class N_Similarity(Resource):
    def get(self):
        args = parser.parse_args()
        return model.n_similarity(args['ws1'],args['ws2'])

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('ws1', type=str, required=True, help="Word set 1 cannot be blank!", action='append')
parser.add_argument('ws2', type=str, required=True, help="Word set 2 cannot be blank!", action='append')

api.add_resource(N_Similarity, '/word2vec/n_similarity')

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
