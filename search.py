class EmbeddingFaiss():
    def __init__(self, explorer, wiki_index):
        self.explorer = explorer
        self.wiki_index = wiki_index
        
    def get_topk(self, argument, k=5):
        top_k = self.explorer.similarity_search(argument, k=k)
        documents = [doc.page_content for doc in top_k]
        return documents
    
    def get_search(self, argument):
        document = self.explorer.similarity_search(argument, k=1)[0].page_content
        document_content = "".join(self.wiki_index[document]['text'])

        document_content += "\nReverse HyperLinks: "
        links = []
        for link in self.wiki_index[document]['unique_reverse_hyperlink']:
            links.append(f"[{link}]")
        reversed_links = ", ".join(links)
        document_content += reversed_links
        return document_content