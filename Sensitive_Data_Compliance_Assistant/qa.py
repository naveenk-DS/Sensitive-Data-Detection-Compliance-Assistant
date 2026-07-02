from langchain_ollama import ChatOllama
from config import OLLAMA_BASE_URL, OLLAMA_MODEL
from rag import load_vector_store

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

def get_llm():
    return ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0
    )

def answer_question(question: str, text: str, document_id: str) -> str:
    """Answers a question about the document. Uses RAG for large docs or direct context for small ones."""
    llm = get_llm()
    
    # If document is small enough, use direct context
    if len(text) < 10000:
        prompt = f"""
        You are an AI Compliance and Security Assistant.
        Based on the following document content, answer the user's question accurately.
        If the answer is not in the text, say you don't know.
        
        Document Content:
        {text}
        
        Question: {question}
        """
        response = llm.invoke(prompt)
        return response.content
    else:
        # Use RAG
        vectorstore = load_vector_store(document_id)
        if not vectorstore:
            return "Error: Vector store not found for this document."
            
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        
        system_prompt = (
            "You are an AI Compliance and Security Assistant. "
            "Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, say that you don't know. "
            "Context: {context}"
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
            
        rag_chain = (
            {"context": retriever | format_docs, "input": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        return rag_chain.invoke(question)
