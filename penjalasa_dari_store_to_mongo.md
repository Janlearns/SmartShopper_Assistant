# Penjelasan: store_to_mongo.py

## Tujuan

Script ini bertugas menyimpan dataset Common Information ke MongoDB Atlas, lengkap dengan vector embedding untuk keperluan RAG (Retrieval-Augmented Generation).

---

## Struktur Dokumen yang Disimpan

Setiap record yang disimpan ke MongoDB memiliki struktur berikut:

```json
{
  "category"  : "pengiriman",
  "question"  : "Berapa lama waktu pengiriman?",
  "answer"    : "Untuk wilayah Jawa 1-3 hari kerja...",
  "embedding" : [0.021, -0.043, ...]
}
```

| Field       | Tipe          | Keterangan                                               |
| ----------- | ------------- | -------------------------------------------------------- |
| `category`  | string        | Kategori pertanyaan (pengiriman, refund, pembelian, dll) |
| `question`  | string        | Teks pertanyaan asli                                     |
| `answer`    | string        | Teks jawaban untuk pertanyaan tersebut                   |
| `embedding` | list of float | Vector 384 dimensi hasil encoding model                  |

---

## Strategi Penyimpanan

### 1. Drop & Re-insert

Collection di-drop terlebih dahulu sebelum insert ulang. Strategi ini memastikan data selalu bersih dan tidak ada duplikasi saat script dijalankan ulang (idempotent).

### 2. Embedding per Dokumen

Setiap dokumen di-embed menggunakan model `all-MiniLM-L6-v2` dari SentenceTransformers. Teks yang di-embed adalah gabungan `question + answer` agar vector mencakup konteks pertanyaan sekaligus jawabannya, sehingga proses retrieval lebih akurat.

### 3. Bulk Insert

Semua dokumen dikumpulkan dalam satu list terlebih dahulu, lalu di-insert sekaligus menggunakan `insert_many()` untuk efisiensi dibanding insert satu per satu.

### 4. Koneksi Aman (TLS/SSL)

Koneksi ke MongoDB Atlas menggunakan `tlsCAFile=certifi.where()` untuk memastikan SSL handshake berhasil di environment Windows dengan Python 3.12.

---

## Alur Eksekusi

```
Baca MONGO_URI dari .env
        ↓
Koneksi ke MongoDB Atlas (dengan TLS)
        ↓
Drop collection lama
        ↓
Load model SentenceTransformer
        ↓
Baca common_info_dataset.json
        ↓
Loop setiap item → encode(question + answer) → buat dokumen
        ↓
insert_many() → simpan ke MongoDB Atlas
        ↓
Tutup koneksi
```
