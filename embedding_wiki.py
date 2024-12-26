from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import pickle
from tqdm import tqdm

def load_wiki_index(wiki_index_path):
    with open(wiki_index_path, 'rb') as f:
        wiki_index = pickle.load(f)
    
    return wiki_index

if __name__ == "__main__":
    wiki_index = load_wiki_index("./DB/wiki_index.pickle")
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                        model_kwargs={'device':'cuda:0'},
                                        encode_kwargs={'normalize_embeddings':True}
                                        )
    data = list(wiki_index.keys())
    len_faiss = len(data) // 100000
    print(f"total wiki documents: {len(data)}")
    for i in tqdm(range(len_faiss+1)):
        if i==0:
            faiss_index = FAISS.from_texts(data[:100000], embedding=embedding_model)
        elif i==len_faiss:
            faiss_index.add_texts(data[100000*i:])
        else:
            faiss_index.add_texts(data[100000*i:100000*(i+1)])
    faiss_index.save_local("./DB/faiss_index")