from flask import Flask
from flask import request
from flask_cors import CORS

from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    args = request.args
    k = 3
    if ('k' in args.keys()): k = args['k']
    
    if ('objectId' in args.keys() and args['objectId']):
        return Recommend(int(args['objectId']), False, k).get()

    if ('visitorIp' in args.keys() and args['visitorIp']):
        return Recommend(False, args['visitorIp'], k).get()
  



def loadOrginalData():
    df2 = pd.read_csv(r'./data/df.csv')
    df3 = df2.reset_index().drop(['index'], axis=1).melt(id_vars = ['objectId'])
    df3.rename(columns = {'value':'counts', 'variable':'visitorIp'}, inplace = True)
    df3['counts'].fillna(0, inplace=True)
    org = df3.pivot(index='objectId', columns='visitorIp', values='counts')
    return org

def loadItemDataAndFactors():
    item = pd.read_json('./data/item_factors.json')
    item_enum = {r: i for i, r in enumerate(item.index.values)}
    return [item, item_enum]

def loadUserDataAndFactors():
    user = pd.read_json('./data/user_factors.json')
    user_enum = {r: i for i, r in enumerate(user.index.values)}
    return [user, user_enum]

def loadBiases():
    user_bias = pd.read_json('./data/user_bias.json', typ='series')
    item_bias = pd.read_json('./data/item_bias.json', typ='series')
    return [user_bias.to_frame(), item_bias.to_frame()]



class Recommend(object):

    def __init__(self, objectId = False, visitorIp = False, k = 3):
        self.objectId = objectId
        self.visitorIp = visitorIp
        self.k = k

        self.orginal_data = loadOrginalData()
        self.item, self.item_enum = loadItemDataAndFactors()    
        self.user, self.user_enum = loadUserDataAndFactors()

        self.user_bias, self.item_bias = loadBiases()
        
        self.ratings = np.dot(self.item, self.user.T)
        
        return None

    def get(self):
        if (self.objectId and self.objectId not in self.item_enum): 
                return "Nedovoljan broj zapisa za traženi smještaj"
        if (self.visitorIp and self.visitorIp not in self.user_enum): 
                return "Nedovoljan broj zapisa o traženom korisniku"


        if (self.objectId and self.objectId in self.item_enum): return self.basedOnItem()
        if (self.visitorIp and self.visitorIp in self.user_enum): return self.basedOnUser()

    def basedOnUser(self):
        user_ratings = [row[self.user_enum.get(self.visitorIp)] + self.item_bias.to_numpy()[i][0] for i, row in enumerate(self.ratings)]
        orginal_user_ratings = self.orginal_data[self.visitorIp]
        orginal_user_ratings = orginal_user_ratings[orginal_user_ratings != 0]

        if (len(orginal_user_ratings)):
            indices_to_ignore = [self.item_enum.get(i) for i in list(orginal_user_ratings.keys())]
            for index in indices_to_ignore:
                if index is not None:
                    user_ratings[index] = -10

        object_indices = list(self.item_enum.keys())
        return [int(object_indices[idx]) for idx in np.array(user_ratings).argsort()[-self.k:][::-1]]    
            
    def basedOnItem(self):
        itemIndex = self.item_enum.get(self.objectId)
        matrix = csr_matrix(self.ratings)

        object_indices = list(self.item_enum.keys())

        knn_model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=self.k, n_jobs=-1)
        knn_model.fit(matrix)

        udaljenosti, indeksi = knn_model.kneighbors(matrix[itemIndex], n_neighbors=self.k+1)
        preporuke = sorted(list(zip(indeksi.squeeze().tolist(), udaljenosti.squeeze().tolist())), key=lambda x: x[1])[:0:-1]
        return [int(object_indices[idx]) for i, (idx, dist) in enumerate(preporuke) if (object_indices[idx] != self.objectId)]