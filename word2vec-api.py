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
import argparse


class N_Similarity(Resource):
    def get(self):
        args = parser.parse_args()
	print(parser.parse_args())
        return model.n_similarity(args['ws1'],args['ws2'])

app = Flask(__name__)
api = Api(app)

@app.errorhandler(404)
def pageNotFound(error):
    return "page not found"

parser = reqparse.RequestParser()
parser.add_argument('ws1', type=str, required=True, help="Word set 1 cannot be blank!", action='append')
parser.add_argument('ws2', type=str, required=True, help="Word set 2 cannot be blank!", action='append')

api.add_resource(N_Similarity, '/word2vec/n_similarity')
api.add_resource(Similarity, '/word2vec/similarity')
api.add_resource(MostSimilar, '/word2vec/most_similar')

if __name__ == '__main__':
    global model
    
    #----------- Parsing Arguments ---------------
    p = argparse.ArgumentParser()
    p.add_argument("--model", help="Path to the trained model")
    p.add_argument("--host", help="Host name (default: localhost)")
    p.add_argument("--port", help="Port (default: 5000)")
    args = p.parse_args()
    
    model_path = args.model if args.model else "./model.bin.gz"
    host = args.host if args.host else "localhost"
    port = int(args.port) if args.port else 5000
    if not args.model:
	print "Usage: wor2vec-apy.py --model path/to/the/model [--host host --port 1234]"
    model = w.load_word2vec_format(model_path, binary=True)
    app.run(host=host, port=port) 
        
