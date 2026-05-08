import os
from dotenv import load_dotenv
from pymongo import MongoClient
from rag.embedder import embed_text, cosine_similarity

load_dotenv()

def retrieve_relevant_docs(query: str, top_k: int = 3) -> list[dict]:
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["smartshopper"]
    collection = db["common_info"]

    query_embedding = embed_text(query)

    all_docs = list(collection.find({}, {"_id": 0}))

    scored_docs = []

    for doc in all_docs:
        score = cosine_similarity(query_embedding, doc["embedding"])
        scored_docs.append((doc, score))

    scored_docs.sort(key=lambda x: x[1], reverse=True)

    top_docs = [doc for doc, score in scored_docs[:top_k]]

    client.close()

    return [
        {
            "category": doc["category"],
            "question": doc["question"],
            "answer": doc["answer"]
        }
        for doc in top_docs
    ]