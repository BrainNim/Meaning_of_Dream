import pandas as pd
from langchain_community.vectorstores import FAISS


def store_to_df(store):
    v_dict = store.docstore._dict
    data_rows = []
    for key in v_dict.keys():
        doc_name = v_dict[key].metadata['source'].split('/')[-1]
        seq_num = v_dict[key].metadata['seq_num']
        content = v_dict[key].page_content
        data_rows.append({'chunk_id':key, 'document':doc_name, 'seq':seq_num, 'content':content})
    vector_df = pd.DataFrame(data_rows)
    
    return vector_df


def add_to_store(docs, original_store, embeddings):
    extension = FAISS.from_documents(docs, embeddings)
    original_store.merge_from(extension)
