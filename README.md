word2vec-api
============

Simple web service providing a word embedding API. The methods are based on Gensim Word2Vec implementation. Models are passed as parameters and must be in the Word2Vec text or binary format.

* Launching the service
```
python word2vec-api --model path/to/the/model [--host host --port 1234]
```

* Example calls
```
curl http://127.0.0.1:5000/wor2vec/n_similarity?ws1=Sushi&ws1=Shop&ws2=Japanese&ws2=Restaurant  
curl http://127.0.0.1:5000/wor2vec/similarity?w1=Sushi&w2=Japanese   
curl http://127.0.0.1:5000/wor2vec/most_similar?positive=indian&positive=food[&negative=][&topn=]
curl http://127.0.0.1:5000/wor2vec/model?word=restaurant
```

Note: The "model" method returns a base64 encoding of the Word2Vec vector.
