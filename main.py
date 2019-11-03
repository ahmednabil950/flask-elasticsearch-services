import tools as tools
import requests
import json
import time

if __name__ == "__main__":
    # load data csv format
    data = tools.load_data()
    
    # filter only Hotels Category reviews
    hotels = tools.filter_by_column(data, 'categories', 'Hotels')
    
    # drop 'NaN' columns
    hotels = hotels.drop(columns=['reviews.userCity', 'reviews.id', 'reviews.userProvince', 'reviews.doRecommend'])
    
    # 'NaN' problem whe indexing in ES
    hotels = hotels.dropna()
    
    # group by hotel name so each hotel will have encapsulated documents
    jsonified_data = {}
    for i, (name, group) in enumerate(hotels.groupby('name')):
        if i == 3: break
        print('indexing {}'.format(name))
        jsonified_data[name] = group.T.to_dict()
        
        
    requests.post('http://127.0.0.1:5000/indexer/', json=jsonified_data)
    