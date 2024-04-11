# document load
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader

loader = DirectoryLoader('./sample_data/', glob="**/*.json",  # 디렉토리 위치, 파일 형식
                         loader_cls=TextLoader,  # 기본적인 load 방식 설정
                         loader_kwargs={'autodetect_encoding': True})  # utf8 인코딩 에러 해결
document = loader.load()



# JSON Loader
from langchain_community.document_loaders import JSONLoader

import json
from pathlib import Path
from pprint import pprint


file_path='./data/물건/모자 꿈 수정.json'
data = json.loads(Path(file_path).read_text())

loader = JSONLoader(
    file_path=file_path,
    jq_schema='.[].content',
    text_content=False)

document = loader.load()


# text split
from langchain.text_splitter import CharacterTextSplitter
text_splitter = CharacterTextSplitter(chunk_size=1000,  # 쪼개는 글자 수
                                      chunk_overlap=0,  # 오버랩 글자 수
                                      separator=',')    # 문서별 구분자
docs = text_splitter.split_documents(document)


# 벡터 임베딩

# bedrock 임베딩 모델 설정
import boto3
from langchain.embeddings import BedrockEmbeddings  # bedrock 임베딩모델 사용
from langchain_community.vectorstores import FAISS  # 벡터 저장

bedrock = boto3.client(service_name='bedrock-runtime')
bedrock_embeddings = BedrockEmbeddings(model_id='amazon.titan-embed-text-v1', client=bedrock)

# 벡터 임베딩
vector = FAISS.from_documents(docs, bedrock_embeddings)
vector.save_local("faiss_index")  # 로컬에 저장

# # 저장한 벡터 불러오기
# vector = FAISS.load_local("faiss_index", bedrock_embeddings, allow_dangerous_deserialization=True)

# # 테스트
# vector.similarity_search("모자가 바람에 날아가는 꿈은 무슨 뜻일까?", k=1)
# vector.similarity_search_with_score("모자가 바람에 날아가는 꿈은 무슨 뜻일까?", k=3)





