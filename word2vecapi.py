'''
Simple web service wrapping a Word2Vec as implemented in Gensim
Example call: curl http://127.0.0.1:5000/n_similarity/ws1=Sushi&ws1=Shop&ws2=Japanese&ws2=Restaurant
@TODO: Add more methods
@TODO: Add command line parameter: path to the trained model
@TODO: Add command line parameters: host and port
'''

from flask import Flask, request, jsonify, render_template
from flask.ext.restful import Resource, Api, reqparse
from gensim.models.word2vec import Word2Vec as w
from gensim import utils, matutils
from numpy import exp, dot, zeros, outer, random, dtype, get_include, float32 as REAL,\
     uint32, seterr, array, uint8, vstack, argsort, fromstring, sqrt, newaxis, ndarray, empty, sum as np_sum
import argparse
import base64
import sys
import re

import conf

# parser = reqparse.RequestParser()


def filter_words(words):
    if words is None:
        return
    return [word for word in words if word in model.vocab]


def dump_index(vocab):
    """Clears all non alpha/underscore words from the vocab and writes it to a space delimited file."""
    ok_words = re.compile('[^\w]')
    index_list = []
    for word in model.vocab:
        if not ok_words.search(word):
            index_list.append(word)
    with open('./model_index.txt', 'wb') as index_file:
        index_file.write(' '.join(index_list))


class SearchTerms(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('q', type=str, required=True, help="Word or characters to search for")
        args = parser.parse_args()
        ss = args['q'].lower()
        # res = [k for k in model.vocab if ss.lower() in k.lower()]
        res = [value for (key, value) in vocab_index.iteritems() if ss in key]
        return res


class NSimilarity(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ws1', type=str, required=True, help="Word set 1 cannot be blank!", action='append')
        parser.add_argument('ws2', type=str, required=True, help="Word set 2 cannot be blank!", action='append')
        args = parser.parse_args()
        return model.n_similarity(filter_words(args['ws1']), filter_words(args['ws2']))


class Similarity(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('w1', type=str, required=True, help="Word 1 cannot be blank!")
        parser.add_argument('w2', type=str, required=True, help="Word 2 cannot be blank!")
        args = parser.parse_args()
        return model.similarity(args['w1'], args['w2'])


class MostSimilar(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('positive', type=str, required=False, help="Positive words", action='append')
        parser.add_argument('negative', type=str, required=False, help="Negative words", action='append')
        parser.add_argument('topn', type=int, required=False, help="Number of results")
        args = parser.parse_args()
        pos = filter_words(args.get('positive', []))
        neg = filter_words(args.get('negative', []))
        t = args.get('topn', 10)
        pos = [] if pos is None else pos
        neg = [] if neg is None else neg
        t = 10 if t is None else t
        print "positive: " + str(pos) + " negative: " + str(neg) + " topn: " + str(t)  
        try:    
            res = model.most_similar_cosmul(positive=pos, negative=neg, topn=t)
            return jsonify(res)
        except Exception as e:
            raise pagenotfound(e)


class Model(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('word', type=str, required=True, help="word to query.")
        args = parser.parse_args()
        try:
            res = model[args['word']]
            res = base64.b64encode(res)
            return res
        except Exception as e:
            raise pagenotfound(e)

app = Flask(__name__)
api = Api(app)
# app.debug = True


@app.errorhandler(404)
@app.errorhandler(500)
def pagenotfound(error):
    return "Requested query had no result", 500


@app.route('/')
def search_root():
    return render_template('index.html')


@app.route('/api')
def api_docs():
    return render_template('restapi.html')

api.add_resource(NSimilarity, '/n_similarity')
api.add_resource(Similarity, '/similarity')
api.add_resource(MostSimilar, '/most_similar')
api.add_resource(Model, '/model')
api.add_resource(SearchTerms, '/search')

# Import model for use
model = w.load_word2vec_format(conf.model_path, binary=conf.binary)
# precalculate lowercase index of terms in model for fast search
vocab_index = {}
for k in model.vocab:
    vocab_index[k.lower()] = k

if __name__ == '__main__':
    app.run(host=conf.host, port=conf.port)
