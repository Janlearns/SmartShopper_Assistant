from google.adk.tools import FunctionTool
from rag.retriever import retrieve_relevant_docs

def get_common_information(query: str) -> str:
    relevant_docs = retrieve_relevant_docs(query, top_k=3)

    if not relevant_docs:
        return (
            "Maaf, saya tidak menemukan informasi yang relevan dengan pertanyaan kamu. "
            "Silakan hubungi customer service kami untuk bantuan lebih lanjut."
        )

    context_parts = []

    for i, doc in enumerate(relevant_docs, start=1):
        context_parts.append(
            f"[{i}] Kategori: {doc['category']}\n"
            f"    Q: {doc['question']}\n"
            f"    A: {doc['answer']}"
        )

    context = "\n\n".join(context_parts)

    best_answer = relevant_docs[0]["answer"]

    response = (
        f"Berdasarkan informasi yang tersedia:\n\n"
        f"{best_answer}\n\n"
        f"---\n"
        f"Informasi terkait lainnya:\n{context}"
    )

    return response


common_info_tool = FunctionTool(func=get_common_information)