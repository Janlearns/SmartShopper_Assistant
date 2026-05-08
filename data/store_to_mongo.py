import json
import os
import certifi
from dotenv import load_dotenv
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

load_dotenv()

def store_common_info():
    mongo_uri = os.getenv("MONGO_URI")

    client = MongoClient(mongo_uri, tlsCAFile=certifi.where())

    db = client["smartshopper"]
    collection = db["common_info"]

    collection.drop()
    print("Collection lama dihapus.")

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    with open("common_info_dataset.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)

    documents_to_insert = []

    for item in dataset:
        text_to_embed = f"{item['question']} {item['answer']}"
        embedding = model.encode(text_to_embed).tolist()

        document = {
            "category": item["category"],
            "question": item["question"],
            "answer": item["answer"],
            "embedding": embedding
        }

        documents_to_insert.append(document)

    result = collection.insert_many(documents_to_insert)

    print(f"Berhasil menyimpan {len(result.inserted_ids)} dokumen ke MongoDB Atlas.")
    print("Struktur dokumen yang disimpan:")
    print("  - category  : kategori pertanyaan (string)")
    print("  - question  : teks pertanyaan (string)")
    print("  - answer    : teks jawaban (string)")
    print("  - embedding : vector float 384 dimensi (list of float)")

    client.close()

if __name__ == "__main__":
    store_common_info()