import json
from flask import Flask, jsonify, request
from tools import cleaner_job
from analyzer import WatsonAnalyzer
from elastic import ElasticDocument

# flask instannce
app = Flask("Tone Analyzer ES")

# configurations
app.config['MAX_CONTENT_LENGTH'] = 1600 * 1024 * 1024

# -------------------------------------------- #
# Tone Analyzer End point                      #
# -------------------------------------------- #
@app.route('/analyzer/', methods=['POST'])
def analyzer():
    analyzer = WatsonAnalyzer(
        version='2017-09-21', 
        apikey='{api_key}')
    
    data_json = json.loads(request.get_data())
    queries = {k: cleaner_job(v) for (k, v) in data_json.items()}
    
    # depend on ibm analyzer tokenizer | prepare the format accordingly
    queries = "\n".join(list(queries.values()))
    tones = analyzer.analyze(queries)
    
    return tones

# -------------------------------------------- #
# Elastic Search Queries Indexer End point     #
# -------------------------------------------- #
@app.route('/indexer/', methods=['POST'])
def indexer():
    document = ElasticDocument(host='127.0.0.1', port=9200)
    analyzer = WatsonAnalyzer(
        version='2017-09-21', 
        apikey='{api_key}')
    
    # de-serialize data from request
    data = json.loads(request.get_data())
    
    documents = []
    for doc, contents in data.items():
        # depend on ibm analyzer tokenizer | prepare the format accordingly
        queries = {k: cleaner_job(v['reviews.text']) for (k, v) in contents.items()}
        queries = "\n".join(list(queries.values()))
        tones = analyzer.analyze(queries)
        
        # prepare the format for es indexer
        documents.append({'data': contents, 'tones': tones})
    
    result = document.create(index='reviews', doc_type='hotels', body_docs=documents)
    return result

if __name__ == '__main__':
    app.run(threaded=False, port=5000)