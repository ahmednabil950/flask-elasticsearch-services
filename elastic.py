from elasticsearch import Elasticsearch, helpers
import json

class ElasticDocument:
    def __init__(self, *args, **kw):
        """Connection is made to elasticsearch server and binded according to the given params
        
        Raises:
            ValueError: if Invalid named or positional args doesn't match
        """
        if len(args):
            self.es = Elasticsearch([{'host': args[0], 'port': args[1]}])
        elif len(kw):
            self.es = Elasticsearch([{'host': kw['host'], 'port': kw['port']}])
        else:
            raise ValueError('Invalid Arguments for Document Constructor')
        
    def create(self, index, doc_type, body_docs):
        """ElasticSearch Bulk Creation in Single API call to index multiple documents at once
        
        Arguments:
            index {str} -- index (database) that will be used to store the documents
            doc_type {str} -- document type (table) that will be used to represent document category
            body_docs {dict} -- actual data that will be stored
            {
                'data': {'0': ....}, {'1': ....}, .. ... .. .. },
                'tones': {'watson api analysis scores'}
            }
        
        Returns:
            dict -- elasticsearch json scheme of the transaction of status
        """
        if not self.es.indices.exists(index):
            self.es.indices.create(index, {
                "settings" : {
                    "number_of_shards": 5,
                    "number_of_replicas": 1
                    },
                # "mappings": {
                #     "hotels": {"properties": {
                #         'address': {'index': 'analyzed', 'type': 'string'},
                #         'categories': {'index': 'analyzed', 'type': 'string'},
                #         'city': {'index': 'analyzed', 'type': 'string'},
                #         'country': {'index': 'analyzed', 'type': 'string'},
                #         'latitude': {'index': 'analyzed', 'type': 'float'},
                #         'longitude': {'index': 'analyzed', 'type': 'float'},
                #         'name': {'index': 'analyzed', 'type': 'string'},
                #         'postalCode': {'index': 'analyzed', 'type': 'string'},
                #         'province': {'index': 'analyzed', 'type': 'string'},
                #         'reviews.date': {'index': 'analyzed', 'type': 'date'},
                #         'reviews.dateAdded': {'index': 'analyzed', 'type': 'date'},
                #         'reviews.rating': {'index': 'analyzed', 'type': 'float'},
                #         'reviews.text': {'index': 'analyzed', 'type': 'string'}, 
                #         'reviews.title': {'index': 'analyzed', 'type': 'string'},
                #         'reviews.usernam': {'index': 'analyzed', 'type': 'string'}
                #     }}
                # }
                })
            # self.es.indices.put_mapping(index=index, include_type_name=True, doc_type=doc_type, 
            #     body={
            #         "properties": {
            #             'address': {'index': 'analyzed', 'type': 'string'},
            #             'categories': {'index': 'analyzed', 'type': 'string'},
            #             'city': {'index': 'analyzed', 'type': 'string'},
            #             'country': {'index': 'analyzed', 'type': 'string'},
            #             'latitude': {'index': 'analyzed', 'type': 'float'},
            #             'longitude': {'index': 'analyzed', 'type': 'float'},
            #             'name': {'index': 'analyzed', 'type': 'string'},
            #             'postalCode': {'index': 'analyzed', 'type': 'string'},
            #             'province': {'index': 'analyzed', 'type': 'string'},
            #             'reviews.date': {'index': 'analyzed', 'type': 'date'},
            #             'reviews.dateAdded': {'index': 'analyzed', 'type': 'date'},
            #             'reviews.rating': {'index': 'analyzed', 'type': 'float'},
            #             'reviews.text': {'index': 'analyzed', 'type': 'text'}, 
            #             'reviews.title': {'index': 'analyzed', 'type': 'string'},
            #             'reviews.usernam': {'index': 'analyzed', 'type': 'string'}
            #     }})
            self.es.indices.put_settings(
                {
                    "mapping": {
                        "total_fields": {
                            "limit": "100000"
                        }
                    }
                }
            )
            
        # Bulk creation Operation
        data_bulk_format = []
        for doc in body_docs:
            data_bulk_format.append(json.dumps({'index': {'_index': index, '_type': doc_type}}))
            data_bulk_format.append(json.dumps(doc))
        res = self.es.bulk("\n".join(data_bulk_format))
        return res
    
    def delete(self, **kw):
        pass
    
    def update(self, **kw):
        pass
    
    def search(self, **kw):
        pass
