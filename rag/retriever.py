import os
import certifi
from dotenv import load_dotenv
from pymongo import MongoClient

from rag.embedder import (
    embed_text,
    cosine_similarity
)

load_dotenv()

SIMILARITY_THRESHOLD = 0.75


def retrieve_relevant_docs(
    query: str,
    top_k: int = 3
) -> list[dict]:

    client = MongoClient(
        os.getenv("MONGO_URI"),
        tlsCAFile=certifi.where()
    )

    db = client["smartshopper"]

    collection = db["common_info"]

    query_embedding = embed_text(query)

    all_docs = list(
        collection.find(
            {},
            {"_id": 0}
        )
    )

    scored_docs = []

    for doc in all_docs:

        score = cosine_similarity(
            query_embedding,
            doc["question_embedding"]
        )

        scored_docs.append(
            (doc, score)
        )

    scored_docs.sort(
        key=lambda x: x[1],
        reverse=True
    )

    filtered_docs = []

    for doc, score in scored_docs:

        if score >= SIMILARITY_THRESHOLD:

            filtered_docs.append({
                "category": doc["category"],
                "question": doc["question"],
                "answer": doc["answer"],
                "similarity": score
            })

        if len(filtered_docs) >= top_k:
            break

    client.close()

    return filtered_docs