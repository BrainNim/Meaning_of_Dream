import boto3
from langchain.llms.bedrock import Bedrock
from langchain.embeddings import BedrockEmbeddings  # bedrock 임베딩모델 사용
from langchain_community.vectorstores import FAISS  # 벡터 저장

from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough


# 모델명 지정
embedding_model_id = 'amazon.titan-embed-text-v1'
chat_model_id = 'anthropic.claude-v2:1'

# Bedrock & 모델 설정
bedrock = boto3.client(service_name='bedrock-runtime')
embeddings = BedrockEmbeddings(model_id=embedding_model_id, client=bedrock)
llm = Bedrock(model_id=chat_model_id, client=bedrock)

# 벡터 저장소 불러오기 & retriever 설정
vector = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
retriever = vector.as_retriever(search_kwargs={'k': 3})


class ChatService:
    def __init__(self):
        # vector 로드 반복을 방지하기 위해 BedrockService class를 직접 상속 하지 않음

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are a helpful assistant. 
                    Answer questions using only the following context that between <context> and </context>. 
                    
                    <context> {context} </context>
                    
                    And, You are the world's most skilled last night dream interpreter.
                    Your role is to interpret the meaning inside a story that a user asks you.
                    To fulfil your role, you take the following steps
                    1) Analyse: Analyse the actions, who is doing what, and what is being done in the story in the user's dream.
                    2) Select: From the contents of <context>, select two or three documents that best matches the context of the analysis.
                    3) Interpretation: Interpret the user's dream based on the information in the analysed and selected documents.
                    4) Scoring: Based on the interpretation result, the luckiness is scored on a 5-point scale. result's data type is integer.
                    5) Summarise: Create a title of 2-3 words based on user's dream and interpretation.
                    
                    After finalising the above steps, you provide the user with an answer in the following format.
                    ```
                    <?xml version="1.0" encoding="UTF-8"?>
                    <Response>
                        <title> (Summarise) </title>
                        <Interpret> (Interpret) </Interpret>
                        <Score> (Score) </Score>
                    </Response>
                    ```
                    """,
                ),
                ("human", "{question}"),
            ]
        )

    def interpret_dream(self, question):
        chain = (
                {
                    "context": retriever,
                    "question": RunnablePassthrough(),
                }
                | self.prompt
                | llm
        )
        answer = chain.invoke(question)
        return answer
