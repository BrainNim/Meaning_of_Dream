from tqdm import tqdm

# JSON Loader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import JSONLoader

# text split
from langchain.text_splitter import CharacterTextSplitter

# bedrock
import boto3
from langchain.embeddings import BedrockEmbeddings  # bedrock 임베딩모델 사용
from langchain_community.vectorstores import FAISS  # 벡터 저장
from common.common_function import *


# file load
glob_condition = '**/*.json'
loader = DirectoryLoader('./data', glob=glob_condition,  # 디렉토리 위치, 파일 형식
                         loader_cls=JSONLoader,  # 기본적인 load 방식 설정
                         loader_kwargs={'jq_schema':'.[].content'},  # utf8 인코딩 에러 해결
                         show_progress=True)
document = loader.load()


# document split
text_splitter = CharacterTextSplitter(chunk_size=1000,  # 쪼개는 글자 수
                                      chunk_overlap=0,)  # 오버랩 글자 수
docs = text_splitter.split_documents(document)


# 벡터 임베딩
bedrock = boto3.client(service_name='bedrock-runtime')
bedrock_embeddings = BedrockEmbeddings(model_id='amazon.titan-embed-text-v1', client=bedrock)

# vector = FAISS.from_documents(docs, bedrock_embeddings)
# chunk_docs = docs[:10]
# vector = FAISS.from_documents(chunk_docs, bedrock_embeddings)
# vector.save_local("faiss_index")  # 로컬에 저장

# 저장한 벡터 불러오기
# vector = FAISS.load_local("faiss_index", bedrock_embeddings, allow_dangerous_deserialization=True)


# 벡터 임베딩
start_num = 7748
for i in tqdm(range(start_num, len(docs))):
    chunk_doc = [docs[i]]  # docs는 list형태여야 함
    if i == 0:
        vector = FAISS.from_documents(chunk_doc, bedrock_embeddings)
    else:
        add_to_store(docs=chunk_doc, original_store=vector, embeddings=bedrock_embeddings)

    if i % 100 == 0:
        vector.save_local("faiss_index")  # 로컬에 저장
        vector = FAISS.load_local("faiss_index", bedrock_embeddings, allow_dangerous_deserialization=True)  # 로컬에 저장한 벡터 불러오기


# 결과 확인
print(len(store_to_df(vector)))
print(store_to_df(vector).tail)


# # 테스트
# vector.similarity_search("모자가 바람에 날아가는 꿈은 무슨 뜻일까?", k=1)
# vector.similarity_search_with_score("모자가 바람에 날아가는 꿈은 무슨 뜻일까?", k=3)
