import bz2
import os
import json
import pickle
from bs4 import BeautifulSoup
from tqdm import tqdm

def parsing_hyperlink(text_with_links):
    hyperlink_texts = []
    for html in text_with_links:
        soup = BeautifulSoup(html, 'html.parser')
        for a in soup.find_all('a'):
            hyperlink_texts.append(a.get_text())
    return hyperlink_texts

def make_wiki_dict(path, wiki_dict):
    with open(path, 'rb') as f:
        data = f.read()
        data = bz2.decompress(data).decode()
        for data_split in data.split("\n")[:-1]:
            data_json = json.loads(data_split)
    
            title = data_json['title']
            text = data_json['text']
            hyperlink = parsing_hyperlink(data_json['text_with_links'])
            wiki_dict[title] = {
                "text": text,
                "hyperlink": hyperlink,
                "reverse_hyperlink": [],
                "unique_reverse_hyperlink": []}

    return wiki_dict

if __name__ == "__main__":
    wiki_path = "./enwiki-20171001-pages-meta-current-withlinks-abstracts"
    wiki_path_list = []
    wiki_dict = dict()

    for middle_path in tqdm(os.listdir(wiki_path)):
        path = os.path.join(wiki_path, middle_path)
        for last_path in os.listdir(path):
            wiki_dict = make_wiki_dict(os.path.join(path, last_path), wiki_dict)
    
    for key in tqdm(wiki_dict.keys()):
        for hyperlink in wiki_dict[key]['hyperlink']:
            try:
                wiki_dict[hyperlink]['reverse_hyperlink'].append(key)
            except:
                continue
            
    for key in tqdm(wiki_dict.keys()):
        for hyperlink in wiki_dict[key]['reverse_hyperlink']:
            if hyperlink not in wiki_dict[key]['hyperlink']:
                wiki_dict[key]['unique_reverse_hyperlink'].append(hyperlink)
    
    os.makedirs("./DB", exist_ok=True)
    with open('./DB/wiki_index.pickle', 'wb') as f:
        pickle.dump(wiki_dict, f)
