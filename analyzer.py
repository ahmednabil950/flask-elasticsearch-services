from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class WatsonAnalyzer:
    def __init__(self, **kwargs):
        self.CATEGORIES = ['anger', 'fear', 'joy', 'sadness', 'analytical', 'confident', 'tentative']
        self.__URL = 'https://gateway-lon.watsonplatform.net/tone-analyzer/api'
        self.__auth = IAMAuthenticator(apikey=kwargs['apikey'])
        self._analyzer = ToneAnalyzerV3(version=kwargs['version'], authenticator=self.__auth)
        self._analyzer.set_service_url(self.__URL)
        
    def analyze(self, query):
        """watson api actual analyzer is made here
        
        Arguments:
            query {bytes} -- serialized sentence (bytes representation) separated by '\n'
                    formatted this way to send multiple sentences at once to watson api
                    in which watson will tokenize and return emotional analysis for each sentence
        
        Returns:
            {dict} -- normalized scores for all sentence analysis
        """
        tone_analyzer = self._analyzer
        val = {'text': query}
        result_json = tone_analyzer.tone(val, content_type='application/json').get_result()
        
        try:
            tones = result_json['sentences_tone']
        except KeyError:
            tones = result_json['document_tone']
            tones = [{'sentence_id': 0, 'text': query, 'tones': []}]
        scores = self.normalize_tones_scores(tones)
        
        return scores
    
    def normalize_tones_scores(self, tones):
        """Normalize the scores of all sentence returned from ibm watson analyzer
        
        Arguments:
            tones {dict} -- sentence emotional tones returned from watson api
        
        Returns:
            {dict} -- {'tone_id': 'normalized score', 'tone_id': 'normalized score',}
        """
        norm_scores = {}
        tones_count = {}
        for analysis in tones:
            for scores in analysis['tones']:
                if scores['tone_id'] not in norm_scores:
                    tones_count[scores['tone_id']] = 1
                    norm_scores[scores['tone_id']] = 0
                else:
                    tones_count[scores['tone_id']] += 1
                    norm_scores[scores['tone_id']] += scores['score']
        return {k: v/tones_count[k] for (k, v) in norm_scores.items()}