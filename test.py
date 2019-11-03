import unittest
from analyzer import WatsonAnalyzer

class ToolsTest(unittest.TestCase):
    def setUp(self):
        # initialization is mad here
        return super().setUp()
    
    
class AnalyzerTest(unittest.TestCase):
    def setUp(self):
        # initialization is made here
        self.analyzer = WatsonAnalyzer(version='2017-09-21', 
                                       apikey='qvl86uV_4tcH91R4g54dFeSHqxsPq-lZzDb4u8Ko2exi')
        return super().setUp()
    
    def test_analyze(self):
        query = "Hello how are you\n"\
                "I love this hotel\n"\
                "I live there for 30 years"
        self.assertIsInstance(self.analyzer.analyze(query), dict)
                
        query = "Hello how are you"\
                "I love this hotel"\
                "I live there for 30 years"
        self.assertRaises(KeyError, self.analyzer.analyze, query)
        
    # def test_normalize_tones_scores(self):
    #     scoress = []
    #     self.assertIsInstance(self.analyzer.normalize_tones_scores(query), dict)
        
        
        
    
class AppTest(unittest.TestCase):
    def setUp(self):
        # initialization is mad here
        return super().setUp()
    

if __name__ == "__main__":
    unittest.main()