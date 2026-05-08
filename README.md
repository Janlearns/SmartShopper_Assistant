# 🛍️ Personalized SmartShopper Assistant

AI Agent berbasis Google ADK yang mampu menjawab pertanyaan seputar **rekomendasi produk** dan **informasi umum belanja** secara otomatis menggunakan strategi RAG (Retrieval-Augmented Generation).

---

## 📌 Deskripsi

SmartShopper Assistant adalah AI Agent yang mengintegrasikan dua tools utama:

- **Product Recommendation Tool** — Memberikan rekomendasi produk berdasarkan kebutuhan user
- **Common Information Tool** — Menjawab pertanyaan umum seputar pengiriman, pembayaran, refund, dll menggunakan strategi RAG dengan data yang tersimpan di MongoDB Atlas

Agent melakukan **routing otomatis** berdasarkan jenis pertanyaan user tanpa perlu input tambahan dari pengguna.

---

## 🗂️ Struktur Project

```
smartshopper-assistant/
├── agent.py                        # Main AI Agent (entry point)
├── tools/
│   ├── __init__.py
│   ├── product_tool.py             # Tool rekomendasi produk
│   └── common_info_tool.py         # Tool common information (RAG)
├── rag/
│   ├── __init__.py
│   ├── embedder.py                 # Embedding teks & cosine similarity
│   └── retriever.py                # Retrieval dokumen dari MongoDB
├── data/
│   ├── common_info_dataset.json    # Dataset common information
│   └── store_to_mongo.py           # Script storing data ke MongoDB Atlas
├── requirements.txt
└── .env
```

---

## ⚙️ Tech Stack

| Komponen           | Teknologi                               |
| ------------------ | --------------------------------------- |
| AI Agent Framework | Google ADK                              |
| LLM                | gemini-flash-latest                     |
| Database           | MongoDB Atlas                           |
| Embedding Model    | SentenceTransformers (all-MiniLM-L6-v2) |
| RAG Strategy       | Cosine Similarity Vector Search         |
| Language           | Python 3.12                             |

---

## 🚀 Cara Menjalankan

### 1. Clone repository & buat virtual environment

```bash
git clone <repo-url>
cd smartshopper-assistant
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Konfigurasi environment variable

Buat file `.env` di root project:

```env
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
GOOGLE_API_KEY=your_google_api_key_here
```

- **MONGO_URI** — didapat dari MongoDB Atlas → Connect → Drivers
- **GOOGLE_API_KEY** — didapat dari [Google AI Studio](https://aistudio.google.com)

### 4. Store dataset ke MongoDB Atlas

```bash
cd data
python store_to_mongo.py
cd ..
```

### 5. Jalankan AI Agent

```bash
python agent.py
```

---

## 💬 Contoh Penggunaan

```
============================================================
SmartShopper Assistant - AI Agent
Ketik 'exit' atau 'quit' untuk keluar
============================================================

Kamu: Rekomendasikan laptop gaming budget 8 juta
Assistant: Halo! Berikut rekomendasi laptop gaming untuk budget sekitar 8 juta...

Kamu: Berapa lama proses refund?
Assistant: Halo! Proses refund membutuhkan waktu 3-7 hari kerja setelah barang diterima kembali...

Kamu: exit
Terima kasih sudah menggunakan SmartShopper Assistant!
```

---

## 🔀 Routing Logic

Agent secara otomatis memilih tool yang tepat berdasarkan jenis pertanyaan:

| Jenis Pertanyaan                            | Tool yang Digunakan          |
| ------------------------------------------- | ---------------------------- |
| Rekomendasi produk, laptop, HP, gadget      | `get_product_recommendation` |
| Pengiriman, refund, pembayaran, cara daftar | `get_common_information`     |

---

## 🧠 Arsitektur RAG

```
User Query
    ↓
Embed query → vector (384 dimensi)
    ↓
Hitung cosine similarity dengan semua dokumen di MongoDB
    ↓
Ambil top-3 dokumen paling relevan
    ↓
Susun konteks → kembalikan jawaban ke Agent
```

---

## 📦 Dependencies

```
google-adk
pymongo
certifi
sentence-transformers
python-dotenv
numpy
```

---

## 👤 Author

**Rayzan Fazri Ramdany**  
Data Science and Machine Learning Bootcamp — Dibimbing.id
