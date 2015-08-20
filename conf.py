import os
if os.name == 'nt':
    model_path = 'F:\Dropbox\word2vec-api\models\GoogleNews-vectors-negative300.bin'
else:
    model_path = "/srv/repos/word2vec-api/models/GoogleNews-vectors-negative300.bin"
binary = True
host = "localhost"
port = 3031