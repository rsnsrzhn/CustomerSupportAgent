from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from .vector_store import VectorStoreService
from src.core.config import settings

class AIEngine:
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name="llama-3.1-8b-instant",
            temperature=0
        )

    def get_answer(self, user_query: str):
        retriever = self.vector_store.get_retriever()

        template = """You are a strict Customer Support Assistant.
Use ONLY the provided context to answer the question. 

RULES:
1. If the context is empty or does not contain the answer, reply with ONLY the word: ESCALATE.
2. Do not use any outside knowledge.
3. Be concise and professional.

CONTEXT:
{context}

QUESTION: {question}

YOUR RESPONSE:"""

        prompt = ChatPromptTemplate.from_template(template)

        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

        try:
            response = rag_chain.invoke(user_query)
            return response.strip()
        except Exception as e:
            print(f"Error in AI Engine: {e}")
            return "ESCALATE"