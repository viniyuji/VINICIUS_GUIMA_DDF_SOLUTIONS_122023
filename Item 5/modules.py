import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import nltk
from gensim.models import word2vec
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import re
import yaml
from yaml.loader import SafeLoader

@st.cache_data
def build_model(column: str):
    nltk.download('stopwords')
    STOP_WORDS = nltk.corpus.stopwords.words()
    regex = re.compile('([^\s\w]|_)+')

    data = pd.read_csv("product_search_scopus_classified.csv").dropna(how="any")
    data[column] = data[column].apply(lambda text: regex.sub('', text))
    corpus = [[token.lower() for token in str(sentence).split(" ") if token not in STOP_WORDS and token.isalpha()] for sentence in data[column]]

    return word2vec.Word2Vec(corpus, window=20, min_count=1, workers=4)

def tsne_plot(model):
    labels = model.wv.index_to_key
    tokens = model.wv.vectors

    tsne_model = TSNE(perplexity=20, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)

    x = [value[0] for value in new_values]
    y = [value[1] for value in new_values]

    figure = plt.figure(figsize=(16, 16))
    plt.style.use('dark_background')
    for i in range(len(x)):
        plt.scatter(x[i],y[i])
        plt.annotate(
            labels[i],
            xy=(x[i], y[i]),
            xytext=(5, 2),
            textcoords='offset points',
            ha='right',
            va='bottom'
        )

    return st.pyplot(figure)

def build_authenticator():
    with open('credentials.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    return stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )