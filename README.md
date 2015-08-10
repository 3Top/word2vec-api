word2vec-api
============

Reworking of https://github.com/3Top/word2vec-api to add:

* deployment via ssl on nginx / uwsgi
* TODO: meaningful errors when a term is not available
* TODO: Cleaned Output

Simple web service providing a word embedding API. 

The methods are based on Gensim Word2Vec implementation. 

Parameters are set in conf.py for ease of use with uwsgi

---

## Environment Setup and usage notes

* This variant of word2vec-api was developed on an AWS Centos x64 6.5 instance using Pycharm 4.5.3
* The main requirement was enough ram to load the Google News model, so an m3.xlarge (16Gb ram) instance was used.
* A virtualenv with Python 2.7.9 was created, and populated with the provided requirements.txt.
* Note that to get Scipy and Numpy working properly for gensim you may have to install yum packages as root, see the specific documentation for installing those packages for your OS.
* To run this as non-root user, you may have to create and permission /var/log/uwsgi.log appropriately.
* Each time you launch the script it will import the model specified in the conf file - it is significantly faster if you unzip it first.

You can download the Google News Vectors as a test model using the following linux command:

    wget https://www.googledrive.com/host/0B7XkCwpI5KDYNlNUTTlSS21pQmM -O GoogleNews-vectors-negative300.bin.gz

### Example calls

    curl http://127.0.0.1:3031/n_similarity?ws1=Sushi&ws1=Shop&ws2=Japanese&ws2=Restaurant
    curl http://127.0.0.1:3031/similarity?w1=Sushi&w2=Japanese
    curl http://127.0.0.1:3031/most_similar?positive=indian&positive=food[&negative=][&topn=]
    curl http://127.0.0.1:3031/model?word=restaurant

Note: The "model" method returns a base64 encoding of the Word2Vec vector.

---

## Where to get a pretrained model

In case you do not have domain specific data to train, it can be convenient to use a pretrained model. 
Please feel free to submit additions to this list through a pull request.
 
 
| Model file | Number of dimensions | Corpus (size)| Vocabulary size | Author | Architecture | Training Algorithm | Context window - size | Web page |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Google News](GoogleNews-vectors-negative300.bin.gz) | 300 |Google News (100B) | 3M | Google | word2vec | negative sampling | BoW - ~5| [link](http://code.google.com/p/word2vec/) |
| [Freebase IDs](https://docs.google.com/file/d/0B7XkCwpI5KDYaDBDQm1tZGNDRHc/edit?usp=sharing) | 1000 | Gooogle News (100B) | 1.4M | Google | word2vec, skip-gram | ? | BoW - ~10 | [link](http://code.google.com/p/word2vec/) |
| [Freebase names](https://docs.google.com/file/d/0B7XkCwpI5KDYeFdmcVltWkhtbmM/edit?usp=sharing) | 1000 | Gooogle News (100B) | 1.4M | Google | word2vec, skip-gram | ? | BoW - ~10 | [link](http://code.google.com/p/word2vec/) |
| [Wikipedia+Gigaword 5](http://www-nlp.stanford.edu/data/glove.6B.50d.txt.gz) | 50 | Wikipedia+Gigaword 5 (6B) | 400,000 | GloVe | GloVe | AdaGrad | 10+10 | [link](http://nlp.stanford.edu/projects/glove/) |
| [Wikipedia+Gigaword 5](http://www-nlp.stanford.edu/data/glove.6B.100d.txt.gz) | 100 | Wikipedia+Gigaword 5 (6B) | 400,000 | GloVe | GloVe | AdaGrad | 10+10 | [link](http://nlp.stanford.edu/projects/glove/) |
| [Wikipedia+Gigaword 5](http://www-nlp.stanford.edu/data/glove.6B.200d.txt.gz) | 200 | Wikipedia+Gigaword 5 (6B) | 400,000 | GloVe | GloVe | AdaGrad | 10+10 | [link](http://nlp.stanford.edu/projects/glove/) |
| [Wikipedia+Gigaword 5](http://www-nlp.stanford.edu/data/glove.6B.300d.txt.gz) | 300 | Wikipedia+Gigaword 5 (6B) | 400,000 | GloVe | GloVe | AdaGrad | 10+10 | [link](http://nlp.stanford.edu/projects/glove/) |
| [Common Crawl 42B](http://www-nlp.stanford.edu/data/glove.42B.300d.txt.gz) | 300 | Common Crawl (42B) | ~2M | GloVe | GloVe | GloVe | AdaGrad | [link](http://nlp.stanford.edu/projects/glove/) |
| [Twitter (2B Tweets)](http://www-nlp.stanford.edu/data/glove.twitter.27B.25d.txt.gz) | 25 | Twitter (27B) | ? | GloVe | GloVe | GloVe | AdaGrad | [link](http://nlp.stanford.edu/projects/glove/) |
| [Twitter (2B Tweets)](http://www-nlp.stanford.edu/data/glove.twitter.27B.50d.txt.gz) | 50 | Twitter (27B) | ? | GloVe | GloVe | GloVe | AdaGrad | [link](http://nlp.stanford.edu/projects/glove/) |
| [Twitter (2B Tweets)](http://www-nlp.stanford.edu/data/glove.twitter.27B.100d.txt.gz) | 100 | Twitter (27B) | ? | GloVe | GloVe | GloVe | AdaGrad | [link](http://nlp.stanford.edu/projects/glove/) |
| [Twitter (2B Tweets)](http://www-nlp.stanford.edu/data/glove.twitter.27B.200d.txt.gz) | 200 | Twitter (27B) | ? | GloVe | GloVe | GloVe | AdaGrad | [link](http://nlp.stanford.edu/projects/glove/) |
| [Wikipedia dependency](http://u.cs.biu.ac.il/~yogo/data/syntemb/deps.words.bz2) | 300 | Wikipedia (?) | 174,015 | Levy \& Goldberg | word2vec modified | word2vec | syntactic dependencies | [link](https://levyomer.wordpress.com/2014/04/25/dependency-based-word-embeddings/) |
| [DBPedia vectors](https://github.com/idio/wiki2vec/raw/master/torrents/enwiki-gensim-word2vec-1000-nostem-10cbow.torrent) | 1000 | Wikipedia (?) | ? | wiki2vec | word2vec | word2vec, skip-gram | BoW, 10 | [link](https://github.com/idio/wiki2vec#prebuilt-models) |



