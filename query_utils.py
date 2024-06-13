from sentence_transformers import CrossEncoder
import openai
import numpy as np

def rank_doc(query, text_chunks, topN=5):
    reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    scores = reranker.predict([[query, doc] for doc in text_chunks])
    top_indices = np.argsort(scores)[::-1][:topN]
    top_pairs = [text_chunks[index] for index in top_indices]
    return top_pairs

def rag(query, retrieved_documents, api_key):
    model = "gpt-4o"
    openai.api_key = api_key

    information = "\n\n".join(retrieved_documents)
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Your users are asking questions about information contained in PDF documents and you'll answer them to the best of your abilities."
        },
        {"role": "user", "content": f"Question: {query}. \n Information: {information}"}
    ]
    
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
    )
    content = response.choices[0].message.content
    return content
