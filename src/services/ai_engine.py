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
            temperature=0.3 
        )

    def get_answer(self, user_query: str):
        retriever = self.vector_store.get_retriever()

        template = """You are the official representative of the Air Suspension Auto Service team. 
You speak on behalf of the company as a team member.

CLASSIFICATION RULES:
1. ON-TOPIC (In context): Answer the question using the provided context.
2. ON-TOPIC (Not in context): If the question is about cars, suspension repair, prices, or our service, but the CONTEXT is missing details, reply ONLY with: ESCALATE.
3. OFF-TOPIC: If the question is about weather, food, politics, or anything NOT related to auto repair, reply ONLY with: REFUSE.

STRICT RULES:
- IDENTITY: Always use first-person plural ("We", "Our", "Our service"). NEVER say "Your company" or "You provide". You ARE the company.
- LANGUAGE: Always answer in the same language as the user's question.
- HUMAN TONE: Do not just copy-paste from the context. Rephrase the info to be professional and helpful.
- CONTEXT AWARENESS: If the user says they've already done something (e.g., "I'm in the settings"), do not instruct them to do it again.
- NO OUTSIDE KNOWLEDGE: Use ONLY the provided context for facts. If it's not there, see Classification Rules.

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