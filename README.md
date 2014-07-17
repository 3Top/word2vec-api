word2vec-api
============

Simple web service wrapping a Word2Vec as implemented in Gensim.

* Launching the service
<blockquote>
 python word2vec-api --model path/to/the/model [--host host --port 1234]
</blockquote>

* Example calls
<blockquote>
 curl http://127.0.0.1:5000/wor2vec/n_similarity?ws1=Sushi&ws1=Shop&ws2=Japanese&ws2=Restaurant
 curl  http://127.0.0.1:5000/wor2vec/similarity?w1=Sushi&w2=Japanese
 curl  http://127.0.0.1:5000/wor2vec/most_similar?positive=indian&positive=food[&negative=][&topn=]
</blockquote>
