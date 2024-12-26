import yaml
import pickle
import joblib
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

def load_data(data_path):
    data = joblib.load(data_path)

    return data

def load_config(config_file):
    with open(config_file) as file:
        config = yaml.safe_load(file)

    return config

def load_embedding_model(model_name):
    embedding_model = HuggingFaceEmbeddings(model_name=model_name,
                                            model_kwargs={'device':'cuda:0'},
                                            encode_kwargs={'normalize_embeddings':True}
    )

    return embedding_model

def load_wiki_index(wiki_index_path):
    with open(wiki_index_path, 'rb') as f:
        wiki_index = pickle.load(f)
    
    return wiki_index

def load_explorer(faiss_index_path, embedding_model):
    explorer = FAISS.load_local(faiss_index_path,
                                embedding_model,
                                allow_dangerous_deserialization=True)
    
    return explorer
