import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# import re
import json

# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')

from nltk.corpus import stopwords
from nltk import word_tokenize as tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial import cKDTree as KDTree

# read_cols = ['brewery_id', 'name', 'style_id', 'abv', 'ibu', 'descript', 'id']
# df = pd.read_csv('./beers-cleaned.csv', encoding='latin-1', usecols=read_cols)

# df = df[~df.descript.isnull()]
# df.reset_index(inplace=True, drop=True)
# df = df.rename(columns={'descript':'text', 'name':'beer_name', 'id':'beer_id'})

# # more bitter less bitter based on the mean of its style
# style = pd.read_csv('./styles.csv')
# style['mean'] = (style.IBU_low + style.IBU_High) / 2
# bitter_map = style[['mean']].to_dict()
# df['ibu_style_mean'] = df.style_id.map(bitter_map['mean'])
# df['bitter'] = np.where(df.ibu > df.ibu_style_mean, 1, 0)
# style = style.rename(columns={'id':'style_id'})
# df = df.merge(style[['style_id','style_name']], on='style_id', how='left')

# df.abv = df.abv.apply(lambda x: x + '.0' if '.' not in x else x)
# df['abv'] = df.abv.apply(lambda x: re.findall('(\d+.\d+)', x)[0])
# df.abv = df.abv.astype(float)

# brewery = pd.read_csv('./breweries.csv')
# brewery = brewery[['id','name', 'city', 'state', 'country']]
# brewery = brewery.rename(columns={'id':'brewery_id', 'name':'brewery_name'})

# df = df.merge(brewery, on='brewery_id', how='left')

# df = df.drop(['style_id','brewery_id'], axis=1)

# df.to_csv('./cleaned_berr_data_asilva_11232019.csv')

def closest_beer(user_input):
    
    user_dict = json.loads(user_input)
    
    n_neighbors = float(user_dict['neighbors'])

    read_cols = ['beer_id', 'text', 'bitter', 'abv']

    df = pd.read_csv('./cleaned_berr_data_asilva_11232019.csv', usecols=read_cols)

    user_data = pd.DataFrame(user_dict, index=[99999])
    user_data['beer_id'] = 99999
    user_data.bitter = np.where((user_data.bitter.str.lower().str.contains('y')), 1, 0)
    user_data.abv = user_data.abv.astype(float)
    user_data = user_data[read_cols]

    df = df.append(user_data, sort=False)
    df = df.reset_index(drop=True)
    
    # below 3, 3-4.5, 4.5-5.5, 5.5-6.5, 6.5-7.5, 7.5-8.5, 9.5-10.5, greater than 10.5
    abv_cols = ['lt_3', '3-4.5', '4.5-5.5', '5.5-6.5',' 6.5-7.5', '7.5-8.5', '9.5-10.5', 'gt_10.5']

    for col in abv_cols:
        df[col] = 0

    zero = df[(df.abv <= 3.0)].index
    one = df[(df.abv > 3) & (df.abv <= 4.5)].index
    two = df[(df.abv > 4.5) & (df.abv <= 5.5)].index
    three = df[(df.abv > 5.5) & (df.abv <= 6.5)].index
    four = df[(df.abv > 6.5) & (df.abv <= 7.5)].index
    five = df[(df.abv > 7.5) & (df.abv <= 8.5)].index
    six = df[(df.abv > 8.5) & (df.abv <= 9.5)].index
    seven = df[(df.abv > 9.5) & (df.abv <= 10.5)].index
    eight = df[df.abv > 10.5].index

    abv_indices = [zero, one, two, three, four, five, six, seven, eight]

    for name, indices in zip(abv_cols, abv_indices):
        df.at[indices, name] = 1

    stopsawords = stopwords.words('english')
    ps = WordNetLemmatizer()

    df['nlp_text'] = df.text.str.lower()
    df['nlp_text'] = df.nlp_text.str.replace('[^a-z]+', ' ')
    df['nlp_text'] = df.nlp_text.apply(lambda x: tokenize(x))
    df['nlp_text'] = df.nlp_text.apply(lambda x: [i for i in x if i not in stopsawords])
    df['nlp_text'] = df.nlp_text.apply(lambda x: [ps.lemmatize(i) for i in x])

    vectorizer = TfidfVectorizer()

    df['text_vect'] = df.nlp_text.apply(lambda x: ' '.join(x))
    text_vect = vectorizer.fit_transform(df['text_vect']).toarray()

    df = pd.concat([df, pd.DataFrame(text_vect)], axis=1)
    
    df = df[list(set(df.columns) - set(['nlp_text', 'text_vect', 'text']))]

    cols = list(set(df.columns) - set(['beer_id']))
    tree = KDTree(df[cols])

    neighbor_indices = tree.query(df[df.beer_id == 99999][cols], k=n_neighbors + 1)[-1]
    
    ids = df.iloc[neighbor_indices[0][1::]]['beer_id'].values
    
    return json.dumps({'beer_id': [int(x) for x in ids]})


if __name__ == '__main__':
    # test_josn = json.dumps({"abv": "5", "text": "light fruity beer", "bitter": "no", "neighbors": "6"})
    test_josn = json.dumps({"abv": "5", "text": "I want a frothy winter strong man's beer because I'm a hardy manly man *muscle emoji*", "bitter": "no", "neighbors": "6"})
    output = closest_beer(test_josn)
    print(output)


